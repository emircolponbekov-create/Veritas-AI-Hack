"""Read-only UI snapshots using the MODEL registry reader and observation adapter."""
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.model.registry import REGISTRY_PATH, project_path, read_registry, sha256
from src.model.datasets import load_observations
from data_loader import DataError, load_results, require


def registry_snapshot(root=ROOT):
    """No UI cache: each rerun observes an atomic registry version."""
    path = project_path(root, REGISTRY_PATH)
    token = sha256(path)
    registry = read_registry(root, verify=False)
    require(sha256(path) == token, "Registry changed while reading. Refresh data.")
    return registry, token


def current(root, token):
    require(sha256(project_path(root, REGISTRY_PATH)) == token,
            "Registry updated during this read. Refresh data to use the new version.")


def measurements_snapshot(entry, token, root=ROOT):
    """Delegate units, eligibility, raw provenance and identity checks to MODEL."""
    current(root, token)
    frame = load_observations(root, entry)
    current(root, token)
    require(len(frame) == entry['rows'], "Observation count disagrees with registry.")
    selected = frame.loc[frame.eligible_measured].copy()
    require(len(selected) == entry['eligible_rows'], "Eligibility count disagrees with registry.")
    counts = {name: int(selected.split.eq(name).sum()) for name in entry['split_counts']}
    require(counts == entry['split_counts'], "Split counts disagree with registry.")
    selected['reported_delta_t_c'] = selected.delta_t_c
    return selected, {'total': len(frame), 'eligible': len(selected),
                      'excluded': frame.loc[~frame.eligible_measured, 'report_month'].tolist()}


def verified_results(entry, measurements, token, root=ROOT):
    """Verify a complete per-system export, train baselines and saved metrics."""
    require(entry['status'] == 'ready_for_model_check', "Dataset is not cleared for model display.")
    require(entry['model_status'] in {'existing_verified', 'evaluated_verified'}
            and entry['results_path'], "No verified model export is registered.")
    current(root, token)
    require(entry['results_path'] == entry['artifacts']['future_results_path'],
            "Registered result destination disagrees with this system.")
    result_path = project_path(root, entry['results_path'])
    artifact_dir = entry['artifacts']['future_artifacts_dir']
    metrics_path = project_path(root, artifact_dir + '/metrics.json')
    paths = [result_path, metrics_path]
    evaluation = entry.get('evaluation')
    if entry['model_status'] == 'evaluated_verified':
        require(bool(evaluation), "Verified evaluation metadata is missing.")
        require(evaluation['metrics_path'] == artifact_dir + '/metrics.json', "Metrics path mismatch.")
        require(evaluation['verification_path'] == artifact_dir + '/verification.json', "Verification path mismatch.")
        paths.append(project_path(root, evaluation['verification_path']))
    hashes = {path: sha256(path) for path in paths}
    results, missing = load_results(measurements, result_path)
    require(not missing, "Incomplete export: some eligible test months are missing.")
    metrics = json.loads(metrics_path.read_text(encoding='utf-8'))
    require(metrics['input_sha256'] == entry['observations']['sha256'], "Metrics source hash mismatch.")
    require(metrics['test_months'] == results.index.tolist(), "Metrics test months mismatch.")
    require(metrics['split']['test']['n'] == len(results), "Metrics test count mismatch.")
    train = measurements.loc[measurements.split.eq('train')]
    seasonal = train.groupby(train.date.dt.month).reported_delta_t_c.median()
    expected = {'median_baseline_delta_t_c': np.repeat(train.reported_delta_t_c.median(), len(results)),
                'seasonal_baseline_delta_t_c': [seasonal.loc[int(month[-2:])] for month in results.index]}
    for field, values in expected.items():
        require(np.allclose(results[field], values, atol=1.1e-6, rtol=0), "Train-only baseline mismatch.")
    scores = {field: float((results[field] - results.reported_delta_t_c).abs().mean())
              for field in [*expected, 'model_delta_t_c']}
    for field, value in scores.items():
        require(np.isclose(value, metrics['test_mae_c'][field], atol=1.1e-6, rtol=0), "Saved MAE mismatch.")
    if evaluation:
        identity = {field: entry[field] for field in ['dataset_id', 'plant_id_eia', 'cooling_id_eia']}
        verification = json.loads(paths[-1].read_text(encoding='utf-8'))
        require(metrics['identity'] == identity and verification['identity'] == identity,
                "Model artifacts belong to another system.")
        require(verification['verified'] is True, "Independent verification is not successful.")
        require(verification['test_n'] == len(results), "Verification test count mismatch.")
        require(hashes[result_path] == evaluation['results_sha256'], "Result hash mismatch.")
        require(hashes[metrics_path] == verification['artifact_sha256']['model_artifacts/metrics.json'],
                "Verified metrics hash mismatch.")
        require(hashes[result_path] == verification['artifact_sha256']['results.csv'],
                "Verified result hash mismatch.")
        require(evaluation['test_n'] == len(results), "Registry test count mismatch.")
        for field, value in scores.items():
            require(np.isclose(value, evaluation['mae_c'][field], atol=1.1e-6, rtol=0), "Registry MAE mismatch.")
            require(np.isclose(value, verification['independent_csv_mae_c'][field], atol=1.1e-6, rtol=0),
                    "Independent verification MAE mismatch.")
    else:
        require(entry['plant_id_eia'] == 3806 and entry['cooling_id_eia'] == 'CW1'
                and entry['results_path'] == 'data/results.csv', "Unrecognized legacy model identity.")
    require(all(sha256(path) == digest for path, digest in hashes.items()),
            "Model files changed during this read. Refresh data.")
    current(root, token)
    return results, scores
