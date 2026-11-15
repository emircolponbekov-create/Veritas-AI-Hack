"""Publication identity, failure isolation, refresh and consumer/technical views."""
import asyncio
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src/ui'))
from environment_loader import REPORTS, ReportSnapshot, report_snapshot


class ReportReaderTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        shutil.copytree(ROOT / REPORTS, self.root / REPORTS)

    def update(self, filename, value, plant=3806):
        directory = self.root / REPORTS / f'eia_{plant}'
        path = directory / filename
        path.write_text(json.dumps(value), encoding='utf-8')
        manifest_path = directory / 'ready.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['sha256'][filename] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')

    def test_real_report_scope_period_and_other_station(self):
        surry = report_snapshot(3806, self.root)
        self.assertEqual(surry.state, 'ready')
        self.assertIn('1970s', surry.report['period_label'])
        self.assertIn('2010', surry.report['period_label'])
        self.assertIn('2025', surry.report['period_label'])
        self.assertEqual(surry.technical['local_checks']['water']['start'], '2010-01')
        self.assertEqual(surry.technical['local_checks']['water']['end'], '2025-12')
        self.assertEqual(surry.technical['local_checks']['water']['system'], 'CW1')
        calvert = report_snapshot(6011, self.root)
        self.assertEqual(calvert.state, 'insufficient_evidence')
        self.assertNotIn('Surry', json.dumps(calvert.report))
        self.assertEqual(report_snapshot(6000, self.root).state, 'missing')
        self.assertEqual(report_snapshot(3806, self.root).report, surry.report)

    def test_missing_corrupt_and_wrong_identity_are_withheld(self):
        directory = self.root / REPORTS / 'eia_3806'
        report = json.loads((directory / 'report.en.json').read_text())
        report['plant_id_eia'] = 6011
        self.update('report.en.json', report)
        self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')
        (directory / 'report.en.json').write_text('{broken')
        self.assertIsNone(report_snapshot(3806, self.root).report)
        (directory / 'ready.json').unlink()
        self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')

    def test_contract_shape_and_unsafe_link_rejected_even_with_new_hash(self):
        publication = report_snapshot(3806, self.root).report
        for value in ('javascript:alert(1)', 'file:///private'):
            report = deepcopy(publication)
            report['sections'][0]['references'][0]['url'] = value
            self.update('report.en.json', report)
            self.assertIsNone(report_snapshot(3806, self.root).report)
        report = deepcopy(publication)
        report['sections'] = []
        self.update('report.en.json', report)
        self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')

    def test_unresolved_conflict_blocks_public_copy(self):
        technical = deepcopy(report_snapshot(3806, self.root).technical)
        technical['accepted_claims'][0]['conflict_state'] = 'unresolved'
        self.update('technical.json', technical)
        result = report_snapshot(3806, self.root)
        self.assertEqual(result.state, 'review_required')
        self.assertIsNone(result.report)

    def test_refresh_reads_new_publication_without_cached_copy(self):
        before = report_snapshot(3806, self.root)
        report = deepcopy(before.report)
        report['as_of'] = '2026-11-14'
        self.update('report.en.json', report)
        after = report_snapshot(3806, self.root)
        self.assertEqual(after.state, 'ready')
        self.assertNotEqual(before.version, after.version)
        self.assertEqual(after.report['as_of'], '2026-11-14')

    def test_missing_module_and_publication_race(self):
        with patch('environment_loader.importlib.import_module', side_effect=ImportError('private detail')):
            self.assertEqual(report_snapshot(3806, self.root).state, 'module_unavailable')
        from src.model.environment_report import read_report
        real_import = __import__('importlib').import_module
        module = real_import('src.model.environment_report')
        def changing_read(directory, plant):
            report = read_report(directory, plant)
            (directory / 'technical.json').write_text('{}')
            return report
        with patch.object(module, 'read_report', side_effect=changing_read):
            self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')


class ReportScreenTests(unittest.TestCase):
    def setUp(self):
        if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':
            def nonrunning_loop():
                loop = MagicMock(spec=asyncio.AbstractEventLoop)
                loop.is_closed.return_value = False
                return loop
            factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop', side_effect=nonrunning_loop)
            factory.start()
            self.addCleanup(factory.stop)

    def screen(self):
        from streamlit.testing.v1 import AppTest
        return AppTest.from_file(str(ROOT / 'src/ui/app.py')).run(timeout=30)

    def public_copy(self, screen):
        return '\n'.join(node.value for node in screen.text)

    def test_consumer_view_switching_sources_and_technical_details(self):
        screen = self.screen()
        self.assertFalse(screen.exception, str(screen.exception))
        self.assertIn('James River', self.public_copy(screen))
        self.assertEqual(len(screen.metric), 3)
        self.assertEqual(len(screen.selectbox), 2)
        self.assertTrue(any('vdh.virginia.gov' in node.url for node in screen.link_button))
        captions = ' '.join(node.value for node in screen.caption)
        self.assertIn('does not change with the historical month', captions)
        self.assertIn('System CW1', captions)
        screen.selectbox(key='system_3806').select('eia_3806_435732').run(timeout=30)
        self.assertTrue(any('CW1 findings are omitted' in node.value for node in screen.info))
        screen.selectbox(key='plant').select(6011).run(timeout=30)
        self.assertNotIn('James River', self.public_copy(screen))
        self.assertFalse(any('vdh.virginia.gov' in node.url for node in screen.link_button))
        self.assertIn('No station-specific environmental evidence', self.public_copy(screen))
        screen.selectbox(key='plant').select(6000).run(timeout=30)
        self.assertTrue(any('No environmental report' in node.value for node in screen.info))
        self.assertNotIn('James River', self.public_copy(screen))
        screen.selectbox(key='plant').select(3806).run(timeout=30)
        screen.selectbox(key='system_3806').select('eia_3806_435731').run(timeout=30)
        screen.toggle(key='technical_details').set_value(True).run(timeout=30)
        self.assertFalse(screen.exception)
        self.assertEqual(screen.metric[2].value, '6.67')
        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [22] * 3)
        screen.select_slider[0].set_value('2025-10').run(timeout=30)
        self.assertIn('James River', self.public_copy(screen))
        screen.toggle(key='technical_details').set_value(False).run(timeout=30)
        screen.toggle(key='technical_details').set_value(True).run(timeout=30)
        self.assertEqual(screen.select_slider[0].value, '2025-10')

    def test_report_failures_keep_legacy_results_and_hide_diagnostics(self):
        for state in ('evidence_unavailable', 'review_required', 'module_unavailable'):
            with self.subTest(state=state), patch('environment_panel.report_snapshot', return_value=ReportSnapshot(state)):
                screen = self.screen()
                self.assertFalse(screen.exception)
                self.assertNotIn('James River', self.public_copy(screen))
                screen.toggle(key='technical_details').set_value(True).run(timeout=30)
                self.assertFalse(screen.exception)
                self.assertEqual(len(screen.metric), 5)
                self.assertEqual(len(screen.dataframe), 1)


if __name__ == '__main__':
    unittest.main()
