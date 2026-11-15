# Credits, provenance and reuse

## Data

- **Source: U.S. Energy Information Administration, EIA-923**, reporting months 2010–2025; local snapshot collected 14 November 2026. [Data](https://www.eia.gov/electricity/data/eia923/), [Schedule instructions](https://www.eia.gov/survey/form/eia_923/instructions.pdf), [reuse policy](https://www.eia.gov/about/copyrights_reuse.php). EIA government data are generally public-domain materials; credit EIA. No EIA logos, photographs or endorsement are claimed.
- **Catalyst Cooperative, Public Utility Data Liberation (PUDL)**, cooling-system table `_core_eia923__monthly_cooling_system_information`, with plant-identity and nuclear-generation reference inputs. [Project and licensing](https://github.com/catalyst-cooperative/pudl), [data](https://data.catalyst.coop/), [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). PUDL data/documentation use CC BY 4.0; PUDL software uses MIT. These licenses do not automatically assign a license to our project's code.
- Exact original URLs, local file paths, selectors, limitations and SHA-256 hashes are in `data/incoming/collected-20261114-150548/INVENTORY.md` and `data/model_artifacts/multistation/registry.json`. Current nightly URLs may differ from our frozen bytes. We do not claim today's live source equals the snapshot.
- **Changes made to source data for analysis:** per-system selection; dates restricted to 2010–2025; explicit Fahrenheit-to-Celsius conversion; ΔT from discharge minus intake; measured-method eligibility; chronological splits. No missing targets were filled. Suspect measured values were retained with review-required status. Source files remain unchanged. The original producer/collector identity beyond the local audit is not invented.

## Software and references

| Tool | Use | Upstream license / link |
| --- | --- | --- |
| Python | Runtime | [PSF](https://docs.python.org/3/license.html) |
| pandas | Tabular data | [BSD 3-Clause](https://github.com/pandas-dev/pandas/blob/main/LICENSE) |
| NumPy | Numeric operations | [BSD 3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt) |
| scikit-learn | StandardScaler, Ridge, MAE; existing MODEL code | [BSD 3-Clause](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING) |
| matplotlib | Saved evaluation and review plots | [Matplotlib license](https://matplotlib.org/stable/project/license.html) |
| PyArrow | Local Parquet reads | [Apache 2.0](https://github.com/apache/arrow/blob/main/LICENSE.txt) |
| Streamlit | Local interactive explorer and AppTest | [Apache 2.0](https://github.com/streamlit/streamlit/blob/develop/LICENSE) |
| Google Colab | Optional notebook viewing/runtime | [Colab](https://colab.research.google.com/) |
| PowerShell / standard-library unittest | Local commands and verification | [PowerShell](https://github.com/PowerShell/PowerShell), [unittest](https://docs.python.org/3/library/unittest.html) |

Method/API references: [Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html), [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [Streamlit testing](https://docs.streamlit.io/develop/concepts/app-testing).
No external pretrained model or AI API is used for temperature estimates. Models are independent Ridge fits in the previously saved MODEL stage, not a foundation model.

## AI assistance and human accountability

**OpenAI ChatGPT / Codex**: assistance with data discovery/import/auditing, implementation of the model pipeline and UI, debugging, verification, explanations, design and submission drafts. [OpenAI](https://openai.com/), [Codex](https://openai.com/codex/). AI-generated outputs require review; the student team must understand the method, confirm its own contributions, and credit any additional tools actually used. Do not add an unverified model/version claim.

**Participant 1:** [NAME]; actual contribution: [FILL IN].  
**Participant 2:** [NAME]; actual contribution: [FILL IN].  
**Other actual sources/tools, if any:** [FILL IN OR REMOVE AFTER CHECKING].

The prototype's own reuse license has not been chosen by the team; none is silently granted here. Third-party packages are not vendored in the release; installers supply their license notices. No participant emails or schools are stored in this public-facing credit file; enter them privately in the official form.


## Added interface, evidence and scenario credits — 15 November

The coastal artwork was supplied by the user and is used as an illustrative
local asset, not a measured thermal map. Segoe UI/Bahnschrift are system font
stacks; no font binaries or third-party stock images are redistributed.
Cooling explanations reuse USGS Thermoelectric Power Water Use and PUDL's
cooling-type metadata; Surry's historical site account remains operator-authored.
Exact URLs, periods and locators are retained in
`src/model/site_support_data/journey.json` and the reviewed evidence catalog
`src/model/environment_evidence/source_catalog.json`. Claim disclosures reuse
those checked links rather than assigning generic citations to new statements.
Scenario references are IPCC AR5 Annex III Table A.III.2 and EPA CADDIS/heat
material listed in docs/SOURCES.md. They are not station emissions measurements.
ChatGPT/Codex also assisted the environmental-report integration, interactive
story views, accessibility adjustments, verification and local packaging.
