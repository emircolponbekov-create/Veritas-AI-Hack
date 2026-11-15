# Current interactive UI — 15 November 2026

This section supersedes earlier UI and release status notes below. Contracts:
registry v2, evidence-report v1, story-support v1. No model fitting or source
search runs in the interface. No new runtime dependency was added.

Start with Surry CW1. The catalog labels environmental evidence, measurements,
saved models and review needs independently, including system counts. The
cooling-system selector is under **Cooling system and measurement coverage**.
The site report opens with **At a glance**, then Water / Animals & plants /
People / Climate / What is unknown. Essential scope and limitations stay beside
the statement; **Why this conclusion?** reveals its reviewed source, role,
period and locator. Source-free evidence gaps are labelled review boundaries.
CW1-specific statements are omitted for CW2. The report's evidence periods do
not change with the selected historical month.

**Follow a drop** has three keyboard-operable native stages and a local SVG.
Once-through, recirculating and unconfirmed metadata use different explanations;
recirculating cooling shows reuse and conditional release. This is a general
educational process illustration, never a pipe map, measured particle or plume.
Stage sources and historical metadata limits remain expandable.

**A ribbon of months** is the only month control. It covers 2010–2025, including
excluded or missing records, with verified intake/discharge/difference in °C.
Unavailable/review-blocked months have no replacement numbers. The selected
month is scoped by dataset; graphs preserve gaps. Saved estimates and baselines
stay separate under **Explore the details** with the original scenarios.

All main navigation destinations have headings even when data are unavailable.
**Reduce decorative motion** disables animation/fades/parallax, and the OS
reduced-motion preference is always respected. Native widgets support keyboard
selection. Captions, focus rings and mobile touch targets were strengthened.
There is no autoplay, polling, external API, safety score or ecological ranking.

## Run and check

From the project root in PowerShell:

```powershell
.\src\ui\.venv\Scripts\python.exe -m streamlit run src/ui/app.py --server.address 127.0.0.1 --server.port 8503 --browser.gatherUsageStats false
```

Open http://127.0.0.1:8503 after successful startup. If the environment is absent,
use `python -m venv src/ui/.venv`, then install `src/ui/requirements.txt` with
that interpreter. Initial installation needs network; normal data viewing is
offline. Do not stop another Work's server; choose another port if necessary.

Use the existing isolated-test workaround only where Windows socket setup
requires it: `VERITAS_UI_NO_SOCKET_TESTS=1`. It is never a production setting.
Run `python -B -m unittest discover -s tests/ui -v` with the UI interpreter.
MODEL read-only checks are `test_site_support.py` and `test_environment_report.py`;
scenario checks are under `tests/fuel`. Do not run broad MODEL discovery, which
includes training/writer tests. See submission/PACKAGE_CHECKS.json for actual
results and verification limits of this release.

The implementation pass visually checked desktop and 390 px width, evidence
expansion, keyboard stage/month selection and an excluded month. During the
finishing retry the browser connection timed out and localhost sockets were
denied (WinError 10013); a new server startup/health check was not confirmed.
This is not a claim of fresh visual QA. Repeat the checklist on the user's PC.

Read [STORY_UI_WALKTHROUGH_RU.md](STORY_UI_WALKTHROUGH_RU.md) for the code and
[../../submission/UI_CAPABILITIES.md](../../submission/UI_CAPABILITIES.md) for
the release scope. The older release ZIP is preserved; the current version is
`submission/nuclear-water-release-20261115-interactive.zip`. Other team materials still need final review.

---

Earlier notes (historical; the current section above takes precedence):

# Multi-station Water Impact — local Streamlit UI

## Impact scenarios — added 15 November 2026

A fourth tab contains explicit-input mixing and closed-volume heat balances,
a dated IPCC literature lifecycle scenario, and a user-documented thermal
reference comparison plus ecological evidence checklist. Calculations are
independent of the selected station and do not run ML or declare safety.
See `src/fuel/README.md` for equations, units, sources and boundaries.
Inputs are initially blank; no station flow, volume, generation or safe limit
is assumed. The new code is `impact_panel.py` and `src/fuel/scenarios.py`.
The previous packaged release does not include this extension.

## Design update

### Environmental report integration — 15 November 2026

The main screen now shows a checked English source-based report immediately
after site/system selection. This module is **curated evidence rules**, not a
trained ecological-safety model. UI calls the existing
`src.model.environment_report.read_report` and validates the public structure
and claim scope; it does not call `generate_report`, train, search or use APIs.

