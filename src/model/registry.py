"""Read dataset metadata without importing or executing the ML pipeline."""
from pathlib import Path
import hashlib
import json

REGISTRY_PATH = 'data/model_artifacts/multistation/registry.json'
STATUSES = {'ready_for_model_check', 'review_required', 'measurements_only',
            'blocked', 'reference_only'}


def dataset_id(plant_id, system_id):
    return f'eia_{int(plant_id)}_{str(system_id).encode("utf-8").hex()}'


def project_path(root, relative):
    root = Path(root).resolve()
    text = str(relative)
    path = Path(text)
    if path.is_absolute() or ':' in text or '\\' in text or '..' in path.parts:
        raise ValueError(f'Not a safe relative project path: {relative}')
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f'Path escapes project: {relative}')
    return resolved


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_registry(root, verify=True):
    root = Path(root).resolve()
    data = json.loads(project_path(root, REGISTRY_PATH).read_text(encoding='utf-8'))
    if data.get('schema_version') != 2:
        raise ValueError('Unsupported dataset registry version')
    seen = set()
    outputs = set()
    checked = {}
    for entry in data['datasets']:
        expected = dataset_id(entry['plant_id_eia'], entry['cooling_id_eia'])
        if entry['dataset_id'] != expected or expected in seen:
            raise ValueError('Dataset identity collision or mismatch')
        seen.add(expected)
        if entry['status'] not in STATUSES:
            raise ValueError('Unknown dataset status')
        for name in ['audit_path', 'future_results_path', 'future_artifacts_dir']:
            project_path(root, entry['artifacts'][name])
        result_destination = entry['artifacts']['future_results_path']
        if result_destination in outputs:
            raise ValueError('Two systems share a result destination')
        outputs.add(result_destination)
        if entry['model_status']=='not_trained' and entry['results_path'] is not None:
            raise ValueError('Untrained dataset cannot advertise a result')
        if entry['results_path'] is not None:
            project_path(root, entry['results_path'])
        source = entry['observations']
        selector = source['selector']
        if source['format'] not in {'csv', 'parquet'}:
            raise ValueError('Unsupported observation format')
        if (selector['plant_id_eia'], selector['cooling_id_eia']) != (entry['plant_id_eia'], entry['cooling_id_eia']):
            raise ValueError('Source selector identity mismatch')
        if (selector['year_min'], selector['year_max']) != (2010,2025):
            raise ValueError('Source selector changes fixed date boundaries')
        path = project_path(root, source['path'])
        if verify:
            if str(path) not in checked:
                checked[str(path)] = sha256(path)
            if checked[str(path)] != source['sha256']:
                raise ValueError(f'Input hash mismatch: {source["path"]}')
    return data


def find_dataset(root, identifier):
    matches = [e for e in read_registry(root)['datasets'] if e['dataset_id'] == identifier]
    if len(matches) != 1:
        raise ValueError(f'Unknown dataset_id: {identifier}')
    return matches[0]
