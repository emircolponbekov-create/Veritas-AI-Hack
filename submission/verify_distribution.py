"""Read-only integrity and saved-result checks; never trains or repairs files."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def local_path(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f'Path outside project: {relative}')
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_integrity():
    registry = json.loads(local_path('data/model_artifacts/multistation/registry.json').read_text(encoding='utf-8'))
    errors = []
    sources = {}
    checks = 0
    for entry in registry['datasets']:
        source = entry['observations']
        expected = source['sha256']
        if source['path'] in sources and sources[source['path']] != expected:
            errors.append(f'Conflicting source hashes: {source["path"]}')
        sources[source['path']] = expected
        required = [entry['artifacts']['audit_path']]
        if entry.get('results_path'):
            required.append(entry['results_path'])
        for name in required:
            if not local_path(name).is_file():
                errors.append(f'Missing registered file: {name}')
    for name, expected in sources.items():
        path = local_path(name)
        checks += 1
        if not path.is_file() or digest(path) != expected:
            errors.append(f'Source hash mismatch: {name}')
    manifests = [
        'src/model/environment_evidence/review_index.json',
        'src/model/site_support_data/review.json',
        'data/environment_reports/v1/eia_3806/ready.json',
        'data/environment_reports/v1/eia_6011/ready.json',
    ]
    for name in manifests:
        path = local_path(name)
        manifest = json.loads(path.read_text(encoding='utf-8'))
        for filename, expected in manifest['sha256'].items():
            target = local_path((path.parent / filename).relative_to(ROOT))
            checks += 1
            if not target.is_file() or digest(target) != expected:
                errors.append(f'Review/publication hash mismatch: {target.relative_to(ROOT)}')
    notebook = json.loads(local_path('submission/RESULTS_REVIEW.ipynb').read_text(encoding='utf-8'))
    outputs = [o for c in notebook['cells'] for o in c.get('outputs', [])]
    if not outputs or any(o.get('output_type') == 'error' for o in outputs):
        errors.append('Review notebook has absent outputs or saved errors')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'PASS: {len(registry["datasets"])} registered systems; {checks} source/evidence hashes; notebook outputs present without errors.')


def check_saved_results():
    sys.path.insert(0, str(ROOT / 'src/ui'))
    from multistation_loader import registry_snapshot, measurements_snapshot, verified_results
    registry, token = registry_snapshot(ROOT)
    evaluated = 0
    improved = 0
    for entry in registry['datasets']:
        if entry['status'] != 'ready_for_model_check' or entry['model_status'] not in {'existing_verified', 'evaluated_verified'}:
            continue
        measurements, _ = measurements_snapshot(entry, token, ROOT)
        results, scores = verified_results(entry, measurements, token, ROOT)
        if len(results) != entry['split_counts']['test']:
            raise ValueError(f'Test count differs: {entry["dataset_id"]}')
        evaluated += 1
        improved += scores['model_delta_t_c'] < min(scores['median_baseline_delta_t_c'], scores['seasonal_baseline_delta_t_c'])
    if (evaluated, improved) != (17, 4):
        raise ValueError(f'Unexpected saved results: evaluated={evaluated}, improved={improved}')
    print('PASS: all 17 saved model comparisons verified; Ridge beats the better baseline in 4 and is worse in 13. No training.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', action='store_true', help='Also verify saved exports and MAE; requires requirements.txt.')
    args = parser.parse_args()
    try:
        check_integrity()
        if args.results:
            check_saved_results()
    except (ValueError, OSError, KeyError, ImportError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        print('Use the original repository bytes. Do not regenerate manifests or retrain models to hide a mismatch.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