- **Surry / EIA 3806:** partial historical evidence, five original report
  sections, original paragraphs, mixed periods and source roles/limitations.
  The water-temperature statement covers **CW1 only**. Selecting CW2 does not
  transfer that statement to CW2. The report is site-level, not month-specific.
- **Calvert Cliffs / EIA 6011:** the real published `insufficient_evidence`
  report, with no Surry findings or source links.
- **Other sites:** no published report. Their checked temperatures and saved
  ML results remain accessible through **Show measurements, model results and
  scenarios** under **Explore the details**.

Contract: additive **evidence-report v1**, alongside unchanged registry v2.
Canonical publications:
`data/environment_reports/v1/eia_<plant_id_eia>/` containing `ready.json`,
`report.en.json`, `report.en.md` and `technical.json`. A publication must pass
the existing reader's identity/hash/stability checks plus UI schema/scope
checks. No UI report cache is used: **Refresh data** rereads these files.
The same checked snapshot is shared by the consumer report and technical audit.
Missing, invalid, incomplete, conflicting or temporarily unavailable reports
are withheld with plain messages; diagnostic logs contain only station/state/
stage codes. There is no previous-site fallback and no raw error text in the
report. Publishing a new version directory still needs an explicit sequential
update to the reader's `REPORTS` path; no automatic latest-version discovery or
new pointer format is invented here.

**Sources and limitations** has expandable groups for water, animals/plants
and climate. Dates distinguish evidence periods from compilation. General IPCC
context remains separate from Surry observations; an NRC-hosted operator
account remains labelled as an operator account. Specialist review has not
been performed. Existing metrics, comparison plots, scenarios, formulas and
technical provenance are preserved behind the details switch. Month selection
persists when that switch is closed. Scenario fields retain their existing
widget behavior and may reset if the entire technical section is closed.

Run from `D:\Projects\Veritas AI Hack`:

```powershell
.\src\ui\.venv\Scripts\python.exe -m streamlit run src/ui/app.py --server.address 127.0.0.1 --server.port 8503 --browser.gatherUsageStats false
```

Open http://127.0.0.1:8503 . If another UI server already owns that port, use it
and click **Rerun** after a file change rather than stopping somebody else's
process. This is a local address, not a published submission URL.

Checks actually completed: 24 UI/data tests (49.439 s, using the existing
test-only `VERITAS_UI_NO_SOCKET_TESTS=1` workaround), 10 existing evidence-module
tests, 5 existing scenario tests, and Python compilation. Browser inspection
in Chrome at desktop width and 390×844 checked the Surry report, its sources,
the technical model/scenario views, Calvert's insufficient-evidence state,
Donald C Cook's missing report with working measurements, and return to Surry.
No mobile horizontal overflow or visible traceback; consumer mode has no
technical metric cards. This visual check is distinct from AppTest. A separate
agent-API server attempt could not be reached from the sandbox and was stopped;
the existing ordinary :8503 app was verified through the connected browser.
No ty/mypy is installed, so no static type-check result is claimed.

Every changed code line is explained in
[ENVIRONMENT_INTEGRATION_WALKTHROUGH_RU.md](ENVIRONMENT_INTEGRATION_WALKTHROUGH_RU.md).
**The earlier release ZIP, manifest and submission prose are stale relative to
this integration.** They were not rebuilt or published in this UI task.

Earlier design notes below remain as history.

Typography refresh: Bahnschrift display headings with Segoe UI body/navigation,
buttons, tabular metric figures and chart labels. System font fallbacks are
provided; no font files redistributed or remote font requests added. Upright
lime emphasis replaces italic hero text. Desktop and 390 px mobile inspected
in Chrome without horizontal overflow; Python presentation module compiles.
Rendering on other operating systems depends on the listed system fallbacks.

### Coastal scene — current, 15 November 2026

The supplied coastal image is bundled at `assets/coastline.png` and embedded
locally. All controls, text and charts remain native interactive elements.
`water_scene.py` builds the decorative scene and measured charts; `motion.js`
mounts the trusted SVG (Streamlit sanitizes inline SVG), animates 16 particles,
water-masked glints and two plume ribbons, and handles restrained desktop
parallax. Intersection/visibility observers pause the scene outside the viewport
or in a hidden browser tab. Reduced motion disables effects. No polling or
Streamlit animation reruns occur. Observers/listeners are cleaned up on rerun.

