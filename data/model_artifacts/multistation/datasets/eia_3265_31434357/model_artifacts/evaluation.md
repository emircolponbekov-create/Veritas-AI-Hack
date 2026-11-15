# Oconee / 1CCW evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 144, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 0.995370
- seasonal_baseline_delta_t_c: 0.995370
- model_delta_t_c: 0.703784

Model beats both baselines: True
Worst error: {"report_month": "2024-11", "intake_temperature_c": 21.666666666666668, "reported_delta_t_c": 5.555555555555555, "median_baseline_delta_t_c": 9.444444444444445, "seasonal_baseline_delta_t_c": 9.166666666666668, "model_delta_t_c": 9.325737017059156, "absolute_model_error_c": 3.7701814615036007}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
