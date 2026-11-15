"""Prepare and validate single-system datasets from frozen local inputs; never fit."""
from pathlib import Path
import json
import re

import numpy as np
import pandas as pd

from .registry import REGISTRY_PATH, dataset_id, project_path, sha256

DEFAULT_INBOX = 'data/incoming/collected-20261114-150548'
METHODS = {'Measured continuously with a thermometer',
           'Measured at intervals (for example, daily) with a thermometer'}
TABLE = '_core_eia923__monthly_cooling_system_information'
BASE_URL = 'https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/'
F_IN = 'monthly_average_intake_temperature_fahrenheit'
F_OUT = 'monthly_average_discharge_temperature_fahrenheit'
VALUE_FIELDS = ['intake_temperature_f', 'discharge_temperature_f',
                'intake_temperature_c', 'discharge_temperature_c', 'delta_t_c']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_flag(series):
    normalized = series.astype(str).str.strip().str.lower()
    require(normalized.isin(['true', 'false']).all(), f'Invalid boolean in {series.name}')
    return normalized.eq('true')


def assign_split(year):
    return np.where(year <= 2021, 'train', np.where(year <= 2023, 'validation', 'test'))


def from_raw(rows, plant_name):
    frame = rows[['report_month', 'plant_id_eia', 'cooling_id_eia']].copy()
    frame['plant_name'] = plant_name
    frame['intake_temperature_f'] = pd.to_numeric(rows[F_IN], errors='raise').to_numpy(dtype=float, na_value=np.nan)
    frame['discharge_temperature_f'] = pd.to_numeric(rows[F_OUT], errors='raise').to_numpy(dtype=float, na_value=np.nan)
    for point in ['intake', 'discharge']:
        frame[f'{point}_temperature_c'] = (frame[f'{point}_temperature_f'] - 32) * 5 / 9
    frame['delta_t_c'] = (frame.discharge_temperature_f - frame.intake_temperature_f) * 5 / 9
    frame['temperature_method'] = rows.temperature_method.fillna('').astype(str).str.strip()
    frame['pair_available'] = np.isfinite(frame[VALUE_FIELDS].to_numpy(dtype=float, na_value=np.nan)).all(axis=1)
    frame['eligible_measured'] = frame.pair_available & frame.temperature_method.isin(METHODS)
    frame['temperature_value_class'] = np.where(frame.temperature_method.isin(METHODS), 'measured',
        np.where(frame.temperature_method.str.contains('calculated|Estimated|Permitted', regex=True),
                 'estimated_or_calculated', 'unknown'))
    frame['split'] = assign_split(pd.to_datetime(frame.report_month).dt.year)
    frame['source_table'] = TABLE
    return frame


def validate_frame(frame, plant_id, system_id):
    frame = frame.copy()
    required = {'report_month', 'plant_id_eia', 'cooling_id_eia', 'temperature_method',
                'pair_available', 'eligible_measured', 'split', *VALUE_FIELDS}
    require(required.issubset(frame.columns), 'Missing observation columns')
    require(not frame.empty, 'No observation rows')
    require(frame.report_month.astype(str).str.fullmatch(r'\d{4}-\d{2}').all(), 'Invalid month format')
    frame['date'] = pd.to_datetime(frame.report_month, format='%Y-%m', errors='raise')
    require(frame.date.between('2010-01-01', '2025-12-01').all(), 'Date outside fixed protocol')
    require(frame.plant_id_eia.eq(plant_id).all() and frame.cooling_id_eia.eq(system_id).all(), 'Identity mismatch')
    require(not frame.report_month.duplicated().any(), 'Duplicate system month')
    frame[VALUE_FIELDS] = frame[VALUE_FIELDS].apply(pd.to_numeric, errors='raise')
    for flag in ['pair_available', 'eligible_measured']:
        frame[flag] = parse_flag(frame[flag])
    pair = np.isfinite(frame[VALUE_FIELDS].to_numpy(dtype=float, na_value=np.nan)).all(axis=1)
    methods = frame.temperature_method.fillna('').astype(str).str.strip()
    require(frame.pair_available.eq(pair).all(), 'Pair flag mismatch')
    require(frame.eligible_measured.eq(pair & methods.isin(METHODS)).all(), 'Measured eligibility mismatch')
    for point in ['intake', 'discharge']:
        require(np.allclose(frame[f'{point}_temperature_c'], (frame[f'{point}_temperature_f']-32)*5/9,
                            atol=1.1e-6, rtol=0, equal_nan=True), 'Celsius conversion mismatch')
    require(np.allclose(frame.delta_t_c, (frame.discharge_temperature_f-frame.intake_temperature_f)*5/9,
                        atol=1.1e-6, rtol=0, equal_nan=True), 'Delta arithmetic mismatch')
    require(frame.split.eq(assign_split(frame.date.dt.year)).all(), 'Fixed split mismatch')
    if 'source_table' in frame:
        require(frame.source_table.eq(TABLE).all(), 'Source table mismatch')
    return frame.sort_values('date').reset_index(drop=True)


