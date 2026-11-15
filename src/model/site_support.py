"""Read-only data for drop journeys, month ribbons, evidence cards and catalogs."""
from copy import deepcopy
from datetime import date
import hashlib
import importlib
import json
from pathlib import Path
import sys

import pandas as pd

from .datasets import load_observations
from .environment_report import load_evidence, validate_claim, read_report
from .registry import REGISTRY_PATH, project_path, read_registry, sha256

CONTENT = 'src/model/site_support_data'
AI_ROLE = ('Ridge estimates the temperature difference across a cooling system for a completed month. '
           'Environmental reports use reviewed sources and rules, not a trained environmental-safety model.')
ERRORS = (OSError, ValueError, KeyError, TypeError, ImportError)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def catalog_version(dependencies):
    return hashlib.sha256(json.dumps(dependencies, sort_keys=True).encode('utf-8')).hexdigest()


def read_catalog(root, relative_path='data/site_support/v1/catalog.json'):
    """A saved catalog is usable only while all checked files/absences still match."""
    catalog = json.loads(project_path(root, relative_path).read_text(encoding='utf-8'))
    require(catalog['schema_version'] == 1, 'Unsupported catalog version')
    require(catalog_version(catalog['dependencies']) == catalog['catalog_version'], 'Catalog version mismatch')
    for name, expected in catalog['dependencies'].items():
        path = project_path(root, name)
        actual = sha256(path) if path.is_file() else None
        require(actual == expected, 'Catalog is stale; rebuild without training: ' + name)
    return catalog


def existing_readers():
    """Reuse pure read-only UI adapters; never import app.py or Streamlit."""
    ui = str(Path(__file__).resolve().parents[1] / 'ui')
    if ui not in sys.path:
        sys.path.insert(0, ui)
    return (importlib.import_module('src.ui.multistation_loader'),
            importlib.import_module('src.ui.environment_loader'))


