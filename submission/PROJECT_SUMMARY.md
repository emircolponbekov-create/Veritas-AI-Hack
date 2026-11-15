# Nuclear Water & Climate Lab
**Track:** AI + Climate · **Our own idea**  
**Team:** [PARTICIPANT 1 NAME] and [PARTICIPANT 2 NAME]

## The problem
A resident or student looking at an energy system's water use needs to distinguish reported cooling-water temperatures from model estimates and unsupported environmental claims. Our question is specific: can a simple model estimate a completed month's intake-to-discharge temperature difference better than two train-only median rules? This connects to the water side of energy-system climate adaptation; it does not measure greenhouse-gas reductions or establish a causal climate impact.

## What we built and added
An English Streamlit explorer starts with Surry's source-based environmental report. A three-stage cooling journey explains the process; one historical month ribbon shows checked intake/discharge temperatures, their difference and gaps. Each ecological statement has its reviewed source, period, scope and limitation. Availability labels distinguish ecological evidence, measurements, saved models and review needs. The ecological report uses curated sources and rules, not trained safety ML. Separate technical views preserve Ridge comparisons and explicit-input scenarios. Our contribution is the particular energy/water question, per-system evidence audit and honest comparison, with no environmental safety ranking.

## How it works
Public U.S. EIA-923 cooling-system data were obtained through Catalyst Cooperative PUDL. The frozen local registry covers 102 systems across 66 EIA plant IDs, not the world's nuclear fleet. Eligibility requires finite temperature pairs and an explicit continuous or interval thermometer method; conversions are Fahrenheit to Celsius. Suspicious measured rows are retained and flagged, not silently removed. Only 17 systems across 14 sites were admitted to model evaluation.

Each system has its own Ridge regression using same-month intake temperature and sine/cosine seasonality. Intake is available after the month, so this is retrospective estimation. Scaling, model fitting and both medians use train 2010–2021 only. A fixed alpha grid (0.1, 1, 10, 100) is selected on validation 2022–2023, before final test 2024–2025. Discharge temperature and current ΔT never enter the features. Systems are not pooled; Surry retains its original checked model.

## Results and failure
Saved exports independently verify 17 evaluated systems: Ridge beats the better median baseline in 4 and is worse in 13. No statistical significance or universal improvement is claimed. Surry CW1 has 22 common test months: Ridge MAE 1.849°C, overall median 1.995°C, seasonal median 2.045°C. Calvert Cliffs SYS042 has 24: Ridge 0.392°C, both medians about 0.301°C, so Ridge is worse by 0.091°C. The full system table is in RESULTS_AUDIT.md; some systems have only 12 test months.

For Surry in December 2025, measured ΔT is 6.667°C and the saved model estimate is 11.029°C: absolute error 4.362°C. Intake and season alone cannot represent every operational change; that is a possible explanation, not a proven cause of this error. Monthly averages also hide short-lived peaks. Cooling-system ΔT is not water-body warming, harm or safety for organisms or people, and is not transferable to Akkuyu.

## Contribution, next steps and sources
**[FILL IN the actual contribution of participant 1.]** **[FILL IN the actual contribution of participant 2.]** ChatGPT/Codex assisted data checks, code, tests and writing; the team must verify and explain the work. Next steps would be independent subject-matter review of flagged records and a separately defined, future evaluation period without reusing this test for tuning. Idealized mixing, volume heat-balance and literature lifecycle scenarios are separate sensitivity tools; uranium mining/milling calculations remain unavailable. Final participant details and submission access still need team verification.

Data: [EIA-923](https://www.eia.gov/electricity/data/eia923/) and [PUDL](https://github.com/catalyst-cooperative/pudl). Software: pandas, NumPy, scikit-learn, matplotlib, PyArrow and Streamlit. AI assistance: [OpenAI ChatGPT/Codex](https://openai.com/). Full attribution and licenses: CREDITS.md. Visible outputs in RESULTS_REVIEW.ipynb are a local review of saved artifacts, not a fresh training run.