def validate_csv(path, raw_frame, plant_id, system_id):
    frame = validate_frame(pd.read_csv(path), plant_id, system_id)
    expected = validate_frame(raw_frame, plant_id, system_id)
    require(frame.report_month.tolist() == expected.report_month.tolist(), 'CSV/raw months disagree')
    require(frame.plant_name.eq(expected.plant_name).all(), 'CSV station name mismatch')
    for field in VALUE_FIELDS:
        require(np.allclose(frame[field], expected[field], rtol=0, atol=1.1e-6, equal_nan=True), 'CSV/raw values disagree')
    actual_method = frame.temperature_method.fillna('').astype(str).str.strip()
    require(actual_method.eq(expected.temperature_method).all(), 'CSV/raw method mismatch')
    return frame


def review_flags(frame):
    measured = frame.eligible_measured
    flags = pd.DataFrame({
        'nonpositive_delta': measured & frame.delta_t_c.le(0),
        'temperature_range_review': measured & (~frame.intake_temperature_c.between(-5, 100)
                                                | ~frame.discharge_temperature_c.between(-5, 100)),
    }, index=frame.index)
    return {str(frame.loc[index, 'report_month']): flags.columns[row].tolist()
            for index, row in flags.iterrows() if row.any()}


def classify(frame, cooling_types, plant_id):
    eligible = frame.loc[frame.eligible_measured]
    counts = {name: int(eligible.split.eq(name).sum()) for name in ['train', 'validation', 'test']}
    reviews = review_flags(frame)
    calendar = sorted(eligible.loc[eligible.split.eq('train'), 'date'].dt.month.unique().tolist())
    screened = frame.eligible_measured & frame.delta_t_c.gt(0) & frame.intake_temperature_c.between(-5,100) & frame.discharge_temperature_c.between(-5,100) & (plant_id != 628)
    screen_counts = {name: int((screened & frame.split.eq(name)).sum()) for name in counts}
    screen_calendar = frame.loc[screened & frame.split.eq('train'), 'date'].dt.month.nunique()
    compatible = bool(cooling_types) and not (set(cooling_types)-{'O','ON','OC'})
    provisional = all(screen_counts.values()) and screen_calendar == 12 and compatible
    limitations = []
    if plant_id == 628:
        status = 'blocked'; limitations.append('mixed_site_nuclear_attribution_unconfirmed')
    elif not frame.pair_available.any():
        status = 'reference_only'; limitations.append('no_complete_pairs')
    elif eligible.empty:
        status = 'blocked'; limitations.append('no_explicit_measured_pairs')
    elif reviews:
        status = 'review_required'; limitations.append('suspect_measured_rows_retained_no_automatic_exclusion')
    elif not compatible:
        status = 'measurements_only'; limitations.append('cooling_scheme_semantics_require_review')
    elif not all(counts.values()) or len(calendar) != 12:
        status = 'measurements_only'; limitations.append('fixed_time_coverage_insufficient')
    else:
        status = 'ready_for_model_check'
    if not compatible:
        limitations.append('recirculating_mixed_or_unknown_cooling_codes')
    if frame.intake_temperature_c.isna().any() or frame.discharge_temperature_c.isna().any():
        limitations.append('missing_temperatures_retained_and_ineligible')
    limitations.extend(['reported_measurement_not_independent_sensor_validation',
                        'historical_monthly_retrospective_only_no_ecosystem_inference',
                        'historical_cooling_metadata_incomplete_or_changed'])
    inventory_status = 'model_check_candidate' if provisional else (
        'verified_reported_measurements' if screened.any() else 'blocked' if frame.pair_available.any() else 'reference_only')
    return status, inventory_status, counts, reviews, limitations


