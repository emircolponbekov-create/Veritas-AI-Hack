# Surry CW1 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: 49d0ccdb17bd32e1155a6001fac24d19785851fe1280d157098788ac1289c82a
Splits: {'train': {'n': 142, 'start': '2010-01', 'end': '2021-11'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 22, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 1.994950
- seasonal_baseline_delta_t_c: 2.045454
- model_delta_t_c: 1.849330

Model beats both baselines: True
Worst error: {"report_month": "2025-12", "intake_temperature_c": 6.111111, "reported_delta_t_c": 6.666667, "median_baseline_delta_t_c": 10.0, "seasonal_baseline_delta_t_c": 10.555556, "model_delta_t_c": 11.02885792369898, "absolute_model_error_c": 4.36219092369898}

Only 22 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