class SiteSupport:
    """One request/refresh snapshot. Do not retain this object in a global UI cache."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.version = sha256(project_path(self.root, REGISTRY_PATH))
        registry = read_registry(self.root, verify=False)
        self.entries = {entry['dataset_id']: entry for entry in registry['datasets']}
        self.frames = {}
        self._stable()

    def _stable(self):
        require(sha256(project_path(self.root, REGISTRY_PATH)) == self.version,
                'Registry changed; start a fresh request')

    def _entry(self, identifier):
        self._stable()
        require(identifier in self.entries, 'Unknown dataset_id; no fallback system')
        return self.entries[identifier]

    def _base(self, entry=None):
        self._stable()
        result = {'schema_version': 1, 'registry_version': self.version}
        if entry:
            result.update({key: entry[key] for key in ('dataset_id', 'plant_id_eia', 'plant_name', 'cooling_id_eia')})
        return result

    def _frame(self, entry):
        require(entry['provenance']['source_units'] == 'degF' and entry['provenance']['units'] == 'degC',
                'Source units need review; do not infer units from values')
        for metadata, path_key, hash_key in [(entry['observations'], 'path', 'sha256'),
                                             (entry['provenance'], 'raw_path', 'raw_sha256')]:
            require(sha256(project_path(self.root, metadata[path_key])) == metadata[hash_key], 'Source hash changed')
        identifier = entry['dataset_id']
        if identifier not in self.frames:
            self.frames[identifier] = load_observations(self.root, entry)
        self._stable()
        return self.frames[identifier]

    def timeline(self, identifier):
        entry = self._entry(identifier)
        payload = {**self._base(entry), 'units': 'degC', 'source_units': 'degF',
                   'kind': 'reported_measurement', 'data_status': entry['status'],
                   'limitations': entry['limitations'], 'calendar_period': ['2010-01', '2025-12']}
        try:
            frame = self._frame(entry).set_index('report_month')
        except ERRORS as exc:
            return {**payload, 'state': 'source_unavailable', 'rows': [], 'reason': str(exc)}
        rows = []
        for month in pd.period_range('2010-01', '2025-12', freq='M').astype(str):
            row = {'report_month': month, 'intake_temperature_c': None, 'discharge_temperature_c': None,
                   'delta_t_c': None, 'record_present': month in frame.index, 'eligible_measured': False,
                   'pair_available': False, 'source_method': None, 'status': 'missing_month',
                   'reasons': ['No source record for this month'], 'kind': 'reported_measurement'}
            if row['record_present']:
                source = frame.loc[month]
                row.update(eligible_measured=bool(source.eligible_measured), pair_available=bool(source.pair_available),
                           source_method=str(source.temperature_method), reasons=[])
                if entry['status'] in {'review_required', 'blocked', 'reference_only'}:
                    row['status'] = 'review_required' if entry['status'] == 'review_required' else 'blocked'
                    row['reasons'] = entry['limitations'] + entry.get('review_months', {}).get(month, [])
                elif not source.pair_available:
                    row.update(status='missing_temperatures', reasons=['Incomplete or nonfinite source temperature pair'])
                elif not source.eligible_measured:
                    row.update(status='excluded_method', reasons=['Source method is not an explicitly measured thermometer method'])
                else:
                    row['status'] = 'verified_measurement'
                    for field in ('intake_temperature_c', 'discharge_temperature_c', 'delta_t_c'):
                        row[field] = float(source[field])
            rows.append(row)
        self._stable()
        return {**payload, 'state': 'available', 'rows': rows}

    def predictions(self, identifier):
        entry = self._entry(identifier)
        payload = {**self._base(entry), 'kind': 'model_estimate', 'units': 'degC', 'rows': [],
                   'label': 'Saved retrospective estimates, not measured temperatures'}
        if entry['status'] != 'ready_for_model_check' or entry['model_status'] not in {'existing_verified', 'evaluated_verified'}:
            return {**payload, 'state': 'model_not_ready'}
        try:
            frame = self._frame(entry)
            measured = frame.loc[frame.eligible_measured].copy()
            measured['reported_delta_t_c'] = measured.delta_t_c
            verifier, _ = existing_readers()
            result, scores = verifier.verified_results(entry, measured, self.version, self.root)
            fields = ('model_delta_t_c', 'median_baseline_delta_t_c', 'seasonal_baseline_delta_t_c')
            payload['rows'] = [{'report_month': month, 'kind': 'model_estimate',
                                **{field: float(row[field]) for field in fields}} for month, row in result.iterrows()]
            payload.update(mae_c=scores, test_n=len(result))
        except ERRORS as exc:
            return {**payload, 'state': 'results_unavailable', 'rows': [], 'reason': str(exc)}
        self._stable()
        return {**payload, 'state': 'verified'}

    def _content(self):
        index = json.loads(project_path(self.root, CONTENT + '/review.json').read_text(encoding='utf-8'))
        for name, expected in index['sha256'].items():
            require(sha256(project_path(self.root, CONTENT + '/' + name)) == expected, 'Story content changed since review')
        return {name: json.loads(project_path(self.root, CONTENT + '/' + name).read_text(encoding='utf-8'))
                for name in index['sha256']}

    def journey(self, identifier):
        entry = self._entry(identifier)
        content = self._content()['journey.json']
        codes = set(entry['cooling_types'])
        family = next((key for key, allowed in content['families'].items() if codes and codes <= set(allowed)), 'unknown')
        mode = 'general_educational' if family == 'unknown' else 'historical_reported_family'
        steps = deepcopy(content['steps'][family])
        for step in steps:
            step['confirmed_for_system'] = (f"Historical registry codes {', '.join(sorted(codes))} report this cooling family. "
                                            'This is not a current pipe map.' if family != 'unknown'
                                            else 'The cooling-system type is not established for this explanation.')
            step['sources'].append({'title': 'Selected-system registry provenance',
                                    'url': entry['provenance']['source_url'], 'role': 'official_statistics',
                                    'locator': entry['dataset_id'] + ' / cooling_types', 'period': entry['period']})
        if entry['plant_id_eia'] == 3806 and family == 'once_through':
            for step in steps:
                step['site_context'] = content['surry_site_context'][step['id']]
        self._stable()
        return {**self._base(entry), 'cooling_family': family, 'scheme_mode': mode,
                'cooling_type_codes': sorted(codes), 'period': entry['period'], 'steps': steps,
                'limitations': content['limitations'], 'ai_role': AI_ROLE}

    def claim_details(self, plant_id, cooling_id=None):
        require(type(plant_id) is int, 'Use an integer plant ID')
        systems = [entry for entry in self.entries.values() if entry['plant_id_eia'] == plant_id]
        require(bool(systems), 'Unknown plant ID')
        if cooling_id is not None:
            require(any(e['cooling_id_eia'] == cooling_id for e in systems), 'Cooling system belongs to another plant')
        _, reader = existing_readers()
        snapshot = reader.report_snapshot(plant_id, self.root)
        base = {**self._base(), 'plant_id_eia': plant_id, 'cooling_id_eia': cooling_id,
                'report_state': snapshot.state, 'statements': [], 'omitted_system_statement_ids': []}
        if snapshot.state != 'ready':
            return base
        try:
            sources, ledger = load_evidence(self.root)
            public, technical = snapshot.report, snapshot.technical
            approved = {c['id']: c for c in ledger['claims'] if c['review_status'] == 'reviewed_for_support'}
            for claim in technical['accepted_claims']:
                require(claim == approved.get(claim['id']), 'Published claim differs from reviewed ledger')
                validate_claim(claim, sources, plant_id, date.today())
            bundle = self._content()['claim_links.json'][str(plant_id)]
            directory = project_path(self.root, f'data/environment_reports/v1/eia_{plant_id}')
            require(sha256(directory / 'report.en.json') == bundle['report_sha256'], 'Claim annotations need review for new report')
            require(technical['review_index_sha256'] == bundle['evidence_index_sha256'], 'Evidence review version changed')
            targets = {'summary': [public['summary']], **{s['id']: s['paragraphs'] for s in public['sections']}}
            coverage = {(key, i): set() for key, texts in targets.items() for i in range(len(texts))}
            identifiers = set()
            for card in bundle['statements']:
                require(card['statement_id'] not in identifiers, 'Duplicate statement ID')
                identifiers.add(card['statement_id'])
                target = targets[card['target']][card['paragraph_index']]
                start, end = card['span']
                require(0 <= start < end <= len(target) and target[start:end] == card['display_span'], 'Statement span mismatch')
                covered = coverage[(card['target'], card['paragraph_index'])]
                require(not covered.intersection(range(start, end)), 'Overlapping statement annotations')
                covered.update(range(start, end))
                require(bool(card['limitation']) and bool(card['review_basis']), 'Statement lacks review boundary')
                require(card['text_role'] in {'source_fact', 'scope_limit', 'evidence_gap', 'method_explanation'}, 'Unknown text role')
                require(card['text_role'] != 'source_fact' or bool(card['sources'] and card['parent_claim_ids']),
                        'Factual statement lacks evidence')
                for parent in card['parent_claim_ids']:
                    require(parent in approved and approved[parent]['plant_id_eia'] == plant_id, 'Unsupported parent claim')
                for ref in card['sources']:
                    require(ref['source_id'] in sources and sources[ref['source_id']]['access_state'] == 'reviewed_content', 'Unreviewed card source')
                    require(ref['url'] == sources[ref['source_id']]['url'] and ref['role'] == sources[ref['source_id']]['role'],
                            'Source URL or role differs from reviewed source')
                    require(any(ref['source_id'] == item['source_id'] and ref['locator'] == item['locator']
                                for parent in card['parent_claim_ids'] for item in approved[parent]['references']), 'Citation does not support this span')
                scope = card['scope']
                require(scope['plant_id_eia'] == plant_id, 'Statement scope belongs to another plant')
                if cooling_id and scope['level'] == 'system' and scope['cooling_id_eia'] != cooling_id:
                    base['omitted_system_statement_ids'].append(card['statement_id'])
                else:
                    base['statements'].append(deepcopy(card))
            for (key, i), positions in coverage.items():
                require(all(j in positions or character.isspace() for j, character in enumerate(targets[key][i])),
                        'A displayed phrase has no evidence or explicit review-boundary annotation')
            require(sha256(directory / 'ready.json') == snapshot.version, 'Report changed during request')
        except ERRORS as exc:
            return {**base, 'report_state': 'review_required', 'statements': [], 'reason': str(exc)}
        self._stable()
        return base

    def catalog(self):
        dependencies = self._dependencies()
        systems = []
        for entry in self.entries.values():
            timeline = self.timeline(entry['dataset_id'])
            predictions = self.predictions(entry['dataset_id'])
            count = sum(row['status'] == 'verified_measurement' for row in timeline['rows'])
            systems.append({**self._base(entry), 'data_status': entry['status'],
                            'has_verified_measurements': count > 0, 'verified_measurement_months': count,
                            'has_verified_model_results': predictions['state'] == 'verified',
                            'model_result_months': predictions.get('test_n', 0),
                            'requires_review': entry['status'] == 'review_required' or timeline['state'] == 'source_unavailable'
                                               or predictions['state'] == 'results_unavailable',
                            'data_blocked': entry['status'] == 'blocked', 'no_temperature_pairs': entry['status'] == 'reference_only',
                            'measurement_state': timeline['state'], 'model_state': predictions['state'],
                            'limitations': entry['limitations']})
        _, reader = existing_readers()
        plants = []
        for plant_id in sorted({entry['plant_id_eia'] for entry in self.entries.values()}):
            entries = [entry for entry in systems if entry['plant_id_eia'] == plant_id]
            report = reader.report_snapshot(plant_id, self.root)
            details = self.claim_details(plant_id) if report.state == 'ready' else None
            substantive = bool(details and details['report_state'] == 'ready' and any(
                c['kind'] in {'observation', 'model_estimate'} for c in report.technical['accepted_claims']))
            plants.append({'plant_id_eia': plant_id, 'plant_name': entries[0]['plant_name'],
                           'has_substantive_environment_report': substantive,
                           'has_insufficient_evidence_report': report.state == 'insufficient_evidence',
                           'report_state': details['report_state'] if details else report.state,
                           'expert_review_status': 'not_performed',
                           'system_count': len(entries),
                           **{'any_system_' + flag: any(e[flag] for e in entries) for flag in
                              ('has_verified_measurements', 'has_verified_model_results', 'requires_review', 'data_blocked')},
                           'verified_measurement_systems': sum(e['has_verified_measurements'] for e in entries),
                           'verified_model_systems': sum(e['has_verified_model_results'] for e in entries)})
        require(self._dependencies() == dependencies, 'Catalog inputs changed during verification; retry')
        return {**self._base(), 'plants': plants, 'systems': systems, 'ai_role': AI_ROLE,
                'dependencies': dependencies, 'catalog_version': catalog_version(dependencies)}

    def _dependencies(self):
        names = {REGISTRY_PATH, 'src/model/site_support.py', 'src/model/environment_report.py',
                 'src/model/datasets.py', 'src/model/registry.py', 'src/ui/multistation_loader.py',
                 'src/ui/environment_loader.py', 'src/ui/data_loader.py',
                 CONTENT + '/review.json', CONTENT + '/claim_links.json', CONTENT + '/journey.json'}
        names.update('src/model/environment_evidence/' + name for name in
                     ['review_index.json', 'claims.json', 'source_catalog.json', 'technical_values.json'])
        for entry in self.entries.values():
            names.update([entry['observations']['path'], entry['provenance']['raw_path']])
            if entry['results_path']:
                names.update([entry['results_path'], entry['artifacts']['future_artifacts_dir'] + '/metrics.json'])
                if entry.get('evaluation'):
                    names.add(entry['evaluation']['verification_path'])
            names.update(f"data/environment_reports/v1/eia_{entry['plant_id_eia']}/{name}" for name in
                         ['ready.json', 'report.en.json', 'report.en.md', 'technical.json'])
        return {name: sha256(project_path(self.root, name)) if project_path(self.root, name).is_file() else None
                for name in sorted(names)}