def write_same_or_new(root, relative, value):
    target = project_path(root, relative)
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')
    if target.exists():
        require(target.read_bytes() == payload, f'Prepared artifact differs; refusing overwrite: {relative}')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(payload)


def inventory_evidence(root, inbox):
    inventory = project_path(root, inbox + '/INVENTORY.md')
    text = inventory.read_text(encoding='utf-8')
    hashes = dict(re.findall(r'\| `([^`]+)` \| `([0-9a-f]{64})` \|', text))
    for absolute, digest in hashes.items():
        path = Path(absolute)
        require(path.resolve().is_relative_to(Path(root).resolve()), 'Inventory path outside project')
        require(sha256(path) == digest, f'Inventory input hash mismatch: {path}')
    return inventory, hashes, text


def prepare_registry(root, inbox=DEFAULT_INBOX):
    root = Path(root).resolve()
    inventory, hashes, text = inventory_evidence(root, inbox)
    raw_path = project_path(root, inbox + '/raw/cooling.parquet')
    entity_path = project_path(root, inbox + '/raw/entity_plants.parquet')
    generation_path = project_path(root, inbox + '/raw/nuclear_generation.parquet')
    for path in [raw_path, entity_path, generation_path]:
        require(str(path) in hashes, 'Raw input not anchored in inventory')
    raw = pd.read_parquet(raw_path)
    raw['report_month'] = pd.to_datetime(raw.report_date).dt.strftime('%Y-%m')
    raw = raw.loc[pd.to_datetime(raw.report_date).dt.year.between(2010, 2025)].copy()
    entities = pd.read_parquet(entity_path).set_index('plant_id_eia')
    nuclear_ids = set(pd.read_parquet(generation_path).plant_id_eia.astype(int))
    require(len(nuclear_ids) == 66, 'Source membership changed; review inventory')
    originals = {}
    csv_paths = [root/'data/surry_cw1_monthly.csv', *project_path(root, inbox+'/station_csv').glob('*.csv')]
    for path in csv_paths:
        require(str(path) in hashes, f'CSV not anchored in inventory: {path}')
        header = pd.read_csv(path, usecols=['plant_id_eia','cooling_id_eia'])
        identities = header.drop_duplicates()
        require(len(identities) == 1, 'Original CSV mixes identities')
        key = (int(identities.iloc[0].plant_id_eia), str(identities.iloc[0].cooling_id_eia))
        require(key not in originals, f'Competing originals for {key}')
        originals[key] = path
    entries = []
    audit_jobs = []
    raw_subset = raw.loc[raw.plant_id_eia.isin(nuclear_ids)]
    require(not raw_subset.cooling_id_eia.isna().any(), 'Missing system ID requires review')
    for (plant_id, system), rows in raw_subset.groupby(['plant_id_eia','cooling_id_eia'], sort=True):
        plant_id = int(plant_id); system = str(system)
        identifier = dataset_id(plant_id, system)
        name = str(entities.loc[plant_id, 'plant_name_eia'])
        frame = validate_frame(from_raw(rows, name), plant_id, system)
        original = originals.get((plant_id, system))
        if original:
            frame = validate_csv(original, frame, plant_id, system)
        types = sorted(rows.cooling_type.dropna().astype(str).str.strip().unique().tolist())
        status, previous, counts, reviews, limits = classify(frame, types, plant_id)
        directory = f'data/model_artifacts/multistation/datasets/{identifier}'
        legacy = plant_id == 3806 and system == 'CW1'
        source_path = original or raw_path
        relative = source_path.relative_to(root).as_posix()
        entry = {'dataset_id': identifier, 'plant_id_eia': plant_id, 'plant_name': name, 'cooling_id_eia': system,
            'observations': {'format': 'csv' if original else 'parquet', 'path': relative, 'sha256': sha256(source_path),
                             'selector': {'plant_id_eia': plant_id, 'cooling_id_eia': system, 'year_min': 2010, 'year_max': 2025}},
            'provenance': {'table': TABLE, 'source_url': BASE_URL+TABLE+'.parquet', 'source_units': 'degF', 'units': 'degC',
                           'raw_path': raw_path.relative_to(root).as_posix(), 'raw_sha256': sha256(raw_path),
                           'inventory_path': inventory.relative_to(root).as_posix(), 'inventory_sha256': sha256(inventory),
                           'license': 'CC-BY-4.0 (PUDL); public EIA data with acknowledgment'},
            'inventory_status': previous, 'status': status, 'limitations': limits,
            'rows': len(frame), 'eligible_rows': int(frame.eligible_measured.sum()),
            'period': [frame.report_month.min(),frame.report_month.max()], 'split_counts': counts,
            'excluded_months': frame.loc[~frame.eligible_measured,'report_month'].tolist(),
            'review_months': reviews, 'cooling_types': types,
            'model_status': 'existing_verified' if legacy else 'not_trained',
            'results_path': 'data/results.csv' if legacy else None,
            'artifacts': {'audit_path': directory+'/audit.json',
                          'future_results_path': 'data/results.csv' if legacy else directory+'/results.csv',
                          'future_artifacts_dir': 'data/model_artifacts' if legacy else directory+'/model_artifacts'}}
        audit = {'dataset_id':identifier, 'split_counts':counts, 'status':status, 'review_months':reviews,
                 'excluded_months':entry['excluded_months'], 'methods': frame.temperature_method.fillna('MISSING').value_counts().to_dict(),
                 'missing': {k:int(v) for k,v in frame.isna().sum().items() if v},
                 'missing_internal_months':pd.date_range(frame.date.min(),frame.date.max(),freq='MS').strftime('%Y-%m').difference(frame.report_month).tolist(),
                 'cooling_types':types, 'input_sha256':entry['observations']['sha256'],
                 'validation':'identity, source, units, arithmetic, strict flags, fixed splits; no fitting or imputation',
                 'limitations':limits}
        audit_jobs.append((entry['artifacts']['audit_path'],audit))
        entries.append(entry)
    require(len(entries)==102, 'System membership changed; review inventory')
    candidate_keys = set()
    section = text.split('## Подробная проверка систем')[1].split('### Методы')[0]
    for line in section.splitlines():
        if 'структурные проверки пройдены' in line:
            plant, system = line.split('|')[1].strip().split(' / ')
            candidate_keys.add(dataset_id(int(plant),system))
    actual_candidates = {e['dataset_id'] for e in entries if e['inventory_status']=='model_check_candidate'}
    require(candidate_keys == actual_candidates, 'Provisional candidates differ from inventory')
    legacy_entry = next(e for e in entries if e['plant_id_eia']==3806 and e['cooling_id_eia']=='CW1')
    verify_legacy_result(root, legacy_entry)
    registry = {'schema_version':2, 'contract':'DATA_CONTRACT v2; v1 Surry preserved',
                'source_inventory':inventory.relative_to(root).as_posix(), 'datasets':entries}
    for relative, value in audit_jobs:
        write_same_or_new(root,relative,value)
    write_same_or_new(root, REGISTRY_PATH,registry)
    return registry


