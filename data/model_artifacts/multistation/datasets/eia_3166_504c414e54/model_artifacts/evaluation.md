# Peach Bottom / PLANT evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: cc9e19be16a456956c6a3c99771857c35818359a90b4f719f1df54ae5b98f0b0
Splits: {'train': {'n': 144, 'start': '2010-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 100.0

Test MAE (°C):
- median_baseline_delta_t_c: 1.319444
- seasonal_baseline_delta_t_c: 0.879630
- model_delta_t_c: 1.017679

Model beats both baselines: False
Worst error: {"report_month": "2025-01", "intake_temperature_c": 1.666667, "reported_delta_t_c": 20.0, "median_baseline_delta_t_c": 12.777778, "seasonal_baseline_delta_t_c": 15.0, "model_delta_t_c": 14.017427735516332, "absolute_model_error_c": 5.982572264483668}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
