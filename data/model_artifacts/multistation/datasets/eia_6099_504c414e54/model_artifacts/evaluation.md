# Diablo Canyon / PLANT evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: 61229722dcd81fe81926758755993ff7c28da43b6e8713157814dcf0c5ae9d87
Splits: {'train': {'n': 142, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 0.1

Test MAE (°C):
- median_baseline_delta_t_c: 0.347222
- seasonal_baseline_delta_t_c: 0.416667
- model_delta_t_c: 0.535444

Model beats both baselines: False
Worst error: {"report_month": "2024-08", "intake_temperature_c": 12.222222, "reported_delta_t_c": 11.666667, "median_baseline_delta_t_c": 10.555556, "seasonal_baseline_delta_t_c": 10.555556, "model_delta_t_c": 10.19107181579605, "absolute_model_error_c": 1.47559518420395}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
