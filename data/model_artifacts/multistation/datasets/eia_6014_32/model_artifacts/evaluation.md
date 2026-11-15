# Brunswick Nuclear / 2 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 132, 'start': '2011-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 0.1

Test MAE (°C):
- median_baseline_delta_t_c: 1.759259
- seasonal_baseline_delta_t_c: 1.527778
- model_delta_t_c: 1.744533

Model beats both baselines: False
Worst error: {"report_month": "2025-03", "intake_temperature_c": 17.22222222222222, "reported_delta_t_c": 3.3333333333333335, "median_baseline_delta_t_c": 16.11111111111111, "seasonal_baseline_delta_t_c": 15.555555555555555, "model_delta_t_c": 12.987879608630372, "absolute_model_error_c": 9.654546275297038}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
