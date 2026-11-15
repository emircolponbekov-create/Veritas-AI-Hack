# Nuclear Water & Climate Lab

An interactive explorer of nuclear-power cooling water, historical measurements and environmental evidence.

Built for the **Veritas AI International High School Hackathon 2026**, track **AI + Climate**.

**Team:** Emir Cholponbekov and Umar Aldayarov.

[Project write-up](submission/PROJECT_SUMMARY.md) · [Results notebook](submission/RESULTS_REVIEW.ipynb) · [Credits](submission/CREDITS.md)

## The problem and user

For a resident or student exploring an energy system's water use, reported temperatures, model estimates and environmental claims can be difficult to distinguish. This prototype brings them together while keeping their evidence and limitations visible.

Our own question is whether a simple model can estimate a completed month's cooling-system temperature difference better than two median rules. The climate connection is energy-system water use and adaptation; this tool does not measure emissions reductions or prove a causal climate impact.

## Explore

- **Follow a drop:** a three-stage educational cooling journey, with explanations suited to the available cooling-type metadata.
- **A ribbon of months:** reported intake and discharge temperatures, differences and explicit data gaps, in degrees Celsius.
- **Why this conclusion?:** the source, observation period, scope and limitation behind an environmental statement.
- **Explore the details:** saved Ridge estimates, two simple baselines, error examples and clearly labelled hypothetical scenarios.

Start with **Surry / CW1**. Its environmental report contains partial historical evidence. Calvert Cliffs has an insufficient-evidence report; most other sites currently provide measurements or saved models rather than an environmental report.

## Run locally

Use Python 3.12 from the repository root. On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src/ui/app.py --browser.gatherUsageStats false
```

On macOS/Linux, use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.
Open the local URL printed by Streamlit. A localhost address is not a public demo link.
Viewing the bundled data needs no API key or model retraining. First-time dependency installation needs internet.
The review notebook additionally needs matplotlib; model development needs scikit-learn. The app and the checks below use the pinned runtime dependencies and do not train models.

## Verify the downloaded project

```powershell
.\.venv\Scripts\python.exe submission/verify_distribution.py --results
```

This checks original source/evidence hashes, the saved notebook outputs and all 17 saved model comparisons. Keep `.gitattributes`: the frozen files have byte-level manifests, so Git must preserve their original line endings on every operating system. A hash mismatch is an error to investigate, not a reason to regenerate the manifests.

## Model and results

The frozen registry covers **102 systems at 66 U.S. EIA plant IDs**. **17 systems at 14 sites** have evaluated Ridge exports.
Each model uses the completed month's intake temperature and calendar seasonality. This is retrospective estimation, not a forecast made before the month.

Training: 2010-2021. Validation: 2022-2023. Test: 2024-2025.
Scaling and both median baselines use training data only; the fixed Ridge parameter grid is selected on validation.
Ridge beats the better of the two baselines in **4 systems** and performs worse in **13**.

| Surry CW1, 22 test months | MAE, degrees C |
| --- | ---: |
| Ridge | 1.849 |
| Overall training median | 1.995 |
| Seasonal training median | 2.045 |

In December 2025, Surry's measured difference was 6.667 degrees C and the saved estimate was 11.029 degrees C: an absolute error of 4.362 degrees C.
[Full results](submission/RESULTS_AUDIT.md) and the [review notebook with saved outputs](submission/RESULTS_REVIEW.ipynb) include negative results. The notebook reviews saved artifacts; it does not represent a new training run.

## What the evidence can establish

Cooling-system temperature differences do not establish whole-water-body warming, ecological harm, health effects or safety.
Environmental reports use curated sources and rules; they are separate from the trained temperature models.
Evidence periods vary, specialist review has not been performed, and findings are not transferred to unstudied stations.
Process artwork is illustrative. Scenario calculations are hypothetical; uranium mining/milling estimates are unavailable without verified coefficients.

## Team contributions

- **Emir Cholponbekov:** Found datasets and prepared them for model training; built the website and was responsible for keeping it working.
- **Umar Aldayarov:** Wrote and reviewed code, trained the models and populated the GitHub repository.
- **Together:** Developed the project ideas, tested the prototype and worked together on recording the demo video.

## Next steps

Obtain independent subject-matter review of flagged measurements and ecological evidence. Evaluate any future model changes on a separately defined future period, without tuning on the current test set.

## Documentation

- [Project write-up](submission/PROJECT_SUMMARY.md)
- [Sources and provenance](docs/SOURCES.md)
- [Credits, tools and reuse terms](submission/CREDITS.md)
- [Data contract](docs/work/DATA_CONTRACT.md)
- [Multi-station model guide](src/model/MULTISTATION.md)
- [Interface guide](src/ui/README.md)
- [Scenario guide](src/fuel/README.md)
- [Code explanation](submission/CODE_WALKTHROUGH.md)
- [Submission checklist](submission/BEFORE_SUBMITTING.md)
- [Verification record](submission/VERIFICATION.md)

Enter participant emails and schools in the official form rather than this public repository.
Third-party data and software retain their own terms; no new project-wide reuse license is implied.

