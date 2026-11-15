"""Unit/conservation and invalid-input checks for explicit scenario arithmetic."""
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.fuel.scenarios import mixed_stream, closed_volume_rise, lifecycle_tonnes, reference_difference


class ScenarioTests(unittest.TestCase):
    def test_mixing_heat_balance_and_bounds(self):
        result = mixed_stream(20, 30, 90, 10)
        self.assertAlmostEqual(result['mixed_c'], 21)
        self.assertAlmostEqual(result['rise_c'], 1)
        self.assertAlmostEqual(result['mixed_c'] * 100, 90 * 20 + 10 * 30)
        self.assertEqual(mixed_stream(20, 30, 0, 10)['mixed_c'], 30)
        self.assertEqual(mixed_stream(20, 20, 90, 10)['rise_c'], 0)
        self.assertLess(mixed_stream(20, 10, 90, 10)['rise_c'], 0)
        self.assertEqual(mixed_stream(20, 30, 1e308, 1e308)['mixed_c'], 25)

    def test_closed_volume_units_and_scaling(self):
        self.assertAlmostEqual(closed_volume_rise(360000, 10, 10, 1), 1)
        self.assertAlmostEqual(closed_volume_rise(720000, 10, 10, 1), .5)
        self.assertEqual(closed_volume_rise(360000, 10, 10, 0), 0)

    def test_lifecycle_unit_conversion(self):
        self.assertEqual(lifecycle_tonnes(1, 12), 12000)
        self.assertEqual(lifecycle_tonnes(0, 12), 0)
        self.assertAlmostEqual(lifecycle_tonnes(1, 3.7), 3700)
        self.assertEqual(lifecycle_tonnes(1, 110), 110000)

    def test_reference_difference_is_not_safety_classification(self):
        self.assertEqual(reference_difference(25, 20), 5)
        self.assertEqual(reference_difference(20, 25), -5)

    def test_invalid_inputs(self):
        for bad in [None, True, math.nan, math.inf, 'unknown']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                lifecycle_tonnes(bad, 12)
        for args in [(20, 30, -1, 10), (20, 30, 10, 0), (-300, 30, 10, 1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                mixed_stream(*args)
        with self.assertRaises(ValueError):
            closed_volume_rise(0, 1, 1, 1)
        with self.assertRaises(ValueError):
            lifecycle_tonnes(-1, 12)
        with self.assertRaises(ValueError):
            lifecycle_tonnes(1e308, 110)


if __name__ == '__main__':
    unittest.main()
