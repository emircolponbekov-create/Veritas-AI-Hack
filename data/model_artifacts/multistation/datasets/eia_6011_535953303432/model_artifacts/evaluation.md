# Calvert Cliffs Nuclear Power Plant / SYS042 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: 5646ef0c7bf57df44173a3d271f0b0d53f7839ade742d019a8f156ea1084a3f9
Splits: {'train': {'n': 120, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 0.300926
- seasonal_baseline_delta_t_c: 0.300926
- model_delta_t_c: 0.391877

Model beats both baselines: False
Worst error: {"report_month": "2025-03", "intake_temperature_c": 6.666667, "reported_delta_t_c": 6.666667, "median_baseline_delta_t_c": 6.111111, "seasonal_baseline_delta_t_c": 6.111111, "model_delta_t_c": 5.823194229957724, "absolute_model_error_c": 0.8434727700422764}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
