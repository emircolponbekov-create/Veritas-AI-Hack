# Point Beach Nuclear Plant / CW evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 144, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 0.1

Test MAE (°C):
- median_baseline_delta_t_c: 1.921296
- seasonal_baseline_delta_t_c: 0.902778
- model_delta_t_c: 1.505865

Model beats both baselines: False
Worst error: {"report_month": "2025-04", "intake_temperature_c": 6.666666666666667, "reported_delta_t_c": 10.0, "median_baseline_delta_t_c": 11.11111111111111, "seasonal_baseline_delta_t_c": 11.944444444444443, "model_delta_t_c": 14.60177805397594, "absolute_model_error_c": 4.60177805397594}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
