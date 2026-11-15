# McGuire / PLANT evaluation

Retrospective estimate; not an advance forecast.
Input SHA-256: 3074d20d655131c694987f2d69e4046b473655a26b692b65baeb9ee63bd952ba
Splits: {'train': {'n': 132, 'start': '2011-01', 'end': '2021-12'}, 'validation': {'n': 24, 'start': '2022-01', 'end': '2023-12'}, 'test': {'n': 24, 'start': '2024-01', 'end': '2025-12'}}
Selected Ridge alpha (validation only): 1.0

Test MAE (°C):
- median_baseline_delta_t_c: 0.925926
- seasonal_baseline_delta_t_c: 0.555555
- model_delta_t_c: 0.672334

Model beats both baselines: False
Worst error: {"report_month": "2025-02", "intake_temperature_c": 11.111111, "reported_delta_t_c": 10.0, "median_baseline_delta_t_c": 7.777778, "seasonal_baseline_delta_t_c": 8.888889, "model_delta_t_c": 8.60332611203069, "absolute_model_error_c": 1.3966738879693104}

Only 24 evaluated test months; one system, temporal dependence, coarse monthly reporting.
No confidence intervals or external-station validation. No causal/ecological/health inference.
Cooling-system delta T is not whole-waterbody warming. Do not transfer to Akkuyu.
