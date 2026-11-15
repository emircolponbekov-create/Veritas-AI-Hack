# R E Ginna Nuclear Power Plant / 1 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 132, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 1.180556
- seasonal_baseline_delta_t_c: 0.532407
- model_delta_t_c: 1.117355

Model beats both baselines: False
Worst error: {"report_month": "2025-02", "intake_temperature_c": 0.0, "reported_delta_t_c": 17.77777777777778, "median_baseline_delta_t_c": 12.222222222222221, "seasonal_baseline_delta_t_c": 15.555555555555555, "model_delta_t_c": 13.12945360650634, "absolute_model_error_c": 4.6483241712714385}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
