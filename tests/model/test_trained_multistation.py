"""Check saved multi-system artifacts and failure paths without fitting models."""
from pathlib import Path
import copy
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from src.model import model
from src.model.registry import REGISTRY_PATH, read_registry, sha256
from src.model.train_multistation import atomic_registry_update, train_dataset, verify_export


class SavedModelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=read_registry(ROOT)
        cls.calvert=next(e for e in cls.registry['datasets'] if e['plant_id_eia']==6011 and e['cooling_id_eia']=='SYS042')
        cls.calvert_dir=(ROOT/cls.calvert['artifacts']['future_results_path']).parent

    def test_all_sixteen_saved_models_verify_without_fit(self):
        evaluated=[e for e in self.registry['datasets'] if e['model_status']=='evaluated_verified']
        self.assertEqual(len(evaluated),16)
        with patch.object(model,'train_model',side_effect=AssertionError('No fitting in verification')):
            for entry in evaluated:
                directory=(ROOT/entry['results_path']).parent
                result=verify_export(ROOT,entry['dataset_id'],directory)
                self.assertTrue(result['verified'])
                self.assertEqual(result['test_n'],entry['split_counts']['test'])
                self.assertEqual(sha256(ROOT/entry['results_path']),entry['evaluation']['results_sha256'])

    def test_surry_and_review_dataset_cannot_train(self):
        surry=next(e for e in self.registry['datasets'] if e['plant_id_eia']==3806 and e['cooling_id_eia']=='CW1')
        pending=next(e for e in self.registry['datasets'] if e['status']=='review_required')
        before=sha256(ROOT/'data/results.csv')
        with patch.object(model,'train_model',side_effect=AssertionError('Fit forbidden')):
            with self.assertRaisesRegex(ValueError,'protected'):
                train_dataset(ROOT,surry['dataset_id'])
            with self.assertRaisesRegex(ValueError,'not ready'):
                train_dataset(ROOT,pending['dataset_id'])
        self.assertEqual(sha256(ROOT/'data/results.csv'),before)

    def test_corrupted_export_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copied=Path(directory)/'copy'
            shutil.copytree(self.calvert_dir,copied)
            data=pd.read_csv(copied/'results.csv')
            data.loc[0,'reported_delta_t_c']+=1
            data.to_csv(copied/'results.csv',index=False)
            with self.assertRaisesRegex(ValueError,'target/source'):
                verify_export(ROOT,self.calvert['dataset_id'],copied)

    def test_wrong_system_identity_and_changed_selection_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copied=Path(directory)/'copy'
            shutil.copytree(self.calvert_dir,copied)
            path=copied/'model_artifacts/parameters.json'
            parameters=json.loads(path.read_text())
            parameters['identity']['plant_id_eia']=3806
            path.write_text(json.dumps(parameters))
            with self.assertRaisesRegex(ValueError,'another system'):
                verify_export(ROOT,self.calvert['dataset_id'],copied)
            shutil.copyfile(self.calvert_dir/'model_artifacts/parameters.json',path)
            selection=copied/'model_artifacts/selection.json'
            value=json.loads(selection.read_text())
            value['selected_alpha']=123
            selection.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError,'Selection lock changed'):
                verify_export(ROOT,self.calvert['dataset_id'],copied)

    def test_atomic_write_failure_keeps_previous_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            path=root/REGISTRY_PATH
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(self.registry))
            before=path.read_bytes()
            with patch('src.model.train_multistation.read_registry',return_value=copy.deepcopy(self.registry)):
                with patch('src.model.train_multistation.os.replace',side_effect=OSError('simulated failure')):
                    with self.assertRaises(OSError):
                        atomic_registry_update(root,self.calvert['dataset_id'],self.calvert['evaluation'])
            self.assertEqual(path.read_bytes(),before)
            self.assertFalse(list(path.parent.glob('registry-*.tmp')))


if __name__=='__main__':
    unittest.main()
