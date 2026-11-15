"""Retrospective Surry CW1 estimation; notebook cells share this source."""
# %% imports
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["intake_temperature_c", "month_sin", "month_cos"]
OUTPUT_FIELDS = ["report_month", "intake_temperature_c", "reported_delta_t_c",
                 "median_baseline_delta_t_c", "seasonal_baseline_delta_t_c",
                 "model_delta_t_c"]
ALPHAS = (0.1, 1.0, 10.0, 100.0)  # fixed before viewing test errors

# %% audit helpers
def require(condition, message):
    if not condition:
        raise ValueError(message)


def boolean_column(series):
    values = series.astype(str).str.lower().str.strip()
    require(values.isin(["true", "false"]).all(),
            f"Invalid boolean values in {series.name}")
    return values.eq("true")


def audit_data(csv_path):
    """Fail on ambiguous identity, target, units, methods, dates or eligibility."""
    frame = pd.read_csv(csv_path)
    required = ["report_month", "plant_id_eia", "cooling_id_eia", "split",
                "intake_temperature_f", "discharge_temperature_f",
                "intake_temperature_c", "discharge_temperature_c", "delta_t_c",
                "temperature_method", "temperature_value_class",
                "eligible_measured", "pair_available", "source_table"]
    require(set(required).issubset(frame.columns), "Required columns missing")
    require(len(frame) > 0, "Empty CSV")
    require(frame.report_month.astype(str).str.fullmatch(r"\d{4}-\d{2}").all(),
            "Months must use YYYY-MM")
    frame["date"] = pd.to_datetime(frame.report_month, format="%Y-%m", errors="raise")
    require(not frame.report_month.duplicated().any(), "Duplicate report_month")
    require(frame.plant_id_eia.eq(3806).all() and frame.cooling_id_eia.eq("CW1").all(),
            "Only Surry 3806 / CW1 is supported")
    require(frame.source_table.eq("_core_eia923__monthly_cooling_system_information").all(),
            "Unexpected source table; review provenance before training")
    frame = frame.sort_values("date").reset_index(drop=True)
    require(frame.date.between("2010-01-01", "2025-12-01").all(),
            "Date outside frozen 2010-2025 protocol")
    frame["eligible_measured"] = boolean_column(frame.eligible_measured)
    frame["pair_available"] = boolean_column(frame.pair_available)
    numeric = ["intake_temperature_f", "discharge_temperature_f",
               "intake_temperature_c", "discharge_temperature_c", "delta_t_c"]
    frame[numeric] = frame[numeric].apply(pd.to_numeric, errors="raise")
    require(np.isfinite(frame[numeric].to_numpy()).all(),
            "Missing/nonfinite temperatures: review input rather than filling targets")
    for point in ("intake", "discharge"):
        require(np.allclose(frame[f"{point}_temperature_c"],
                            (frame[f"{point}_temperature_f"] - 32) * 5 / 9,
                            atol=1.1e-6, rtol=0), "Fahrenheit/Celsius mismatch")
    require(np.allclose(frame.delta_t_c,
                        frame.discharge_temperature_c - frame.intake_temperature_c,
                        atol=1.1e-6, rtol=0), "Delta T arithmetic mismatch")
    measured = frame.temperature_method.eq("Measured continuously with a thermometer")
    require(frame.eligible_measured.eq(measured & frame.pair_available).all(),
            "Eligibility disagrees with verified measurement method")
    require(frame.loc[measured, "temperature_value_class"].eq("measured").all(),
            "Measurement classification mismatch")
    expected_split = np.where(frame.date.dt.year <= 2021, "train",
                              np.where(frame.date.dt.year <= 2023, "validation", "test"))
    require((frame.split == expected_split).all(), "Split disagrees with fixed dates")
    expected_months = pd.date_range("2010-01-01", "2025-12-01", freq="MS")
    audit = {
        "input_sha256": hashlib.sha256(Path(csv_path).read_bytes()).hexdigest(),
        "rows": len(frame), "columns": list(pd.read_csv(csv_path, nrows=0).columns),
        "period": [frame.report_month.min(), frame.report_month.max()],
        "missing_by_column": {k: int(v) for k, v in frame.isna().sum().items() if k != "date"},
        "duplicate_months": 0,
        "missing_calendar_months": expected_months.difference(frame.date).strftime("%Y-%m").tolist(),
        "temperature_methods": frame.temperature_method.fillna("MISSING").value_counts().to_dict(),
        "excluded_months": frame.loc[~frame.eligible_measured, "report_month"].tolist(),
        "ranges_c": {c: [float(frame[c].min()), float(frame[c].max())]
                     for c in ["intake_temperature_c", "discharge_temperature_c", "delta_t_c"]},
    }
    return frame, audit

