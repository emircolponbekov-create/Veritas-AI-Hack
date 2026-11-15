"""Train isolated ready systems with the existing pipeline; verify before registry update."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import model
from .datasets import require
from .pipeline import prepare_job
from .registry import REGISTRY_PATH, find_dataset, project_path, read_registry, sha256

LOCKED_GRID = (0.1, 1.0, 10.0, 100.0)
IDENTITY_FIELDS = ('dataset_id', 'plant_id_eia', 'cooling_id_eia')


def identity(entry):
    return {field: entry[field] for field in IDENTITY_FIELDS}


def write_json(path, value, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')


def atomic_registry_update(root, identifier, evaluation):
    path = project_path(root, REGISTRY_PATH)
    before = path.read_bytes()
    data = read_registry(root)
    entry = next(e for e in data['datasets'] if e['dataset_id'] == identifier)
    require(entry['model_status'] != 'existing_verified', 'Protected legacy model')
    require(entry['status'] == 'ready_for_model_check', 'Dataset no longer ready')
    entry['model_status'] = 'evaluated_verified'
    entry['results_path'] = entry['artifacts']['future_results_path']
    entry['evaluation'] = evaluation
    payload = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode('utf-8')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='registry-', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        require(path.read_bytes() == before, 'Concurrent registry change; refusing to replace')
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def split_record(job):
    return {'identity': identity(job['dataset']),
            'periods': {'train': [2010,2021], 'validation': [2022,2023], 'test': [2024,2025]},
            'months': {name: part.report_month.tolist() for name,part in job['parts'].items()},
            'counts': job['dataset']['split_counts'],
            'excluded_months': job['dataset']['excluded_months'],
            'input_sha256': job['dataset']['observations']['sha256']}


def lock_selection(directory, job, fitted, median, seasonal, candidates):
    scaler, ridge = fitted.steps[0][1], fitted.steps[1][1]
    record = {'identity': identity(job['dataset']), 'locked_before_test': True,
              'locked_at_utc': datetime.now(timezone.utc).isoformat(),
              'alpha_grid': list(LOCKED_GRID), 'selected_alpha': float(ridge.alpha),
              'validation_candidates': candidates.to_dict(orient='records'),
              'features': model.FEATURES, 'scaler_mean': scaler.mean_.tolist(),
              'scaler_scale': scaler.scale_.tolist(), 'ridge_coef': ridge.coef_.tolist(),
              'ridge_intercept': float(ridge.intercept_), 'train_median_c': median,
              'train_monthly_medians_c': {str(k):float(v) for k,v in seasonal.items()},
              'input_sha256': job['dataset']['observations']['sha256'],
              'pipeline_sha256': sha256(Path(model.__file__))}
    write_json(directory/'selection.json', record, exclusive=True)
    write_json(directory/'splits.json', split_record(job), exclusive=True)
    return sha256(directory/'selection.json')


def verify_export(root, identifier, output_dir):
    job = prepare_job(root, identifier)
    entry = job['dataset']
    output_dir = Path(output_dir)
    artifacts = output_dir/'model_artifacts'
    results = pd.read_csv(output_dir/'results.csv')
    require(results.columns.tolist() == model.OUTPUT_FIELDS, 'Results contract mismatch')
    require(results.report_month.is_unique and results.report_month.is_monotonic_increasing, 'Duplicate/unsorted results')
    test = job['parts']['test'].reset_index(drop=True)
    train = job['parts']['train']
    require(results.report_month.tolist() == test.report_month.tolist(), 'Wrong system test months')
    require(np.isfinite(results.iloc[:,1:].to_numpy()).all(), 'Missing/nonfinite exported values')
    require(np.allclose(results.intake_temperature_c,test.intake_temperature_c,atol=1.1e-6,rtol=0), 'Export inlet/source mismatch')
    require(np.allclose(results.reported_delta_t_c,test.delta_t_c,atol=1.1e-6,rtol=0), 'Export target/source mismatch')
    median = float(train.delta_t_c.median())
    seasonal = train.groupby(train.date.dt.month).delta_t_c.median()
    require(np.allclose(results.median_baseline_delta_t_c,median,atol=5.1e-7,rtol=0), 'Global baseline is not train-only median')
    require(np.allclose(results.seasonal_baseline_delta_t_c,test.date.dt.month.map(seasonal),atol=5.1e-7,rtol=0), 'Seasonal baseline is not train-only median')
    params = json.loads((artifacts/'parameters.json').read_text(encoding='utf-8'))
    metrics = json.loads((artifacts/'metrics.json').read_text(encoding='utf-8'))
    selection = json.loads((artifacts/'selection.json').read_text(encoding='utf-8'))
    splits = json.loads((artifacts/'splits.json').read_text(encoding='utf-8'))
    audit = json.loads((artifacts/'audit.json').read_text(encoding='utf-8'))
    for document in [params,metrics,selection,splits,audit]:
        require(document['identity'] == identity(entry), 'Artifact belongs to another system')
    require(splits == split_record(job), 'Saved splits changed')
    require(selection['locked_before_test'] and selection['alpha_grid'] == list(LOCKED_GRID), 'Selection protocol mismatch')
    require(selection['pipeline_sha256'] == sha256(Path(model.__file__)), 'Pipeline code changed')
    require(selection['input_sha256'] == metrics['input_sha256'] == entry['observations']['sha256'], 'Input provenance mismatch')
    require(metrics['selection_sha256'] == sha256(artifacts/'selection.json'), 'Selection lock changed')
    require(params['features'] == model.FEATURES, 'Unexpected features')
    for field in ['scaler_mean','scaler_scale','ridge_coef','ridge_intercept','train_median_c','train_monthly_medians_c']:
        require(params[field] == selection[field], 'Parameters differ from pre-test selection lock')
    candidates = pd.read_csv(artifacts/'validation_scores.csv')
    require(candidates.alpha.tolist() == list(LOCKED_GRID), 'Candidate grid changed')
    locked_candidates = pd.DataFrame(selection['validation_candidates'])
    require(np.allclose(candidates,locked_candidates,rtol=0,atol=1e-12), 'Validation record mismatch')
    require(candidates.loc[candidates.validation_mae_c.idxmin(),'alpha'] == params['alpha'] == metrics['selected_alpha'] == selection['selected_alpha'], 'Alpha was not selected on validation')
    x_train = job['features']['train'].to_numpy()
    require(np.allclose(params['scaler_mean'],x_train.mean(axis=0),atol=1e-12,rtol=0), 'Scaler mean is not train-only')
    require(np.allclose(params['scaler_scale'],x_train.std(axis=0),atol=1e-12,rtol=0), 'Scaler scale is not train-only')
    require(abs(params['train_median_c']-median)<1e-12, 'Parameter median mismatch')
    require(all(abs(params['train_monthly_medians_c'][str(k)]-v)<1e-12 for k,v in seasonal.items()), 'Parameter seasonal medians mismatch')
    def infer(part):
        x = job['features'][part].to_numpy()
        return ((x-np.array(params['scaler_mean']))/np.array(params['scaler_scale']))@np.array(params['ridge_coef'])+params['ridge_intercept']
    require(np.allclose(results.model_delta_t_c,infer('test'),atol=5.1e-7,rtol=0), 'Export differs from saved model parameters')
    val_mae = float(np.abs(infer('validation')-job['parts']['validation'].delta_t_c.to_numpy()).mean())
    require(abs(val_mae-metrics['validation_mae_c']['model_delta_t_c'])<1e-12, 'Validation MAE mismatch')
    scores = {field:float(np.abs(results[field]-results.reported_delta_t_c).mean()) for field in model.OUTPUT_FIELDS[3:]}
    require(all(abs(scores[k]-metrics['test_mae_c'][k])<=1e-6 for k in scores), 'Saved MAE mismatch beyond CSV rounding')
    require(metrics['test_months'] == results.report_month.tolist(), 'Metrics use different test months')
    for name,part in job['parts'].items():
        expected={'n':len(part),'start':part.report_month.min(),'end':part.report_month.max()}
        require(metrics['split'][name]==expected, 'Metric split metadata mismatch')
    errors=pd.read_csv(artifacts/'test_errors.csv')
    require(errors.report_month.tolist()==results.report_month.tolist(), 'Error file uses other months')
    require(np.allclose(errors[model.OUTPUT_FIELDS[1:]],results[model.OUTPUT_FIELDS[1:]],atol=5.1e-7,rtol=0), 'Error table values mismatch')
    require(np.allclose(errors.absolute_model_error_c,np.abs(errors.model_delta_t_c-errors.reported_delta_t_c),atol=1e-12,rtol=0), 'Error table arithmetic mismatch')
    report=(artifacts/'evaluation.md').read_text(encoding='utf-8')
    require(report.startswith(f'# {entry["plant_name"]} / {entry["cooling_id_eia"]} evaluation'), 'Wrong station label in report')
    worst_index = np.abs(results.model_delta_t_c-results.reported_delta_t_c).idxmax()
    worst = results.loc[worst_index].to_dict()
    worst['absolute_model_error_c'] = float(abs(worst['model_delta_t_c']-worst['reported_delta_t_c']))
    require(worst['report_month']==metrics['worst_model_error']['report_month'], 'Wrong error example')
    require(abs(worst['absolute_model_error_c']-metrics['worst_model_error']['absolute_model_error_c'])<1e-6, 'Error example mismatch')
    hashes = {p.relative_to(output_dir).as_posix():sha256(p) for p in sorted(output_dir.rglob('*')) if p.is_file() and p.name!='verification.json'}
    best = min(scores[k] for k in model.OUTPUT_FIELDS[3:5])
    return {'identity':identity(entry), 'verified':True, 'independent_csv_mae_c':scores,
            'test_n':len(results), 'split_counts':entry['split_counts'],
            'beats_best_baseline':scores['model_delta_t_c']<best,
            'improvement_vs_best_baseline_c':best-scores['model_delta_t_c'],
            'worst_error_from_csv':worst, 'artifact_sha256':hashes}


def register_verified(root, identifier, verification):
    entry = find_dataset(root,identifier)
    base = project_path(root,entry['artifacts']['future_results_path']).parent
    atomic_registry_update(root,identifier,{
        'metrics_path':(base/'model_artifacts/metrics.json').relative_to(root).as_posix(),
        'verification_path':(base/'model_artifacts/verification.json').relative_to(root).as_posix(),
        'results_sha256':sha256(base/'results.csv'), 'test_n':verification['test_n'],
        'mae_c':verification['independent_csv_mae_c'],
        'beats_best_baseline':verification['beats_best_baseline']})


def train_dataset(root, identifier):
    root = Path(root).resolve()
    job = prepare_job(root,identifier)
    entry = job['dataset']
    require(not job['preserve_existing_result'], 'Surry CW1 is protected; no retraining')
    require(tuple(model.ALPHAS)==LOCKED_GRID, 'Shared Ridge grid differs from predefined protocol')
    final = job['results_path'].parent
    require(final.resolve().is_relative_to(root), 'Output directory escapes project')
    if (final/'results.csv').exists() and (final/'model_artifacts').is_dir():
        verification = verify_export(root,identifier,final)
        write_json(final/'model_artifacts/verification.json',verification)
        register_verified(root,identifier,verification)
        return verification
    require(entry['model_status']=='not_trained', 'Unexpected model state; no retraining')
    require(not (final/'results.csv').exists() and not (final/'model_artifacts').exists(), 'Partial output exists; preserve for inspection')
    final.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.training-',dir=final) as temporary:
        stage = Path(temporary)
        artifacts = stage/'model_artifacts'
        train, validation = job['parts']['train'], job['parts']['validation']
        fitted, median, seasonal, candidates = job['shared_training_function'](train,validation)
        selection_hash = lock_selection(artifacts,job,fitted,median,seasonal,candidates)
        results = job['shared_prediction_function'](job['parts']['test'],fitted,median,seasonal)
        figure = model.plot_results(results)
        figure.axes[0].set_title(f'{entry["plant_name"]} / {entry["cooling_id_eia"]}: retrospective test estimates')
        try:
            audit = {'input_sha256':entry['observations']['sha256'], 'identity':identity(entry),
                     'provenance':entry['provenance'], 'limitations':entry['limitations']}
            model.export_outputs(stage,project_path(root,entry['observations']['path']),audit,
                                 job['parts'],fitted,median,seasonal,candidates,results,figure)
        finally:
            plt.close(figure)
        for name in ['metrics.json','parameters.json','audit.json']:
            path = artifacts/name
            data = json.loads(path.read_text(encoding='utf-8'))
            data['identity'] = identity(entry)
            if name=='metrics.json':
                data['contract_version']='v2'
                data['selection_sha256']=selection_hash
            if name=='audit.json':
                data.pop('expected_split_counts_match',None)
                data['registry_split_counts_match']=data['split_counts']==entry['split_counts']
            write_json(path,data)
        report_path=artifacts/'evaluation.md'
        text=report_path.read_text(encoding='utf-8')
        report_path.write_text(text.replace('# Surry CW1 evaluation',f'# {entry["plant_name"]} / {entry["cooling_id_eia"]} evaluation',1),encoding='utf-8')
        verification=verify_export(root,identifier,stage)
        write_json(artifacts/'verification.json',verification,exclusive=True)
        require(not (final/'results.csv').exists() and not (final/'model_artifacts').exists(),'Concurrent output appeared')
        os.rename(artifacts,final/'model_artifacts')
        os.rename(stage/'results.csv',final/'results.csv')
    verification=verify_export(root,identifier,final)
    register_verified(root,identifier,verification)
    return verification


def protection_snapshot(root):
    root=Path(root)
    paths=[*root.joinpath('data/incoming').rglob('*'),*root.joinpath('data/model_artifacts').glob('*'),
           root/'data/results.csv',root/'data/surry_cw1_monthly.csv',root/'src/model/model.py',
           root/'src/model/surry_model.ipynb',*root.joinpath('src/ui').glob('*.py'),root/'docs/work/DATA_CONTRACT.md']
    return {str(p):sha256(p) for p in paths if p.is_file()}


def assert_protected(snapshot):
    require(all(sha256(path)==value for path,value in snapshot.items()),'Protected source/Surry/UI/contract hash changed')


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--dataset')
    parser.add_argument('--remaining',action='store_true')
    args=parser.parse_args()
    require(bool(args.dataset)!=args.remaining,'Choose exactly --dataset ID or --remaining')
    root=args.root.resolve()
    protected=protection_snapshot(root)
    data=read_registry(root)
    ready=[e for e in data['datasets'] if e['status']=='ready_for_model_check']
    require(len(ready)==17,'Ready membership changed; review before batch')
    selected=[e for e in ready if e['model_status']=='not_trained'] if args.remaining else [find_dataset(root,args.dataset)]
    failures=[]
    try:
        for entry in selected:
            try:
                check=train_dataset(root,entry['dataset_id'])
                print(json.dumps({'dataset_id':entry['dataset_id'],'verified':True,'mae_c':check['independent_csv_mae_c']},ensure_ascii=False),flush=True)
            except Exception as error:
                failures.append({'dataset_id':entry['dataset_id'],'error_type':type(error).__name__,'reason':str(error)})
                print(json.dumps(failures[-1],ensure_ascii=False),flush=True)
            assert_protected(protected)
    finally:
        assert_protected(protected)
    if failures:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
        write_json(project_path(root,f'data/model_artifacts/multistation/failures-{stamp}.json'),failures,exclusive=True)
        raise SystemExit(1)


if __name__=='__main__':
    main()