def verify_legacy_result(root, entry):
    frame = pd.read_csv(project_path(root,entry['observations']['path']))
    frame = validate_frame(frame,3806,'CW1')
    test = frame.loc[frame.eligible_measured & frame.split.eq('test')].set_index('report_month')
    train = frame.loc[frame.eligible_measured & frame.split.eq('train')]
    result = pd.read_csv(project_path(root,'data/results.csv'))
    fields = ['report_month','intake_temperature_c','reported_delta_t_c','median_baseline_delta_t_c',
              'seasonal_baseline_delta_t_c','model_delta_t_c']
    require(result.columns.tolist()==fields and result.report_month.is_unique,'Legacy result schema mismatch')
    require(result.report_month.tolist()==test.index.tolist(),'Legacy test months mismatch')
    require(np.isfinite(result.iloc[:,1:]).all().all(),'Legacy nonfinite result')
    require(np.allclose(result.reported_delta_t_c,test.delta_t_c,rtol=0,atol=1e-9),'Legacy target mismatch')
    require(np.allclose(result.intake_temperature_c,test.intake_temperature_c,rtol=0,atol=1e-9),'Legacy inlet mismatch')
    median=train.delta_t_c.median()
    seasonal=train.groupby(train.date.dt.month).delta_t_c.median()
    require(np.allclose(result.median_baseline_delta_t_c,median,rtol=0,atol=5.1e-7),'Legacy median mismatch')
    require(np.allclose(result.seasonal_baseline_delta_t_c,pd.to_datetime(result.report_month).dt.month.map(seasonal),rtol=0,atol=5.1e-7),'Legacy seasonal mismatch')
    metrics=json.loads(project_path(root,'data/model_artifacts/metrics.json').read_text())
    require(metrics['input_sha256']==entry['observations']['sha256'],'Legacy metrics/source mismatch')
    for field in fields[3:]:
        score=float(np.abs(result[field]-result.reported_delta_t_c).mean())
        require(abs(score-metrics['test_mae_c'][field])<1e-6,'Legacy metric mismatch')
    return {field:float(np.abs(result[field]-result.reported_delta_t_c).mean()) for field in fields[3:]}