# %% feature preparation
def make_features(frame):
    """Whitelist only inlet temperature and calendar; target cannot enter X."""
    month = pd.to_datetime(frame.report_month, format="%Y-%m").dt.month
    return pd.DataFrame({
        "intake_temperature_c": frame.intake_temperature_c.to_numpy(),
        "month_sin": np.sin(2 * np.pi * month.to_numpy() / 12),
        "month_cos": np.cos(2 * np.pi * month.to_numpy() / 12),
    }, index=frame.index)[FEATURES]


def prepare_splits(frame):
    eligible = frame.loc[frame.eligible_measured].copy()
    parts = {name: eligible.loc[eligible.split.eq(name)].copy()
             for name in ("train", "validation", "test")}
    require(all(len(part) > 0 for part in parts.values()), "A time split is empty")
    require(parts["train"].date.max() < parts["validation"].date.min()
            < parts["test"].date.min(), "Time splits overlap")
    require(parts["train"].date.dt.month.nunique() == 12,
            "Train needs every calendar month for seasonal baseline")
    return parts

# %% training (does not accept test)
def train_model(train, validation):
    X_train, X_val = make_features(train), make_features(validation)
    candidates, models = [], {}
    for alpha in ALPHAS:
        model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
        model.fit(X_train, train.delta_t_c)
        val_mae = mean_absolute_error(validation.delta_t_c, model.predict(X_val))
        candidates.append({"alpha": alpha, "validation_mae_c": float(val_mae)})
        models[alpha] = model
    # Deterministic tie break: first alpha in the predefined grid.
    chosen = min(candidates, key=lambda row: row["validation_mae_c"])
    median = float(train.delta_t_c.median())
    seasonal = train.groupby(train.date.dt.month).delta_t_c.median().to_dict()
    return models[chosen["alpha"]], median, seasonal, pd.DataFrame(candidates)

# %% evaluation (after selection is locked)
def predict_table(frame, model, median, seasonal):
    result = frame[["report_month", "intake_temperature_c"]].copy()
    result["reported_delta_t_c"] = frame.delta_t_c
    result["median_baseline_delta_t_c"] = median
    result["seasonal_baseline_delta_t_c"] = frame.date.dt.month.map(seasonal)
    result["model_delta_t_c"] = model.predict(make_features(frame))
    result = result[OUTPUT_FIELDS].reset_index(drop=True)
    require(np.isfinite(result.iloc[:, 1:].to_numpy()).all(), "Nonfinite output")
    require(not result.report_month.duplicated().any(), "Duplicate output month")
    return result


def score_table(result):
    return {name: float(mean_absolute_error(result.reported_delta_t_c, result[name]))
            for name in OUTPUT_FIELDS[3:]}


def plot_results(result):
    # Reindex calendar so excluded months remain gaps in all four curves.
    calendar = pd.date_range("2024-01-01", "2025-12-01", freq="MS")
    series = result.set_index(pd.to_datetime(result.report_month)).reindex(calendar)
    fig, ax = plt.subplots(figsize=(11, 4.5))
    labels = {"reported_delta_t_c": "Reported measurement",
              "median_baseline_delta_t_c": "Train median",
              "seasonal_baseline_delta_t_c": "Train monthly median",
              "model_delta_t_c": "Ridge estimate"}
    for field, label in labels.items():
        ax.plot(series.index, series[field], marker="o", markersize=3, label=label)
    ax.set(title="Surry CW1: retrospective cooling-system estimates (test only)",
           ylabel="Cooling-system delta T (°C)", xlabel="Reporting month")
    ax.grid(alpha=0.25)
    ax.legend(ncol=2)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

