"""UI/data integration checks; fixtures stay in temporary directories."""
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src/ui"))
from data_loader import (DataError, SOURCE_PATH, RESULTS_PATH, load_measurements,
                         load_results, history_chart, mae_table)


class DataTests(unittest.TestCase):
    def setUp(self):
        self.measurements, self.audit = load_measurements()

    def temporary_csv(self, frame):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "fixture.csv"
        frame.to_csv(path, index=False)
        return path

    def test_actual_source_months_units_and_gaps(self):
        self.assertEqual(self.audit["total"], 192)
        self.assertEqual(len(self.measurements), 188)
        months = self.measurements.report_month.tolist()
        self.assertEqual(months, sorted(set(months)))
        self.assertEqual((months[0], months[-1]), ("2010-01", "2025-12"))
        row = self.measurements.iloc[0]
        self.assertAlmostEqual(row.reported_delta_t_c,
                               row.discharge_temperature_c - row.intake_temperature_c)
        chart = history_chart(self.measurements)
        self.assertTrue(pd.isna(chart.loc["2024-08-01", "reported_delta_t_c"]))

    def test_rejects_unknown_units_eligibility_and_duplicate_months(self):
        original = pd.read_csv(SOURCE_PATH)
        wrong_units = original.copy()
        wrong_units.loc[0, "intake_temperature_c"] = 40
        wrong_eligibility = original.copy()
        wrong_eligibility.loc[0, "eligible_measured"] = False
        for frame in [wrong_units, wrong_eligibility, pd.concat([original, original.iloc[:1]])]:
            with self.subTest(), self.assertRaises(DataError):
                load_measurements(self.temporary_csv(frame))

    def test_actual_results_join_and_common_mae(self):
        results, missing = load_results(self.measurements)
        self.assertEqual(len(results), 22)
        self.assertEqual(missing, [])
        # Reverse measurement order: the join must still match months, not positions.
        reversed_results, _ = load_results(self.measurements.iloc[::-1])
        pd.testing.assert_frame_equal(results, reversed_results)
        scores = mae_table(results).set_index("Method")["MAE (°C)"]
        self.assertAlmostEqual(scores["Model"], 1.849330, places=5)
        self.assertAlmostEqual(scores["Train median"], 1.994950, places=5)
        self.assertAlmostEqual(scores["Train monthly median"], 2.045454, places=5)

    def test_partial_results_explicit_missing_month(self):
        frame = pd.read_csv(RESULTS_PATH).iloc[1:]
        results, missing = load_results(self.measurements, self.temporary_csv(frame))
        self.assertEqual(len(results), 21)
        self.assertEqual(missing, ["2024-01"])

    def test_invalid_results_rejected_without_changing_measurements(self):
        original = pd.read_csv(RESULTS_PATH)
        missing_value = original.copy()
        missing_value.loc[0, "model_delta_t_c"] = float("nan")
        bad_target = original.copy()
        bad_target.loc[0, "reported_delta_t_c"] += 1
        unknown_month = original.copy()
        unknown_month.loc[0, "report_month"] = "2023-12"
        for frame in [missing_value, bad_target, unknown_month,
                      pd.concat([original, original.iloc[:1]]), original.iloc[::-1],
                      original.drop(columns="model_delta_t_c")]:
            with self.subTest(), self.assertRaises(DataError):
                load_results(self.measurements, self.temporary_csv(frame))
        self.assertEqual(len(self.measurements), 188)


if __name__ == "__main__":
    unittest.main()
