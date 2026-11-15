"""Offline, curated evidence reports; neither a safety classifier nor a training job."""
import argparse
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path

from .registry import project_path, read_registry

EVIDENCE = 'src/model/environment_evidence'
SECTIONS = ('water', 'animals_plants', 'people', 'climate', 'unknowns')
TITLES = dict(zip(SECTIONS, ('Water', 'Animals and plants', 'People', 'Climate', 'What remains unknown')))
KINDS = {'observation', 'model_estimate', 'scenario', 'general_context'}
MISSING = 'Insufficient evidence for this station to draw a conclusion.'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_evidence(root):
    directory = project_path(root, EVIDENCE)
    index = json.loads((directory / 'review_index.json').read_text(encoding='utf-8'))
    for name, expected in index['sha256'].items():
        require(digest(project_path(root, EVIDENCE + '/' + name)) == expected,
                'Evidence changed since support review: ' + name)
    catalog = json.loads((directory / 'source_catalog.json').read_text(encoding='utf-8'))
    ledger = json.loads((directory / 'claims.json').read_text(encoding='utf-8'))
    require(ledger['schema_version'] == 1, 'Unsupported evidence schema')
    identifiers = [claim['id'] for claim in ledger['claims']]
    require(len(identifiers) == len(set(identifiers)), 'Duplicate claim identifiers')
    return catalog, ledger


def validate_claim(claim, sources, plant_id, as_of):
    require(claim['plant_id_eia'] == plant_id, 'Claim belongs to another station')
    require(claim['kind'] in KINDS, 'Unknown evidence kind')
    require(claim['section'] in SECTIONS, 'Unknown report section')
    require(claim['review_status'] == 'reviewed_for_support', 'Claim has not passed support review')
    require(bool(claim['support_review']) and bool(claim['limitations']), 'Review or limitations missing')
    require(date.fromisoformat(claim['reviewed_on']) <= as_of, 'Future review date')
    require(claim['conflict_state'] in {'none_identified', 'different_endpoint', 'unresolved'}, 'Unknown conflict state')
    require(claim['conflict_state'] != 'unresolved' or bool(claim['conflict_note']), 'Unexplained conflict')
    require(claim['conflict_state'] != 'unresolved', 'Unresolved conflict: adjudication required before publication')
    require(bool(claim['references']), 'A link alone is not supporting evidence')
    require(bool(claim['geography']) and bool(claim['period']['label']), 'Missing place or period')
    for bound in ('start', 'end'):
        value = claim['period'].get(bound)
        require(value is None or date.fromisoformat(value) <= as_of, 'Future observation period')
    if claim['period'].get('start') and claim['period'].get('end'):
        require(claim['period']['start'] <= claim['period']['end'], 'Reversed period')
    for reference in claim['references']:
        source = sources[reference['source_id']]
        require(source['access_state'] == 'reviewed_content', 'Source contents not reviewed')
        require(source['scope'] == 'general' or plant_id in source['plant_ids'], 'Source belongs to another station')
        require(source['scope'] != 'general' or claim['kind'] == 'general_context', 'General source cannot prove site impact')
        require(bool(reference['locator']) and bool(reference['support_note']), 'Missing exact support location')
        require(bool(reference['public_locator']), 'Missing plain-language citation label')
        require(source['role'] != 'operator' or claim['operator_attributed'], 'Operator statement needs attribution')
    require(claim['kind'] != 'scenario' or claim['scenario_labelled'], 'Scenario disguised as observation')


def check_local_water(root, sources, plant_id):
    from .datasets import load_observations
    entries = read_registry(root, verify=False)['datasets']
    entry = next(e for e in entries if e['plant_id_eia'] == plant_id and e['cooling_id_eia'] == 'CW1')
    source = sources['eia_surry_cw1']
    require(entry['observations']['sha256'] == source['local_sha256'], 'Frozen water source changed')
    frame = load_observations(root, entry)
    measured = frame.loc[frame.eligible_measured]
    require(len(measured) == 188 and measured.delta_t_c.gt(0).all(), 'Water claim no longer matches observations')
    return {'system': 'CW1', 'source_rows': len(frame), 'eligible_months': len(measured),
            'start': measured.report_month.min(), 'end': measured.report_month.max(),
            'min_delta_c': float(measured.delta_t_c.min()), 'max_delta_c': float(measured.delta_t_c.max()),
            'note': 'Source-reported monthly means, not receiving-water warming; no Ridge invocation.'}


