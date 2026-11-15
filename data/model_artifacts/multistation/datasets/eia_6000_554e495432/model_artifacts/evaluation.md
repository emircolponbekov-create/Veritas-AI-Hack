# Donald C Cook / UNIT2 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 68, 'start': '2016-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 12, 'start': '2024-01', 'end': '2024-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 1.574074
- seasonal_baseline_delta_t_c: 1.250000
- model_delta_t_c: 1.383337

Model beats both baselines: False
Worst error: {"report_month": "2024-04", "intake_temperature_c": 8.88888888888889, "reported_delta_t_c": 12.777777777777779, "median_baseline_delta_t_c": 9.444444444444445, "seasonal_baseline_delta_t_c": 10.555555555555555, "model_delta_t_c": 10.058423982736011, "absolute_model_error_c": 2.7193537950417674}

Only 12 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
