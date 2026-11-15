# Donald C Cook / UNIT1 evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: d79695d157c7166d787ff76f9e127e97c927070d847fcadacd4fc2abc419f84f
Splits: {'train': {'n': 70, 'start': '2016-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 12, 'start': '2024-01', 'end': '2024-12'}}
Selected Ridge alpha (validation only): 1.0

Test MAE (°C):
- median_baseline_delta_t_c: 1.111111
- seasonal_baseline_delta_t_c: 1.087963
- model_delta_t_c: 1.061511

Model beats both baselines: True
Worst error: {"report_month": "2024-11", "intake_temperature_c": 12.222222222222221, "reported_delta_t_c": 6.666666666666667, "median_baseline_delta_t_c": 11.666666666666666, "seasonal_baseline_delta_t_c": 11.38888888888889, "model_delta_t_c": 10.947021280917326, "absolute_model_error_c": 4.280354614250659}

Only 12 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
