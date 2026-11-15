"""Read-only, independently validated inputs for Water Impact (contract v1)."""
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = PROJECT_ROOT / "data/surry_cw1_monthly.csv"
RESULTS_PATH = PROJECT_ROOT / "data/results.csv"
SOURCE_TABLE = "_core_eia923__monthly_cooling_system_information"
METHOD = "Measured continuously with a thermometer"
RESULT_FIELDS = ["report_month", "intake_temperature_c", "reported_delta_t_c",
                 "median_baseline_delta_t_c", "seasonal_baseline_delta_t_c",
                 "model_delta_t_c"]
METHOD_LABELS = {"model_delta_t_c": "Model", "median_baseline_delta_t_c": "Train median",
                 "seasonal_baseline_delta_t_c": "Train monthly median"}
TOLERANCE = 1.1e-6  # CSV temperatures rounded to six decimal places.


class DataError(ValueError):
    """An input cannot safely be displayed with the documented meaning."""


def require(ok, message):
    if not ok:
        raise DataError(message)


def read_csv(path):
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        raise DataError(f"Cannot read {Path(path).name}: {exc}") from exc


def validate_months(frame):
    require(not frame.empty, "The CSV has no data rows.")
    require("report_month" in frame, "Missing report_month column (expected YYYY-MM).")
    require(frame.report_month.astype(str).str.fullmatch(r"\d{4}-(0[1-9]|1[0-2])").all(),
            "report_month must contain valid YYYY-MM values.")
    require(not frame.report_month.duplicated().any(), "Duplicate report_month values.")
    try:
        return pd.to_datetime(frame.report_month, format="%Y-%m", errors="raise")
    except ValueError as exc:
        raise DataError("Invalid reporting dates.") from exc


def numeric(frame, fields):
    try:
        frame[fields] = frame[fields].apply(pd.to_numeric, errors="raise")
    except (ValueError, TypeError) as exc:
        raise DataError("Temperature / estimate fields must be numeric.") from exc
    require(np.isfinite(frame[fields].to_numpy(dtype=float)).all(),
            "Missing or nonfinite numeric values; no values have been filled.")


def boolean(series):
    values = series.astype(str).str.strip().str.lower()
    require(values.isin(["true", "false"]).all(), f"Invalid true/false values in {series.name}.")
    return values.eq("true")


def load_measurements(path=SOURCE_PATH):
    frame = read_csv(path)
    fields = ["intake_temperature_f", "discharge_temperature_f", "intake_temperature_c",
              "discharge_temperature_c", "delta_t_c"]
    required = set(fields + ["report_month", "plant_id_eia", "cooling_id_eia", "source_table",
                              "eligible_measured", "pair_available", "temperature_method",
                              "temperature_value_class", "split"])
    require(required.issubset(frame.columns),
            f"Source schema needs review. Missing columns: {', '.join(sorted(required - set(frame.columns)))}")
    frame["date"] = validate_months(frame)
    require(pd.to_numeric(frame.plant_id_eia, errors="coerce").eq(3806).all()
            and frame.cooling_id_eia.eq("CW1").all(), "Expected only Surry EIA 3806 / CW1.")
    require(frame.source_table.eq(SOURCE_TABLE).all(), "Unknown source table; review data provenance.")
    eligible = boolean(frame.eligible_measured)
    pairs = boolean(frame.pair_available)
    measured = frame.temperature_method.eq(METHOD)
    require(eligible.eq(measured & pairs).all(), "Eligibility disagrees with the documented measurement method.")
    require(frame.loc[eligible, "temperature_value_class"].eq("measured").all(),
            "Eligible records must be classified as measured.")
    require(frame.date.between("2010-01-01", "2025-12-01").all(), "Source dates outside documented 2010–2025 snapshot.")
    expected_split = np.where(frame.date.dt.year <= 2021, "train",
                              np.where(frame.date.dt.year <= 2023, "validation", "test"))
    require((frame.split == expected_split).all(), "Source split disagrees with documented date ranges.")
    # Excluded rows may have missing measurements; they never enter cards or charts.
    selected = frame.loc[eligible].copy()
    require(not selected.empty, "No eligible measured months are available.")
    numeric(selected, fields)
    for point in ("intake", "discharge"):
        require(np.allclose(selected[f"{point}_temperature_c"],
                            (selected[f"{point}_temperature_f"] - 32) * 5 / 9,
                            atol=TOLERANCE, rtol=0), "Fahrenheit/Celsius mismatch; review units and conversion.")
    delta = selected.discharge_temperature_c - selected.intake_temperature_c
    require(np.allclose(selected.delta_t_c, delta, atol=TOLERANCE, rtol=0),
            "Reported delta differs from discharge minus intake.")
    selected["reported_delta_t_c"] = delta
    selected = selected.sort_values("report_month").reset_index(drop=True)
    return selected, {"total": len(frame), "eligible": len(selected),
                      "excluded": sorted(frame.loc[~eligible, "report_month"].tolist())}


def load_results(measurements, path=RESULTS_PATH):
    frame = read_csv(path)
    require(set(frame.columns) == set(RESULT_FIELDS), "results.csv does not match DATA_CONTRACT v1 columns.")
    dates = validate_months(frame)
    require(dates.dt.year.isin([2024, 2025]).all(), "Results must contain only test months in 2024–2025.")
    require(frame.report_month.is_monotonic_increasing, "Results must be sorted by report_month.")
    numeric(frame, RESULT_FIELDS[1:])
    source = measurements.set_index("report_month")
    require(frame.report_month.isin(source.index).all(), "Results include months without eligible measurements.")
    matched = source.loc[frame.report_month]
    for field in ["intake_temperature_c", "reported_delta_t_c"]:
        require(np.allclose(frame[field], matched[field], atol=TOLERANCE, rtol=0),
                f"Results {field} disagrees with source measurements joined by month.")
    expected = set(source.loc[source.split.eq("test")].index)
    missing = sorted(expected - set(frame.report_month))
    return frame.set_index("report_month"), missing


def mae_table(results):
    """All methods use exactly the same validated rows; no rowwise dropping."""
    return pd.DataFrame({"Method": list(METHOD_LABELS.values()),
                         "MAE (°C)": [float((results[field] - results.reported_delta_t_c).abs().mean())
                                      for field in METHOD_LABELS]})


def history_chart(measurements):
    """Reindex for gaps, never interpolate or turn unavailable months into zero."""
    indexed = measurements.set_index("date")[["reported_delta_t_c"]]
    return indexed.reindex(pd.date_range(indexed.index.min(), indexed.index.max(), freq="MS"))
