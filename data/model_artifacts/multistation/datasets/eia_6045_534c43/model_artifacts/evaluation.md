# St Lucie / SLC evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 144, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 0.486111
- seasonal_baseline_delta_t_c: 0.393519
- model_delta_t_c: 0.751729

Model beats both baselines: False
Worst error: {"report_month": "2024-10", "intake_temperature_c": 27.22222222222222, "reported_delta_t_c": 11.666666666666666, "median_baseline_delta_t_c": 13.333333333333334, "seasonal_baseline_delta_t_c": 12.5, "model_delta_t_c": 12.97155072186156, "absolute_model_error_c": 1.3048840551948935}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
