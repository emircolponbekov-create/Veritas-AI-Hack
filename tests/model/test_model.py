"""Focused guards against leakage, broken units, flags and time splits."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("surry_model", ROOT / "src/model/model.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ModelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pd.read_csv(ROOT / "data/surry_cw1_monthly.csv")
        cls.frame, cls.audit = module.audit_data(ROOT / "data/surry_cw1_monthly.csv")
        cls.parts = module.prepare_splits(cls.frame)

    def reject(self, frame, message):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            frame.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, message):
                module.audit_data(path)

    def test_duplicate_month_rejected(self):
        self.reject(pd.concat([self.raw, self.raw.iloc[:1]], ignore_index=True), "Duplicate")

    def test_units_and_target_arithmetic_rejected(self):
        changed = self.raw.copy()
        changed.loc[0, "intake_temperature_c"] += 1
        self.reject(changed, "Fahrenheit/Celsius")
        changed = self.raw.copy()
        changed.loc[0, "delta_t_c"] += 1
        self.reject(changed, "Delta T")

    def test_unknown_method_cannot_be_eligible(self):
        changed = self.raw.copy()
        changed.loc[0, "temperature_method"] = "Other (provide explanation in Schedule 9)"
        self.reject(changed, "Eligibility")

    def test_chronological_split_guard(self):
        changed = self.raw.copy()
        changed.loc[0, "split"] = "test"
        self.reject(changed, "Split disagrees")

    def test_target_columns_cannot_affect_features(self):
        changed = self.frame.copy()
        changed["delta_t_c"] = 9999
        changed["discharge_temperature_c"] = -9999
        changed["discharge_temperature_f"] = 123456
        pd.testing.assert_frame_equal(module.make_features(self.frame), module.make_features(changed))

    def test_fit_uses_train_only_and_contract_matches(self):
        train, val, test = (self.parts[k] for k in ("train", "validation", "test"))
        model, median, seasonal, candidates = module.train_model(train, val)
        np.testing.assert_allclose(model.named_steps["standardscaler"].mean_,
                                   module.make_features(train).mean())
        self.assertEqual(median, train.delta_t_c.median())
        self.assertEqual(seasonal, train.groupby(train.date.dt.month).delta_t_c.median().to_dict())
        self.assertEqual(model.named_steps["ridge"].alpha,
                         candidates.loc[candidates.validation_mae_c.idxmin(), "alpha"])
        result = module.predict_table(test, model, median, seasonal)
        self.assertEqual(result.columns.tolist(), module.OUTPUT_FIELDS)
        self.assertEqual(result.report_month.tolist(), test.report_month.tolist())
        self.assertEqual(len(result), 22)
        self.assertTrue(np.isfinite(result.iloc[:, 1:].to_numpy()).all())


if __name__ == "__main__":
    unittest.main()
