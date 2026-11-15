# Independent saved-results audit

Local review only; no training or parameter selection. All MAE values are °C. Each row compares three methods on identical eligible test months for that system. The table is not an ecological ranking.

| Plant / system | Train / validation / test | Ridge MAE | Overall median MAE | Seasonal median MAE | Ridge vs best baseline |
| --- | --- | --- | --- | --- | --- |
| Quad Cities Generating Station / PLANT | 144/24/24 | 1.361909 | 3.287037 | 1.111111 | Worse |
| PSEG Salem Generating Station / NSS2 | 132/24/24 | 1.179570 | 1.064815 | 1.064815 | Worse |
| Nine Mile Point Nuclear Station / U1 | 132/24/24 | 1.149599 | 1.157407 | 1.157407 | Better |
| Peach Bottom / PLANT | 144/24/24 | 1.017679 | 1.319444 | 0.879630 | Worse |
| Oconee / 1CCW | 144/24/24 | 0.703784 | 0.995371 | 0.995370 | Better |
| Surry / CW1 | 142/24/22 | 1.849330 | 1.994950 | 2.045454 | Better |
| Point Beach Nuclear Plant / CW | 144/24/24 | 1.505864 | 1.921296 | 0.902777 | Worse |
| Point Beach Nuclear Plant / CW2 | 108/24/24 | 2.020413 | 3.194445 | 1.342593 | Worse |
| Donald C Cook / UNIT1 | 70/24/12 | 1.061511 | 1.111111 | 1.087963 | Better |
| Donald C Cook / UNIT2 | 68/24/12 | 1.383337 | 1.574075 | 1.250000 | Worse |
| Calvert Cliffs Nuclear Power Plant / SYS042 | 120/24/24 | 0.391877 | 0.300926 | 0.300926 | Worse |
| Brunswick Nuclear / 1 | 132/24/24 | 1.487265 | 1.458333 | 1.273148 | Worse |
| Brunswick Nuclear / 2 | 132/24/24 | 1.744533 | 1.759259 | 1.527778 | Worse |
| McGuire / PLANT | 132/24/24 | 0.672334 | 0.925926 | 0.555555 | Worse |
| St Lucie / SLC | 144/24/24 | 0.751729 | 0.486111 | 0.393519 | Worse |
| Diablo Canyon / PLANT | 142/24/24 | 0.535444 | 0.347222 | 0.416667 | Worse |
| R E Ginna Nuclear Power Plant / 1 | 132/24/24 | 1.117355 | 1.180556 | 0.532407 | Worse |

17 evaluated systems across 14 sites; 4 better and 13 worse. This includes Surry CW1, which was not retrained. The three new-model improvements are Nine Mile Point U1, Oconee 1CCW and Donald C Cook UNIT1. Their gains and the count are descriptive, not statistically significant findings.

Input registry SHA-256: `decbc418729de40b6a0563de0673456a1de1147c1eeeec40677dd448d2104896`. Exact recomputed values are in VERIFICATION.json. Comparison checks include all eligible test months, finite outputs, source intake/target agreement, train-only median agreement, saved MAE agreement and system/artifact hashes.

Surry December 2025: measured 6.666667°C; estimate 11.028858°C; absolute error 4.362191°C. Operational changes are a possible missing influence, not a verified diagnosis.

Existing checks actually run: 15 UI/data tests (43.621 s, test-only non-running event-loop mock) and 5 saved-model verification tests (27.304 s), all passed. Those mocks do not replace measurements, results or metric calculations. No claim of browser visual QA is made.

Known preparation regression caveat: the old test_repeated_preparation_has_identical_bytes_and_mtime targets the pre-training registry and calls a writer. It was not run after evaluated statuses were published. Do not rerun prepare_registry or the legacy training notebook simply to obtain a green test suite.
