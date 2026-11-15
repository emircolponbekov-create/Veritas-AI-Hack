# Nine Mile Point Nuclear Station / U1 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 132, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 1.157407
- seasonal_baseline_delta_t_c: 1.157407
- model_delta_t_c: 1.149599

Model beats both baselines: True
Worst error: {"report_month": "2025-03", "intake_temperature_c": 4.444444444444445, "reported_delta_t_c": 13.333333333333334, "median_baseline_delta_t_c": 17.22222222222222, "seasonal_baseline_delta_t_c": 16.11111111111111, "model_delta_t_c": 16.15985225370551, "absolute_model_error_c": 2.826518920372175}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