Cards reveal once per page session. Changed metrics fade to their actual new
values; no interpolated values or artificial delay. Intake is turquoise and
discharge amber in cards and charts. Selected months have actual-value points
and a label. Missing months remain gaps. Source/data/model readers are unchanged.
Source details now follow the tabs, so the evidence CTA works from any tab.
React Aria selectors/tabs (Streamlit 1.67) have ocean/lime styling.

Verified: 15 existing UI/data tests pass (55.530 s), Python compilation and
JavaScript syntax checks; embedded PNG/SVG namespace/16-particle check passes.
Chrome at 1536×695 and 390×844: scene, navigation spacing, both CTAs, month
change (2025-12 to 2025-10), Surry CW2 withholding, Calvert Cliffs SYS042 and
model tab checked. Observed changing particle distance/plume opacity, desktop
parallax (~3 px), offscreen pause, and mobile parallax disabled/no horizontal
overflow. OS reduced-motion and hidden-tab pause are implemented but were not
independently exercised. Mobile viewport override reset after inspection.

Run from the project root:

```powershell
.\src\ui\.venv\Scripts\python.exe -m streamlit run src/ui/app.py --server.address 127.0.0.1 --server.port 8503 --browser.gatherUsageStats false
```

Open http://127.0.0.1:8503 . If an existing server says **File change**, click
**Rerun** to invalidate its imported presentation module. The background is
fixed artwork, never selected-station/month thermal data. Its caption is
“Illustrative scene · not a measured thermal map”. Image provenance: supplied
by the user, native file `libfile_1fca9bc013e88191a865c00697efb7b6`; downloaded
through Chrome after shell DNS failed. No third-party stock imagery was added.

Earlier design notes below are historical.

### Ocean refresh — 15 November 2026

The current theme is dark ocean / turquoise / lime, with glass-style metric
cards and the headline **Energy leaves a ripple.** `water_scene.py` contains a
local SVG illustration, moving current lines and a pulsing illustrative plume.
It is not a measured map or a geographic depiction of the selected plant.
Navigation anchors lead to the explorer, ecosystem context and climate scope.
The existing site/system/month selectors and all data gates remain unchanged.
Ocean-colored Altair charts include tooltips and a selected-month marker;
intake/discharge are monthly observations, with missing months kept as gaps.
Charts fade in on rerender; values do not interpolate between observations.
Cards have hover/fade effects. Reduced-motion preferences disable animations.
No new package or remote asset is required (Altair is supplied by Streamlit).
The climate section explains the calculator's excluded scope without numbers.

Verification: 15 UI/data tests passed with `VERITAS_UI_NO_SOCKET_TESTS=1`;
Python compilation passed. This pass could not access the local health endpoint
(socket access denied), and the browser reported connection refused. Desktop
and narrow-screen visual inspection remains unverified. Earlier health results
below describe the previous design pass.

### Previous design pass (historical)

The screen now uses a local light teal/navy stylesheet (`style.css`), a compact
selection row, temperature cards and three tabs: **Water overview**, **Model
performance**, **Sources & context**. A permanent note distinguishes system ΔT
from water-body heating. Technical provenance is collapsible; the model tab
includes the largest observed test error. Loaders, contracts and model artifacts
are unchanged. No extra packages, remote fonts or image services were added.

See [DESIGN_WALKTHROUGH.md](DESIGN_WALKTHROUGH.md) for the changed UI statements
and CSS rules, and [FINISH.md](FINISH.md) for the shortened completion workflow.
The design verification server uses port **8503** to avoid stopping another Work's
server. Its health endpoint returned HTTP 200. The 15 existing UI/data tests passed
with the documented test-loop workaround; browser appearance remains a manual
check because the browser tool could not initialize.

PowerShell, project root `D:\Projects\Veritas AI Hack`:

