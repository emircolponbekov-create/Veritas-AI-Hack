# MODEL data support for three website features

Backend-only, 15 November 2026. Existing UI, registry, observations, Ridge models,
saved results and environmental publications are not modified. Contract is the
additive story-support v1 appendix in docs/work/DATA_CONTRACT.md.

## API: one snapshot per request/refresh

```python
from pathlib import Path
from src.model.site_support import SiteSupport, read_catalog
provider = SiteSupport(Path.cwd())  # run from the project root
journey = provider.journey('eia_3806_435731')
months = provider.timeline('eia_3806_435731')
estimates = provider.predictions('eia_3806_435731')
statements = provider.claim_details(3806, 'CW1')
catalog = read_catalog(Path.cwd())  # verifies the saved catalog dependencies
# After a legitimate data/publication change: create a NEW provider and call catalog().
```

`SiteSupport.catalog()` computes/validates catalog flags from actual files. The
saved catalog is an illustrative checked snapshot, not a replacement registry.
`read_catalog(root, relative_path)` refuses stale dependencies, including a
previously absent report that appears later. Rebuild without fitting models;
do not silently keep stale/foreign numbers. The provider's frame cache is only
inside that request; cached source hashes and registry version are rechecked.
Never retain a provider in st.cache_resource or session state across refreshes.

The two reused read-only verifiers currently live in src/ui: multistation_loader
and environment_loader. The backend imports those **existing pure reader modules**,
not app.py, environment_panel or Streamlit. A small import-path bootstrap supports
the legacy unqualified data_loader import. No reader/preparation algorithm is
copied and no UI file is edited. Include the existing readers on transfer.

## Identity and units

The site is plant_id_eia, while a system is exact dataset_id. The registry's
UTF-8 hex identity distinguishes CW1/CW2/PLANT and similarly named sites. Lookup
failure raises; there is no default-to-Surry fallback. Values come through
src.model.datasets.load_observations, which verifies original/raw hashes,
Fahrenheit-to-Celsius arithmetic, flags, methods, identity and unique months.
The timeline exposes Celsius while retaining source_units=degF. It does not
infer units from magnitude. Subtraction is the reported cooling-system
intake/discharge difference, not downstream or whole-river heating.

## Drop journey

Return fields: cooling_family, scheme_mode, cooling_type_codes, period, steps,
limitations. Steps have confirmed_for_system, general_explanation, sources,
unknowns; Surry can additionally have operator-attributed **site_context**.

- Historical metadata entirely within O/ON/OC/OF/OS selects once_through.
- Entirely within R/RC/RF/RI/RN selects recirculating: explain make-up water,
  cooling/reuse and only conditional release. Do not show the whole loop flowing
  directly into a river. Subtype/geometry are not inferred.
- Empty, unknown, dry/hybrid or mixed family codes select general_educational.
  The water illustration is explicitly hypothetical for that selected system,
  rather than asserting a direct-flow water design for every nuclear station.

Type metadata are historical, aggregated across source years, not current pipe
inspection and not per-month configuration. A selected-system code is a reported
family, not independent verification of the entire installation. The animation
must not imply that one measured droplet travelled along its geometry.

Primary sources actually read 15 November 2026:

1. PUDL2026.2 code metadata, cooling-system-type table:
   https://docs.catalyst.coop/pudl/en/v2026.2.0/data_dictionaries/codes_and_labels.html
   O=once-through nonspecified; ON/OC and recirculating codes in that table.
2. USGS Thermoelectric Power Water Use, “Cooling – A Primary Use”:
   https://www.usgs.gov/mission-areas/water-resources/science/thermoelectric-power-water-use
   Definitions of withdrawal/heat exchange/return versus cooling and recirculation.
3. Historical Surry **operator** applicant report section3.1.2.1, printed
   pp.3-2–3-5, https://www.nrc.gov/cdn/legacy/reactors/operating/licensing/renewal/applications/northanna-surry/surry_env.pdf
   Confirms site intake from the James River, condenser/service-water passage
   and a discharge canal. Exact publication date not established; no present-day
   inspection or assignment of an individual physical pipe to CW1/CW2 is claimed.

The old account says upriver return, while the read 2019 NRC **draft** says
downstream. Therefore **no direction, distance or plume route is used**; that
point needs site-specific review. A regulator-hosted operator document is not
an independent field measurement. No numerical flows, plume footprint, cooling
benefit, organism/population effect or safety verdict is produced by this API.

## Month ribbon and separate estimates

The fixed calendar is 2010-01 to2025-12. Each row has report_month,
intake_temperature_c, discharge_temperature_c, delta_t_c, record_present,
eligible_measured, pair_available, source_method, status, reasons, kind.

