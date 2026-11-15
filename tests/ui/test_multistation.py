"""Read-only integration, artifact races and Streamlit selection regressions."""
from copy import deepcopy
import asyncio
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src/ui'))
from multistation_loader import registry_snapshot, measurements_snapshot, verified_results
from data_loader import DataError


class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.token = registry_snapshot()
        cls.surry = next(e for e in cls.registry['datasets'] if e['plant_id_eia'] == 3806 and e['cooling_id_eia'] == 'CW1')
        cls.calvert = next(e for e in cls.registry['datasets'] if e['plant_id_eia'] == 6011)

    def test_all_seventeen_saved_models(self):
        entries = [e for e in self.registry['datasets'] if e['status'] == 'ready_for_model_check']
        self.assertEqual(len(entries), 17)
        for entry in entries:
            with self.subTest(dataset=entry['dataset_id']):
                measurements, _ = measurements_snapshot(entry, self.token)
                result, scores = verified_results(entry, measurements, self.token)
                self.assertEqual(len(result), entry['split_counts']['test'])
                self.assertGreaterEqual(scores['model_delta_t_c'], 0)

    def test_registry_changed_mid_read(self):
        with self.assertRaisesRegex(DataError, 'Registry updated'):
            measurements_snapshot(self.surry, 'stale')

    def test_missing_corrupt_and_foreign_export(self):
        measured, _ = measurements_snapshot(self.calvert, self.token)
        entry = deepcopy(self.calvert)
        entry['evaluation']['results_sha256'] = 'wrong'
        with self.assertRaisesRegex(DataError, 'Result hash'):
            verified_results(entry, measured, self.token)
        entry = deepcopy(self.calvert)
        entry['results_path'] = 'data/results.csv'
        with self.assertRaisesRegex(DataError, 'destination'):
            verified_results(entry, measured, self.token)
        with patch('multistation_loader.sha256', side_effect=FileNotFoundError('temporarily missing')):
            with self.assertRaises(FileNotFoundError):
                verified_results(self.calvert, measured, self.token)

    def test_result_replaced_during_read(self):
        measured, _ = measurements_snapshot(self.calvert, self.token)
        from multistation_loader import sha256
        counts = {}
        def changing_hash(path):
            text = str(path)
            counts[text] = counts.get(text, 0) + 1
            return 'changed' if text.endswith('results.csv') and counts[text] > 1 else sha256(path)
        with patch('multistation_loader.sha256', side_effect=changing_hash):
            with self.assertRaisesRegex(DataError, 'changed during'):
                verified_results(self.calvert, measured, self.token)

    def test_incomplete_export_withholds_comparison(self):
        measured, _ = measurements_snapshot(self.calvert, self.token)
        with patch('multistation_loader.load_results', return_value=(None, ['2024-01'])):
            with self.assertRaisesRegex(DataError, 'Incomplete export'):
                verified_results(self.calvert, measured, self.token)