```powershell
.\src\ui\.venv\Scripts\python.exe -m pip install -r src/ui/requirements.txt
.\src\ui\.venv\Scripts\python.exe -m streamlit run src/ui/app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

If the environment is absent, first run `python -m venv src/ui/.venv`.
Open http://127.0.0.1:8501 . Keep the terminal open; stop with Ctrl+C.
If the port is occupied, use `--server.port 8502` and open that port.

## Read-only integration

The actual registry is `data/model_artifacts/multistation/registry.json`.
`multistation_loader.py` calls existing `src.model.registry.read_registry` and
`src.model.datasets.load_observations`; no Parquet preparation logic is copied.
It does not import the training pipeline or sklearn. Original CSV paths are
reused. Paths are resolved against the project root, not the terminal directory.

Select **Plant site**, then **Cooling system**. Names, IDs, source, limitations,
month options and model status come from the selected entry. Default: Surry
EIA 3806 / CW1. Month state is keyed by dataset, system state by plant.

| Registry data status | Display |
| --- | --- |
| ready_for_model_check | Validated eligible measurements; saved model only after export checks |
| measurements_only | Eligible source-reported measurements with limitations; Model not ready |
| review_required | Prominent reasons and review months; temperature cards/plots withheld |
| blocked / reference_only | Reasons; no temperature or model numbers |

`existing_verified` preserves Surry's legacy export. `evaluated_verified` uses
that system's registered export, metrics and verification sidecar. Other/missing
or inconsistent model artifacts produce **Model not ready** while valid
measurements remain visible. Eligibility alone does not override review status.

Every rerun reads fresh files: there is no UI data cache. **Refresh data** causes
a rerun without fitting anything. Registry SHA-256 is checked before and after
reads; selected source hashes are checked by MODEL's adapter. Result/metrics
hashes are checked before/after reading and against evaluation metadata for
new models. If publication overlaps a read, no partial model comparison is
shown; press Refresh data again. There is no automatic polling.

The UI requires all eligible test months, finite values, correct measured
intake/target joined by month and matching system identity. It independently
checks both baselines against train medians and recalculates all three MAEs on
identical rows, with N and dates. Saved metrics must agree within CSV rounding.
A model may be worse than the best baseline; the UI says so. No station safety
ranking, advance forecasts or claims of harm/safety are supported.

The old `data_loader.py` remains unchanged as a legacy validation utility;
`load_results` and `history_chart` are reused by the new UI. Its standalone
legacy partial-export function still returns missing months, but the new
snapshot wrapper refuses to display MAE for such exports.

## Checks

```powershell
.\src\ui\.venv\Scripts\python.exe -m compileall -q src/ui/app.py src/ui/data_loader.py src/ui/multistation_loader.py tests/ui
.\src\ui\.venv\Scripts\python.exe -m unittest discover -s tests/ui -v
```

In this execution environment normal Streamlit/AppTest initialization hung in
Windows asyncio socketpair creation before application execution. For isolated
synchronous AppTest checks only, use:

```powershell
$env:VERITAS_UI_NO_SOCKET_TESTS='1'
.\src\ui\.venv\Scripts\python.exe -m unittest discover -s tests/ui -v
Remove-Item Env:VERITAS_UI_NO_SOCKET_TESTS
```

That test flag substitutes a non-running AbstractEventLoop mock; it does not
mock the UI widgets, observation adapter, results or MAE calculations. It is
not a browser/server test and is never read by production UI code. Normal
server startup was attempted but could not be confirmed in this environment;
Chrome connection also timed out. Run the normal command on the user's PC.

## Manual checks

1. Initial Surry CW1: latest month 2025-12, measured ΔT 6.67°C, model 11.03°C;
   MAE Model 1.849 / Train median 1.995 / Train monthly median 2.045, N=22.
2. Calvert Cliffs SYS042: own measurements, N=24, model MAE 0.392°C;
   model worse than the best median by 0.091°C. Switch back to Surry: N=22.
3. Surry CW2: review warning, reasons, no temperature/model cards.
4. Pick a measurements_only system: measurements with limitations and Model
   not ready. Pick blocked/reference_only: reasons and no numeric substitution.
5. While MODEL publishes a result atomically, press Refresh data. Newly verified
   results should appear; missing/changing/inconsistent exports should show
   Model not ready. Do not alter real files just to simulate this case.
6. Select an earlier month outside test: historical measurements remain;
   No model estimate for this month. Historical gaps remain gaps.

Newly published-model behavior and missing/corrupt/concurrently changed files
are also covered by synthetic test state, without modifying project data.

See `UI_MULTISTATION_WALKTHROUGH.md` for every new/changed code line.
Do not transfer `.venv`, `__pycache__`, or local test/server evidence as source.
Credits: EIA, Catalyst Cooperative PUDL, pandas, NumPy, PyArrow, Streamlit;
ChatGPT/Codex for implementation and testing assistance.
