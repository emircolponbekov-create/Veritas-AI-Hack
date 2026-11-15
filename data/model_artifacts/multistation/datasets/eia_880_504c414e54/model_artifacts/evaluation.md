# Quad Cities Generating Station / PLANT evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 144, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 10.0

Test MAE (°C):
- median_baseline_delta_t_c: 3.287037
- seasonal_baseline_delta_t_c: 1.111111
- model_delta_t_c: 1.361909

Model beats both baselines: False
Worst error: {"report_month": "2024-10", "intake_temperature_c": 16.666666666666668, "reported_delta_t_c": 15.555555555555555, "median_baseline_delta_t_c": 17.77777777777778, "seasonal_baseline_delta_t_c": 17.22222222222222, "model_delta_t_c": 18.788020364535676, "absolute_model_error_c": 3.2324648089801205}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