| status | Interpretation | Celsius fields |
| --- | --- | --- |
| verified_measurement | Source pair/method verified and dataset cleared for display | Original checked numbers |
| excluded_method | Not an explicit measured thermometer method | null |
| missing_temperatures | Incomplete/nonfinite pair | null |
| missing_month | No source row for that month | null |
| review_required | Dataset retained but unresolved values require review | null; original eligibility remains visible |
| blocked | Blocked/reference-only dataset cannot supply confirmed display | null |

An unreadable/changed source returns source_unavailable with **no rows**, not
invented missing months. No interpolation, zero fill or synthetic measurements.
Measurements_only rows can be displayed with their existing scheme/coverage
limitations; this does not qualify them for a model or ecological conclusion.

`predictions()` uses the existing verified_results function: exact eligible test
months, independent baseline/MAE checks, identity and artifact hashes. All saved
model/baseline rows have kind=model_estimate and a retrospective label. Nothing
is appended to measurement rows. No export or verified model => empty estimates
with model_not_ready; broken advertised results => results_unavailable. Surry
has22 test months; Calvert has24. No estimate is invented for an excluded month.

## Why this statement? Companion spans, not replaced reports

Original report v1 is untouched. site_support_data/claim_links.json adds25
semantic, stable statement IDs for Surry's summary and every section paragraph.
Text positions are references into the exact hash-bound publication, not IDs;
semantic IDs must be retained when the same reviewed proposition moves. After
text edits, re-review spans/sources before changing the companion hash index.

Each statement has standalone statement, display_span, target/paragraph_index/
span, parent_claim_ids, evidence_kind, text_role, sources with roles/locations,
period, geography, scope, limitation, review_basis and counterevidence.
The evidence_kind refers to the accepted parent evidence; text_role determines
whether the displayed span is a factual claim or a review/method boundary.
A scope_limit is not an observation merely because its parent is observational.

- source_fact requires an accepted parent claim and reviewed source location.
  General IPCC facts have scope=general and geography=global, not a Surry finding.
- scope_limit/evidence_gap/method_explanation explicitly describe the limits
  of our reviewed collection or method. Source-free gap statements are **not**
  newly measured facts and point to the existing local review document.
- Every nonspace character of summary/section paragraphs must be covered once.
  Wrong/missing/overlapping spans, unread sources, changed versions or unknown
  citations return review_required with no statement cards.
- A single report paragraph is split where evidence differs. VDH's H3
  observation links to the sample table/location, while the separate nondetection
  explanation links to page10. We do not give the table citation to a health
  inference or imply that every sentence in the paragraph was measured.
- Operator's historical population statement remains attributed; individual
  capture versus no detected population decline remain different endpoints.
- At selected CW2, three CW1-specific statements are omitted and their IDs
  listed. Remaining site-level facts are **site context**, not impacts attributed
  to CW2. General context is not attributed to any cooling system.

Calvert's real insufficient publication and Brunswick's absent publication
return honest states and no Surry cards. No report generator, source search,
new statement training or paid API is called during reads.

## Catalog flags may coexist

Plant flags: has_substantive_environment_report, has_insufficient_evidence_report,
report_state, expert_review_status, system_count, verified_measurement_systems,
verified_model_systems and any_system_* aggregates. Substantive requires reviewed
site observations/assessments and verified annotation wiring, not a model flag,
filename or purely general-context passage.

System flags: has_verified_measurements, verified_measurement_months,
has_verified_model_results, model_result_months, requires_review, data_blocked,
no_temperature_pairs, measurement_state, model_state, limitations. These are
technical availability flags, never a safety ranking or complete-site coverage.

Current checked snapshot:66 sites/102 systems;38 systems expose verified
measurements (17 model-evaluable +21 measurements_only),17 have verified model
results. Surry combines one substantive site report, one model, and a different
system requiring review. Calvert combines an insufficient-evidence report with
a valid measured dataset/model. Brunswick has three registered systems, two
models and no approved ecological publication. Exact counts are checked values
for this snapshot, not assumptions to force future data to match.

## Examples, tests and limits

`data/site_support/v1/catalog.json` plus four identity-named example JSON files
show Surry CW1/CW2, Calvert SYS042 and Brunswick PLANT (unknown metadata example).
They are new illustrative payloads, not competing source CSVs or model exports.

```powershell
.\src\ui\.venv\Scripts\python.exe -B -m unittest discover -s tests/model -p test_site_support.py -v
.\src\ui\.venv\Scripts\python.exe -B -m unittest discover -s tests/model -p test_environment_report.py -v
```

See SITE_SUPPORT_WALKTHROUGH_RU.md for every new code/test line. Existing MODEL
verification and UI/environment-reader tests can be used without fitting. Do not
run broad training/preparation test discovery. Runtime imports no sklearn/model.py
and calls no fit. This task does not perform browser/animation QA, UI integration,
hydrodynamic validation or expert health/ecology assessment. Source review is
scoped to the indicated passages; programmatic checks cannot establish scientific
truth merely from a URL. Existing environmental expert-review status remains
not_performed. Global documents and the old release ZIP are not refreshed.