# %% export
def export_outputs(output_dir, csv_path, audit, parts, model, median, seasonal,
                   validation_scores, results, figure):
    output_dir = Path(output_dir)
    artifacts = output_dir / "model_artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    require(Path(csv_path).resolve() != (output_dir / "results.csv").resolve(),
            "Refusing to overwrite source CSV")
    results.to_csv(output_dir / "results.csv", index=False, encoding="utf-8", float_format="%.6f")
    audit["split_counts"] = {name: len(part) for name, part in parts.items()}
    audit["expected_split_counts_match"] = audit["split_counts"] == {
        "train": 142, "validation": 24, "test": 22}
    split_info = {name: {"n": len(part), "start": part.report_month.min(),
                         "end": part.report_month.max()} for name, part in parts.items()}
    scores = score_table(results)
    validation_result = predict_table(parts["validation"], model, median, seasonal)
    worst_index = (results.model_delta_t_c - results.reported_delta_t_c).abs().idxmax()
    worst = results.loc[worst_index].to_dict()
    worst["absolute_model_error_c"] = float(abs(worst["model_delta_t_c"] - worst["reported_delta_t_c"]))
    scaler, ridge = model.steps[0][1], model.steps[1][1]
    parameters = {"features": FEATURES, "scaler_mean": scaler.mean_.tolist(),
                  "scaler_scale": scaler.scale_.tolist(), "ridge_coef": ridge.coef_.tolist(),
                  "ridge_intercept": float(ridge.intercept_), "alpha": float(ridge.alpha),
                  "train_median_c": median,
                  "train_monthly_medians_c": {str(k): float(v) for k, v in seasonal.items()}}
    metrics = {"contract_version": "v1", "task": "retrospective_monthly_delta_t",
               "feature_availability": "Same-month inlet mean available after reporting; calendar known in advance. Annual Schedule 8D publication may lag further.",
               "split": split_info, "selected_alpha": float(ridge.alpha),
               "validation_candidates": validation_scores.to_dict(orient="records"),
               "validation_mae_c": score_table(validation_result), "test_mae_c": scores,
               "model_beats_both_baselines": bool(scores["model_delta_t_c"] < min(scores[k] for k in OUTPUT_FIELDS[3:5])),
               "test_months": results.report_month.tolist(), "worst_model_error": worst,
               "input_sha256": audit["input_sha256"],
               "versions": {"python": platform.python_version(), "pandas": pd.__version__,
                            "numpy": np.__version__, "scikit-learn": sklearn.__version__,
                            "matplotlib": plt.matplotlib.__version__},
               "seed": "None: deterministic Ridge; no shuffle or random sampling",
               "imputation": "None; temperatures must be finite; eligibility excludes unknown methods",
               "fit_policy": "Scaler, Ridge and both medians fitted on 2010-2021 only; alpha chosen on 2022-2023; no refit on validation/test"}
    for filename, value in [("audit.json", audit), ("metrics.json", metrics),
                            ("parameters.json", parameters)]:
        (artifacts / filename).write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")
    validation_scores.to_csv(artifacts / "validation_scores.csv", index=False)
    figure.savefig(artifacts / "test_predictions.png", dpi=160)
    errors = results.assign(absolute_model_error_c=(results.model_delta_t_c - results.reported_delta_t_c).abs())
    errors.to_csv(artifacts / "test_errors.csv", index=False)
    report = ["# Surry CW1 evaluation", "", "Retrospective estimate; not an advance forecast.",
              f"Input SHA-256: {audit['input_sha256']}", f"Splits: {split_info}",
              f"Selected Ridge alpha (validation only): {ridge.alpha}", "", "Test MAE (°C):"]
    report += [f"- {name}: {value:.6f}" for name, value in scores.items()]
    report += ["", "Model beats both baselines: " + str(metrics["model_beats_both_baselines"]),
               "Worst error: " + json.dumps(worst), "",
               f"Only {len(results)} evaluated test months; one system, temporal dependence, coarse monthly reporting.",
               "No confidence intervals or external-station validation. No causal/ecological/health inference.",
               "Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu."]
    (artifacts / "evaluation.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return metrics

# %% command line
def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/surry_cw1_monthly.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    args = parser.parse_args()
    frame, audit = audit_data(args.csv)
    parts = prepare_splits(frame)
    model, median, seasonal, validation_scores = train_model(parts["train"], parts["validation"])
    results = predict_table(parts["test"], model, median, seasonal)
    figure = plot_results(results)
    metrics = export_outputs(args.output_dir, args.csv, audit, parts, model, median,
                             seasonal, validation_scores, results, figure)
    print(json.dumps(metrics, indent=2))
    plt.close(figure)


if __name__ == "__main__":
    main()
