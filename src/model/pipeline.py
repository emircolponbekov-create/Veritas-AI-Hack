"""Parameterize the existing pipeline by dataset_id; preparation only, no fit."""
from .registry import find_dataset, project_path
from .datasets import load_observations, require


def prepare_job(root, identifier):
    entry = find_dataset(root, identifier)
    require(entry['status']=='ready_for_model_check',
            f'Dataset is not ready: {entry["status"]}; {entry["limitations"]}')
    frame = load_observations(root, entry)
    from . import model
    parts = model.prepare_splits(frame)
    require({name:len(part) for name,part in parts.items()}==entry['split_counts'],
            'Prepared split sizes changed')
    features = {name:model.make_features(part) for name,part in parts.items()}
    return {'dataset':entry, 'parts':parts, 'features':features,
            'target':'delta_t_c', 'shared_training_function':model.train_model,
            'shared_prediction_function':model.predict_table,
            'results_path':project_path(root,entry['artifacts']['future_results_path']),
            'artifacts_dir':project_path(root,entry['artifacts']['future_artifacts_dir']),
            'preserve_existing_result':entry['model_status']=='existing_verified'}
