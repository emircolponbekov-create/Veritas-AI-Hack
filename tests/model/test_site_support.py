"""Scientific scope, identity and read-only data contracts for future UI work."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.model.site_support import SiteSupport, AI_ROLE, read_catalog, catalog_version
from src.model.environment_report import read_report

SURRY = 'eia_3806_435731'
CW2 = 'eia_3806_435732'
CALVERT = 'eia_6011_535953303432'


class StorySupportTests(unittest.TestCase):
    def setUp(self):
        self.provider = SiteSupport(ROOT)

    def test_actual_calendar_units_and_exclusions(self):
        data = self.provider.timeline(SURRY)
        self.assertEqual(len(data['rows']), 192)
        good = [r for r in data['rows'] if r['status'] == 'verified_measurement']
        self.assertEqual(len(good), 188)
        self.assertEqual((data['source_units'], data['units']), ('degF', 'degC'))
        frame = self.provider._frame(self.provider._entry(SURRY)).set_index('report_month')
        for row in good:
            original = frame.loc[row['report_month']]
            self.assertAlmostEqual(row['intake_temperature_c'], (original.intake_temperature_f - 32) * 5 / 9, places=5)
            self.assertAlmostEqual(row['delta_t_c'], row['discharge_temperature_c'] - row['intake_temperature_c'], places=5)
        excluded = next(r for r in data['rows'] if r['report_month'] == '2024-08')
        self.assertFalse(excluded['eligible_measured'])
        self.assertIsNone(excluded['delta_t_c'])
        self.assertEqual(excluded['status'], 'excluded_method')

    def test_missing_row_and_temperature_not_interpolated(self):
        entry = self.provider._entry(SURRY)
        frame = self.provider._frame(entry).copy()
        frame = frame.loc[frame.report_month.ne('2010-02')].copy()
        index = frame.index[frame.report_month.eq('2010-01')][0]
        frame.loc[index, 'pair_available'] = False
        frame.loc[index, 'eligible_measured'] = False
        with patch.object(self.provider, '_frame', return_value=frame):
            rows = {r['report_month']: r for r in self.provider.timeline(SURRY)['rows']}
        self.assertEqual(rows['2010-02']['status'], 'missing_month')
        self.assertFalse(rows['2010-02']['record_present'])
        self.assertEqual(rows['2010-01']['status'], 'missing_temperatures')
        self.assertIsNone(rows['2010-01']['intake_temperature_c'])

    def test_review_numbers_withheld_and_no_cross_system_model(self):
        data = self.provider.timeline(CW2)
        self.assertTrue(any(row['eligible_measured'] for row in data['rows']))
        self.assertTrue(all(row['delta_t_c'] is None for row in data['rows']))
        self.assertEqual(self.provider.predictions(CW2)['state'], 'model_not_ready')
        for identifier, count in [(SURRY, 22), (CALVERT, 24), (SURRY, 22)]:
            result = self.provider.predictions(identifier)
            self.assertEqual(result['state'], 'verified')
            self.assertEqual(len(result['rows']), count)
            self.assertTrue(all(row['kind'] == 'model_estimate' for row in result['rows']))
            self.assertEqual(result['dataset_id'], identifier)

    def test_unavailable_source_or_result_never_fake(self):
        with patch.object(self.provider, '_frame', side_effect=ValueError('source changed')):
            timeline = self.provider.timeline(SURRY)
            self.assertEqual((timeline['state'], timeline['rows']), ('source_unavailable', []))
            self.assertEqual(self.provider.predictions(SURRY)['state'], 'results_unavailable')
        with self.assertRaisesRegex(ValueError, 'Unknown dataset'):
            self.provider.timeline('eia_3806_fake')

    def test_units_are_not_guessed(self):
        self.provider.entries[SURRY]['provenance']['source_units'] = 'unknown'
        result = self.provider.timeline(SURRY)
        self.assertEqual(result['state'], 'source_unavailable')
        self.assertEqual(result['rows'], [])

    def test_journey_family_and_general_fallback(self):
        path = self.provider.journey(SURRY)
        self.assertEqual(path['cooling_family'], 'once_through')
        self.assertEqual(len(path['steps']), 3)
        self.assertTrue(all(s['site_context']['source']['role'] == 'operator' for s in path['steps']))
        other = self.provider.journey(CALVERT)
        self.assertFalse(any('site_context' in step for step in other['steps']))
        for codes, family in [([], 'unknown'), (['O', 'R'], 'unknown'), (['RC'], 'recirculating')]:
            altered = deepcopy(self.provider._entry(SURRY))
            altered['cooling_types'] = codes
            with patch.object(self.provider, '_entry', return_value=altered):
                data = self.provider.journey(SURRY)
            self.assertEqual(data['cooling_family'], family)
            if family == 'unknown':
                self.assertEqual(data['scheme_mode'], 'general_educational')
            if family == 'recirculating':
                self.assertIn('reuse', data['steps'][2]['general_explanation'])

    def test_atomic_claim_sources_and_system_scope(self):
        data = self.provider.claim_details(3806)
        self.assertEqual(data['report_state'], 'ready')
        self.assertEqual(len(data['statements']), 25)
        cards = {c['statement_id']: c for c in data['statements']}
        h3 = cards['eia_3806.water.tritium_detected']
        self.assertEqual(len(h3['sources']), 1)
        self.assertNotIn('p. 10', h3['sources'][0]['locator'])
        method = cards['eia_3806.water.nondetection_boundary']
        self.assertEqual(method['text_role'], 'method_explanation')
        self.assertIn('p. 10', method['sources'][0]['locator'])
        self.assertEqual(cards['eia_3806.climate.general_lifecycle_context']['scope']['level'], 'general')
        other = self.provider.claim_details(3806, 'CW2')
        self.assertEqual(len(other['omitted_system_statement_ids']), 3)
        self.assertFalse(any(c['scope']['level'] == 'system' for c in other['statements']))
        self.assertEqual(self.provider.claim_details(6011)['statements'], [])
        self.assertEqual(self.provider.claim_details(6014)['report_state'], 'missing')
        with self.assertRaisesRegex(ValueError, 'another plant'):
            self.provider.claim_details(6011, 'CW1')

    def test_bad_link_or_incomplete_span_fails_closed(self):
        for mutation in ['citation', 'span']:
            content = self.provider._content()
            card = content['claim_links.json']['3806']['statements'][0]
            if mutation == 'citation':
                card['sources'][0]['source_id'] = 'operator_legacy'
            else:
                content['claim_links.json']['3806']['statements'].pop()
            with patch.object(self.provider, '_content', return_value=content):
                data = self.provider.claim_details(3806)
            self.assertEqual(data['report_state'], 'review_required')
            self.assertEqual(data['statements'], [])

    def test_existing_report_reader_unchanged_and_registry_refresh(self):
        old = read_report(ROOT / 'data/environment_reports/v1/eia_3806', 3806)
        self.assertEqual(old['report_version'], 1)
        self.provider.claim_details(3806)
        self.assertEqual(read_report(ROOT / 'data/environment_reports/v1/eia_3806', 3806), old)
        self.provider.version = 'outdated'
        with self.assertRaisesRegex(ValueError, 'fresh request'):
            self.provider.timeline(SURRY)
        self.assertIn('not a trained environmental-safety model', AI_ROLE)

    def test_checked_catalog_has_combining_flags(self):
        catalog = read_catalog(ROOT)
        self.assertEqual((len(catalog['plants']), len(catalog['systems'])), (66, 102))
        self.assertEqual(sum(s['has_verified_model_results'] for s in catalog['systems']), 17)
        self.assertEqual(sum(s['has_verified_measurements'] for s in catalog['systems']), 38)
        surry = next(p for p in catalog['plants'] if p['plant_id_eia'] == 3806)
        self.assertTrue(surry['has_substantive_environment_report'])
        self.assertTrue(surry['any_system_requires_review'])
        self.assertEqual(surry['verified_model_systems'], 1)
        calvert = next(p for p in catalog['plants'] if p['plant_id_eia'] == 6011)
        self.assertTrue(calvert['has_insufficient_evidence_report'])
        self.assertTrue(calvert['any_system_has_verified_model_results'])
        self.assertFalse(calvert['has_substantive_environment_report'])

    def test_saved_catalog_not_stale_when_a_report_appears(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            deps = {'new-report.json': None}
            value = {'schema_version': 1, 'dependencies': deps, 'catalog_version': catalog_version(deps)}
            (root / 'catalog.json').write_text(json.dumps(value), encoding='utf-8')
            read_catalog(root, 'catalog.json')
            (root / 'new-report.json').write_text('{}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'stale'):
                read_catalog(root, 'catalog.json')


if __name__ == '__main__':
    unittest.main()