class ScreenTests(unittest.TestCase):
    def setUp(self):
        if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':
            def nonrunning_loop():
                loop = MagicMock(spec=asyncio.AbstractEventLoop)
                loop.is_closed.return_value = False
                return loop
            factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop',
                            side_effect=nonrunning_loop)
            factory.start()
            self.addCleanup(factory.stop)

    def screen(self, overrides=None):
        from streamlit.testing.v1 import AppTest
        script = f'''
import sys
sys.path.insert(0, {str(ROOT / 'src/ui')!r})
import app
from unittest.mock import patch
real = app.registry_snapshot
def snapshot(root):
    registry, token = real(root)
    for entry in registry['datasets']:
        if entry['plant_id_eia'] == 6011:
            entry.update({overrides or {}!r})
    return registry, token
with patch.object(app, 'registry_snapshot', snapshot):
    app.render()
'''
        screen = AppTest.from_string(script).run(timeout=30)
        screen.toggle(key='technical_details').set_value(True).run(timeout=30)
        self.assertFalse(screen.exception, str(screen.exception))
        return screen

    def switch(self, screen, plant):
        screen.selectbox[0].select(plant).run(timeout=30)
        self.assertFalse(screen.exception, str(screen.exception))
        return screen

    def test_surry_default_switch_system_and_refresh(self):
        screen = self.screen()
        self.assertEqual(screen.selectbox[0].value, 3806)
        self.assertEqual(screen.selectbox[1].value, 'eia_3806_435731')
        self.assertEqual(screen.metric[2].value, '6.67')
        self.assertEqual(screen.metric[3].value, '11.03')
        self.switch(screen, 6011)
        self.assertEqual(screen.selectbox[1].value, 'eia_6011_535953303432')
        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [24]*3)
        self.assertTrue(any('worse' in x.value for x in screen.markdown))
        screen.button[0].click().run(timeout=30)
        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [24]*3)
        self.switch(screen, 3806)
        screen.selectbox[1].select('eia_3806_435732').run(timeout=30)
        self.assertFalse(screen.exception)
        self.assertEqual(len(screen.metric), 0)
        self.assertTrue(any(x.value == 'Model not ready' for x in screen.info))
        screen.selectbox[1].select('eia_3806_435731').run(timeout=30)
        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [22]*3)

    def test_valid_measurements_without_model(self):
        screen = self.switch(self.screen({'model_status': 'not_trained', 'results_path': None}), 6011)
        self.assertEqual(len(screen.metric), 3)
        self.assertTrue(any(x.value == 'Model not ready' for x in screen.info))
        self.assertEqual(len(screen.dataframe), 0)

    def test_refresh_observes_newly_published_model(self):
        from streamlit.testing.v1 import AppTest
        script = f'''
import sys
sys.path.insert(0, {str(ROOT / 'src/ui')!r})
import app
import streamlit as st
from unittest.mock import patch
real = app.registry_snapshot
def snapshot(root):
    registry, token = real(root)
    if not st.session_state.get('fixture_published', False):
        for entry in registry['datasets']:
            if entry['plant_id_eia'] == 6011:
                entry.update(model_status='not_trained', results_path=None)
    return registry, token
with patch.object(app, 'registry_snapshot', snapshot):
    app.render()
'''
        screen = AppTest.from_string(script).run(timeout=30)
        screen.toggle(key='technical_details').set_value(True).run(timeout=30)
        self.switch(screen, 6011)
        self.assertEqual(len(screen.metric), 3)
        self.assertEqual(len(screen.dataframe), 0)
        screen.session_state['fixture_published'] = True
        screen.button[0].click().run(timeout=30)
        self.assertFalse(screen.exception)
        self.assertEqual(len(screen.metric), 5)
        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [24]*3)

    def test_each_restricted_status(self):
        registry, _ = registry_snapshot()
        for status in ['review_required', 'blocked', 'reference_only', 'measurements_only']:
            entry = next(e for e in registry['datasets'] if e['status'] == status)
            with self.subTest(status=status):
                screen = self.switch(self.screen(), entry['plant_id_eia'])
                screen.selectbox[1].select(entry['dataset_id']).run(timeout=30)
                self.assertFalse(screen.exception, str(screen.exception))
                self.assertTrue(any(x.value == 'Model not ready' for x in screen.info))
                if status != 'measurements_only':
                    self.assertEqual(len(screen.metric), 0)
                if status == 'review_required':
                    self.assertTrue(any('Data review required' in x.value for x in screen.error))

    def test_corrupt_model_graceful(self):
        screen = self.screen()
        from streamlit.testing.v1 import AppTest
        script = f'''
import sys
sys.path.insert(0, {str(ROOT / 'src/ui')!r})
from unittest.mock import patch
import app
with patch.object(app, 'verified_results', side_effect=FileNotFoundError('updating')):
    app.render()
'''
        screen = AppTest.from_string(script).run(timeout=30)
        screen.toggle(key='technical_details').set_value(True).run(timeout=30)
        self.assertFalse(screen.exception)
        self.assertEqual(len(screen.metric), 3)
        self.assertTrue(any('temporarily unavailable' in x.value for x in screen.warning))


if __name__ == '__main__':
    unittest.main()