def load_observations(root, entry):
    source=entry['observations']
    path=project_path(root,source['path'])
    require(sha256(path)==source['sha256'],'Observation hash changed')
    raw_path=project_path(root,entry['provenance']['raw_path'])
    require(sha256(raw_path)==entry['provenance']['raw_sha256'],'Raw source hash changed')
    raw=pd.read_parquet(raw_path,
        filters=[('plant_id_eia','==',entry['plant_id_eia']),('cooling_id_eia','==',entry['cooling_id_eia'])],
        columns=['plant_id_eia','cooling_id_eia','report_date',F_IN,F_OUT,'temperature_method'])
    raw['report_month']=pd.to_datetime(raw.report_date).dt.strftime('%Y-%m')
    raw=raw.loc[raw.plant_id_eia.eq(entry['plant_id_eia']) & raw.cooling_id_eia.eq(entry['cooling_id_eia'])
                & pd.to_datetime(raw.report_date).dt.year.between(2010,2025)]
    frame=from_raw(raw,entry['plant_name'])
    return validate_csv(path,frame,entry['plant_id_eia'],entry['cooling_id_eia']) if source['format']=='csv' else validate_frame(frame,entry['plant_id_eia'],entry['cooling_id_eia'])


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    args=parser.parse_args()
    registry=prepare_registry(args.root)
    from collections import Counter
    print(json.dumps(dict(Counter(e['status'] for e in registry['datasets'])),indent=2))


if __name__=='__main__':
    main()
