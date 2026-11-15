"""Preparation and saved-result regression checks; every fit is forbidden."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.model import datasets, registry, pipeline, model


class PreparationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = registry.read_registry(ROOT)
        cls.entries = cls.data['datasets']
        cls.surry = next(e for e in cls.entries if e['plant_id_eia']==3806 and e['cooling_id_eia']=='CW1')

    def test_ui_reader_imports_no_ml_or_dataframe_library(self):
        code = (f'import sys;sys.path.insert(0,{str(ROOT)!r});'
                'from src.model.registry import read_registry;'
                f'd=read_registry({str(ROOT)!r});'
                'assert len(d["datasets"])==102;'
                'assert not any(x in sys.modules for x in ["sklearn","pandas","numpy"]);print("OK")')
        result = subprocess.run([sys.executable,'-I','-B','-c',code],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_ids_are_reversible_and_do_not_merge_different_systems(self):
        systems = ['1','CW1','CW-1','cw1','CW/1','CW_1']
        identifiers = [registry.dataset_id(3806,s) for s in systems]
        self.assertEqual(len(set(identifiers)),len(systems))
        for identifier,system in zip(identifiers,systems):
            self.assertEqual(bytes.fromhex(identifier.split('_',2)[2]).decode(),system)
        self.assertEqual(len(self.entries),102)
        self.assertEqual(len({e['plant_id_eia'] for e in self.entries}),66)

    def test_original_csv_paths_are_reused(self):
        csv_entries = [e for e in self.entries if e['observations']['format']=='csv']
        self.assertEqual(len(csv_entries),7)
        self.assertEqual(self.surry['observations']['path'],'data/surry_cw1_monthly.csv')
        self.assertTrue(all('/station_csv/' in e['observations']['path'] for e in csv_entries if e!=self.surry))

    def test_all_ready_jobs_use_shared_pipeline_without_fitting(self):
        ready = [e for e in self.entries if e['status']=='ready_for_model_check']
        self.assertEqual(len(ready),17)
        with patch.object(model,'train_model',side_effect=AssertionError('Training forbidden')):
            with patch('sklearn.linear_model.Ridge.fit',side_effect=AssertionError('Fit forbidden')):
                for entry in ready:
                    job = pipeline.prepare_job(ROOT,entry['dataset_id'])
                    self.assertEqual({k:len(v) for k,v in job['parts'].items()},entry['split_counts'])
                    self.assertTrue(all(v.columns.tolist()==model.FEATURES for v in job['features'].values()))
                    self.assertTrue(all(np.isfinite(v.to_numpy()).all() for v in job['features'].values()))
                    self.assertFalse(entry['review_months'])

    def test_suspect_measured_values_are_kept_but_job_is_blocked(self):
        entry = next(e for e in self.entries if e['plant_id_eia']==566 and e['cooling_id_eia']=='CIRC2')
        self.assertEqual(entry['status'],'review_required')
        frame = datasets.load_observations(ROOT,entry)
        row = frame.loc[frame.report_month.eq('2023-06')].iloc[0]
        self.assertTrue(row.eligible_measured)
        self.assertEqual(row.delta_t_c,0)
        self.assertEqual(entry['split_counts'],{'train':144,'validation':24,'test':24})
        with self.assertRaisesRegex(ValueError,'not ready'):
            pipeline.prepare_job(ROOT,entry['dataset_id'])

    def test_strict_flags_missing_pair_and_units(self):
        self.assertEqual(datasets.parse_flag(pd.Series(['True','False','false'])).tolist(),[True,False,False])
        with self.assertRaisesRegex(ValueError,'Invalid boolean'):
            datasets.parse_flag(pd.Series(['unknown']))
        frame = datasets.load_observations(ROOT,self.surry)
        bad = frame.copy(); bad.loc[0,'intake_temperature_c'] += 1
        with self.assertRaisesRegex(ValueError,'conversion'):
            datasets.validate_frame(bad,3806,'CW1')
        bad = frame.copy(); bad.loc[0,'delta_t_c'] += 1
        with self.assertRaisesRegex(ValueError,'arithmetic'):
            datasets.validate_frame(bad,3806,'CW1')
        bad = frame.copy(); bad.loc[0,'split']='test'
        with self.assertRaisesRegex(ValueError,'split'):
            datasets.validate_frame(bad,3806,'CW1')
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            datasets.validate_frame(pd.concat([frame,frame.iloc[:1]]),3806,'CW1')
        missing=pd.DataFrame({'report_month':['2010-01'],'plant_id_eia':[3806],
            'cooling_id_eia':['CW1'],datasets.F_IN:pd.Series([pd.NA],dtype='Float64'),
            datasets.F_OUT:[60.0],'temperature_method':['Measured continuously with a thermometer']})
        prepared=datasets.from_raw(missing,'Surry')
        self.assertFalse(prepared.pair_available.iloc[0])
        self.assertFalse(prepared.eligible_measured.iloc[0])
        self.assertTrue(pd.isna(prepared.delta_t_c.iloc[0]))

    def test_path_traversal_and_changed_artifact_are_rejected(self):
        for path in ['../secret','C:/secret','/secret','data/../secret',r'data\secret']:
            with self.assertRaises(ValueError):
                registry.project_path(ROOT,path)
        with tempfile.TemporaryDirectory() as directory:
            datasets.write_same_or_new(directory,'data/item.json',{'x':1})
            path=Path(directory)/'data/item.json'
            before=path.read_bytes()
            with self.assertRaisesRegex(ValueError,'refusing overwrite'):
                datasets.write_same_or_new(directory,'data/item.json',{'x':2})
            self.assertEqual(path.read_bytes(),before)

    def test_registry_rejects_tampered_selector_and_fake_model_result(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/registry.REGISTRY_PATH
            target.parent.mkdir(parents=True)
            altered=json.loads(json.dumps(self.data))
            altered['datasets'][0]['observations']['selector']['plant_id_eia']=999999
            target.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError,'selector identity'):
                registry.read_registry(directory,verify=False)
            altered=json.loads(json.dumps(self.data))
            entry=next(e for e in altered['datasets'] if e['model_status']=='not_trained')
            entry['results_path']='data/fake.csv'
            target.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError,'Untrained dataset'):
                registry.read_registry(directory,verify=False)

    def test_existing_surry_result_and_hashes_unchanged(self):
        scores=datasets.verify_legacy_result(ROOT,self.surry)
        self.assertAlmostEqual(scores['model_delta_t_c'],1.8493300909090906,places=10)
        self.assertEqual(self.surry['split_counts'],{'train':142,'validation':24,'test':22})
        self.assertEqual(self.surry['results_path'],'data/results.csv')
        self.assertEqual(registry.sha256(ROOT/'data/results.csv'),
                         '428f2546307aae67a29be8c49827faa09e4e3d765b7999a5bdf22426afafd435')
        self.assertEqual(registry.sha256(ROOT/'src/model/model.py'),
                         'b53aec7f6f1870eec9195822e71509c2785e2bf4f92d8c8ec0698378948e9a5a')

    def test_repeated_preparation_has_identical_bytes_and_mtime(self):
        paths=list((ROOT/'data/model_artifacts/multistation').rglob('*.json'))
        before={p:(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns) for p in paths}
        with patch.object(model,'train_model',side_effect=AssertionError('Training forbidden')):
            datasets.prepare_registry(ROOT)
        after={p:(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns) for p in paths}
        self.assertEqual(before,after)


if __name__=='__main__':
    unittest.main()
