"""Evidence gates and identity tests; no fitting, UI changes or network required."""
from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.model.environment_report import (generate_report, validate_claim, load_evidence,
                                          markdown, export_report, read_report)


class EvidenceReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, cls.ledger = load_evidence(ROOT)
        cls.report, cls.technical = generate_report(ROOT, 3806, date(2026, 11, 15))

    def test_actual_water_claim_and_plain_body(self):
        self.assertEqual(self.technical['local_checks']['water']['eligible_months'], 188)
        self.assertEqual(self.report['status'], 'partial_evidence')
        self.assertEqual(self.report['expert_review_status'], 'not_performed')
        body = self.report['summary'] + ' '.join(' '.join(s['paragraphs']) for s in self.report['sections'])
        self.assertTrue(300 <= len(body.split()) <= 500)
        for term in ['ΔT =', 'MAE', 'Ridge', 'eligible_measured', 'pCi/L', '121171']:
            self.assertNotIn(term, markdown(self.report))
        self.assertNotIn('rejected_safety', str(self.report))
        self.assertEqual(len(self.technical['omitted_claims']), 2)

    def test_station_switch_refuses_unsupported_inference(self):
        other, audit = generate_report(ROOT, 6011)
        self.assertEqual(other['status'], 'insufficient_evidence')
        self.assertEqual(audit['accepted_claims'], [])
        self.assertNotIn('Surry', markdown(other))
        self.assertFalse(any(section['references'] for section in other['sections']))
        again, _ = generate_report(ROOT, 3806, date(2026, 11, 15))
        self.assertEqual(again, self.report)
        with self.assertRaisesRegex(ValueError, 'not in project registry'):
            generate_report(ROOT, 999999)

    def test_wrong_station_and_general_source_gates(self):
        claim = deepcopy(self.ledger['claims'][0])
        with self.assertRaisesRegex(ValueError, 'another station'):
            validate_claim(claim, self.sources, 6011, date(2026, 11, 15))
        context = deepcopy(next(c for c in self.ledger['claims'] if c['id'] == 'ipcc_context'))
        context['kind'] = 'observation'
        with self.assertRaisesRegex(ValueError, 'General source'):
            validate_claim(context, self.sources, 3806, date(2026, 11, 15))

    def test_link_only_unread_and_future_evidence_rejected(self):
        valid = deepcopy(self.ledger['claims'][0])
        for field, value in [('review_status', 'not_reviewed'), ('reviewed_on', '2027-01-01')]:
            claim = deepcopy(valid)
            claim[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_claim(claim, self.sources, 3806, date(2026, 11, 15))
        claim = deepcopy(valid)
        claim['references'][0]['support_note'] = ''
        with self.assertRaisesRegex(ValueError, 'support location'):
            validate_claim(claim, self.sources, 3806, date(2026, 11, 15))
        sources = deepcopy(self.sources)
        sources['eia_surry_cw1']['access_state'] = 'link_only'
        with self.assertRaisesRegex(ValueError, 'not reviewed'):
            validate_claim(valid, sources, 3806, date(2026, 11, 15))

    def test_operator_attribution_and_conflict_gates(self):
        claim = deepcopy(next(c for c in self.ledger['claims'] if c['id'] == 'epa_fish'))
        claim['operator_attributed'] = False
        with self.assertRaisesRegex(ValueError, 'attribution'):
            validate_claim(claim, self.sources, 3806, date(2026, 11, 15))
        claim['operator_attributed'] = True
        claim['conflict_state'] = 'unresolved'
        with self.assertRaisesRegex(ValueError, 'Unresolved conflict'):
            validate_claim(claim, self.sources, 3806, date(2026, 11, 15))
        self.assertIn('different outcome', markdown(self.report))

    def test_scenario_needs_label(self):
        claim = deepcopy(self.ledger['claims'][0])
        claim['kind'] = 'scenario'
        with self.assertRaisesRegex(ValueError, 'Scenario disguised'):
            validate_claim(claim, self.sources, 3806, date(2026, 11, 15))

    def test_curated_file_tampering_invalidates_review(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'src/model/environment_evidence'
            shutil.copytree(ROOT / 'src/model/environment_evidence', target)
            with (target / 'claims.json').open('a', encoding='utf-8') as stream:
                stream.write(' ')
            with self.assertRaisesRegex(ValueError, 'changed since support review'):
                load_evidence(directory)

    def test_publication_identity_integrity_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'report'
            export_report(self.report, self.technical, target)
            self.assertEqual(read_report(target, 3806), self.report)
            with self.assertRaisesRegex(ValueError, 'another station'):
                read_report(target, 6011)
            with self.assertRaises(FileExistsError):
                export_report(self.report, self.technical, target)
            (target / 'report.en.md').write_text('changed', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'changed or incomplete'):
                read_report(target, 3806)

    def test_without_ready_manifest_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                read_report(directory, 3806)

    def test_no_network_or_training_import(self):
        with patch('socket.create_connection', side_effect=AssertionError('No network')):
            generate_report(ROOT, 3806)
        self.assertNotIn('sklearn', sys.modules)
        self.assertNotIn('src.model.model', sys.modules)


if __name__ == '__main__':
    unittest.main()