def generate_report(root, plant_id, as_of=None):
    as_of = as_of or date.today()
    require(type(plant_id) is int, 'Use an integer EIA plant ID')
    registry = read_registry(root, verify=False)
    entries = [e for e in registry['datasets'] if e['plant_id_eia'] == plant_id]
    require(bool(entries), 'Station not in project registry; no fallback report')
    sources, ledger = load_evidence(root)
    profile = ledger['profiles'].get(str(plant_id))
    name = entries[0]['plant_name']
    claims = [deepcopy(c) for c in ledger['claims'] if c['plant_id_eia'] == plant_id]
    accepted, omitted, audit = [], [], {}
    for claim in claims:
        if claim['review_status'] != 'reviewed_for_support':
            omitted.append({'claim_id': claim['id'], 'reason': claim['review_status']})
            continue
        validate_claim(claim, sources, plant_id, as_of)
        if claim.get('local_water_check'):
            audit['water'] = check_local_water(root, sources, plant_id)
        accepted.append(claim)
    usable = bool(accepted) and profile is not None
    sections = []
    for key in SECTIONS:
        relevant = [c for c in accepted if c['section'] == key]
        state = 'partial_evidence' if relevant else 'insufficient_evidence'
        if relevant and all(c['kind'] == 'general_context' for c in relevant):
            state = 'context_only'
        paragraphs = [c['public_text'] for c in relevant]
        if usable:
            paragraphs.append(profile['section_limits'][key])
        else:
            paragraphs = [MISSING]
        references = []
        for claim in relevant:
            for reference in claim['references']:
                source = sources[reference['source_id']]
                references.append({**reference, 'title': source['title'], 'url': source['url'],
                                   'role': source['role'], 'claim_id': claim['id']})
            if claim['conflict_state'] != 'none_identified':
                paragraphs.append(claim['conflict_note'])
        sections.append({'id': key, 'title': TITLES[key], 'status': state, 'paragraphs': paragraphs,
                         'claim_ids': [c['id'] for c in relevant], 'references': references,
                         'periods': [c['period'] for c in relevant],
                         'limitations': [limit for c in relevant for limit in c['limitations']]})
    report = {'report_version': 1, 'plant_id_eia': plant_id, 'station_name': name, 'language': 'en',
              'status': 'partial_evidence' if usable else 'insufficient_evidence',
              'as_of': as_of.isoformat(), 'period_label': profile['period_label'] if usable else 'No reviewed reporting period available',
              'summary': profile['summary'] if usable else 'No station-specific environmental evidence has been approved in this module. No benefit, harm or safety conclusion is made.',
              'sections': sections, 'expert_review_status': 'not_performed',
              'method': 'curated_evidence_rules_not_trained_safety_model'}
    technical = {'accepted_claims': accepted, 'omitted_claims': omitted, 'local_checks': audit,
                 'review_index_sha256': digest(project_path(root, EVIDENCE + '/review_index.json')),
                 'scope': 'Content support checked by Codex; not independent expert validation. No runtime search, API or fitting.'}
    return report, technical


def markdown(report):
    lines = [f"# {report['station_name']}", '', f"Evidence period: {report['period_label']}", '', report['summary'], '']
    for section in report['sections']:
        lines.extend(['## ' + section['title'], '', *section['paragraphs'], ''])
        seen = set()
        for reference in section['references']:
            key = (reference['url'], reference['locator'])
            if key not in seen:
                lines.extend([f"Source: [{reference['title']}]({reference['url']}) — {reference['public_locator']}.", ''])
                seen.add(key)
    return '\n'.join(lines)


def export_report(report, technical, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    payloads = {'report.en.md': markdown(report),
                'report.en.json': json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                'technical.json': json.dumps(technical, ensure_ascii=False, indent=2) + '\n'}
    for name, content in payloads.items():
        with (destination / name).open('x', encoding='utf-8') as stream:
            stream.write(content)
    ready = {'report_version': 1, 'plant_id_eia': report['plant_id_eia'],
             'sha256': {name: digest(destination / name) for name in payloads}}
    with (destination / 'ready.json').open('x', encoding='utf-8') as stream:
        json.dump(ready, stream, indent=2)


def read_report(directory, expected_plant_id):
    directory = Path(directory)
    publication = digest(directory / 'ready.json')
    ready = json.loads((directory / 'ready.json').read_text(encoding='utf-8'))
    require(ready['plant_id_eia'] == expected_plant_id, 'Report belongs to another station')
    require(set(ready['sha256']) == {'report.en.md', 'report.en.json', 'technical.json'}, 'Incomplete report publication')
    for name, expected in ready['sha256'].items():
        require(digest(directory / name) == expected, 'Report file changed or incomplete')
    report = json.loads((directory / 'report.en.json').read_text(encoding='utf-8'))
    require(report['plant_id_eia'] == expected_plant_id and report['report_version'] == 1, 'Invalid report identity/version')
    require(digest(directory / 'ready.json') == publication, 'Publication changed during reading')
    require(all(digest(directory / name) == expected for name, expected in ready['sha256'].items()),
            'Report files changed during reading')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plant-id', type=int, required=True)
    parser.add_argument('--output', required=True, help='New project-relative output directory')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    report, technical = generate_report(root, args.plant_id)
    export_report(report, technical, project_path(root, args.output))
    print(markdown(report))


if __name__ == '__main__':
    main()
