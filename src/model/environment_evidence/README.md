# Evidence-based environmental reports — offline pilot

This is **curated report-generation rules**, not a trained ecological-safety model.
No external API/network call or fitting is performed. Existing Ridge is neither
changed nor invoked; it remains a retrospective cooling-system delta estimator.

## Run and connect later

From the project root with the existing UI Python environment (pandas/NumPy/PyArrow):

```powershell
.\src\ui\.venv\Scripts\python.exe -B -m unittest discover -s tests/model -p test_environment_report.py -v
.\src\ui\.venv\Scripts\python.exe -B -m src.model.environment_report --plant-id 3806 --output data/environment_reports/new-review/eia_3806
```

Use a **new** output directory. Export refuses overwrite. Existing examples:
`data/environment_reports/v1/eia_3806/` and `.../eia_6011/`.
Programmatic use (no writes): `generate_report(root, plant_id)` returns a public
report and a separate technical audit; `markdown(report)` renders the body;
`read_report(directory, expected_plant_id)` checks completed publication hashes.
No Streamlit import/UI code exists in this module.

Read DATA_CONTRACT's additive evidence-report v1 section before connecting UI.
Select the site by EIA ID; keep source-level cooling-system scope and periods.
Calvert Cliffs has temperature/model data elsewhere, but no approved eco-evidence
in this module: its report correctly refuses broader environmental conclusions.
No Surry sentence, source or general-context claim is carried into that refusal.

## Evidence files and fields

- `source_catalog.json`: exact URLs, titles, author role, scope, access state,
  publication/date uncertainty, retrieval method, license caveats and origin.
- `claims.json`: per-claim place/time/type, plain text, support location/review,
  limitations, polarity, counterevidence/conflict and explicit rejection reasons.
- `technical_values.json`: checked table values/units, never a health verdict.
- `review_index.json`: hashes of the curated records after support review;
  not a cryptographic authority or scientific truth certificate.
- `CAPABILITY_AUDIT_RU.md`: six-domain matrix, bounded dataset search, source
  access failures/draft distinction and the expert-review backlog.
- `CODE_WALKTHROUGH_RU.md`: every delivered code/test line explained in blocks.

Accepted source-derived factual statements are the CW1 monthly water difference,
a 2024 state tritium observation, and historical intake capture/survival.
The operator's old population statement is explicitly attributed and is not
independent proof of no harm. IPCC supply-chain comparison is general context
only; no station-specific avoided-emissions number is produced. No measured
benefit/harm to human health, land plants/animals or current conditions is claimed.
A substantive final NRC 2020 body could not be read; a 2019 draft was identified
and not promoted to a final/current finding. Both rejected claims remain in the
technical audit rather than the public report.

## Extending a station without copying code

1. Use its existing integer plant ID. Research the actual site/waterbody/period.
2. Register primary sources with author/operator distinction and exact pages.
3. Curate station-specific claims and a plain-language profile/limitations.
   Do not copy Surry's conclusions or use LLM output as outcome labels.
4. Check every claim against source content; record contradictory material,
   publication/observation dates, gaps, licensing and expert-review needs.
5. Resolve direct conflicts before publication; review local index changes.
6. Run focused tests, generate into a new directory, inspect the consumer text
   and technical audit. New output status never becomes a safety label.

An arbitrary station cannot become "approved" merely by adding a URL. Technical
checks enforce provenance gates; only actual source review can establish support.
The pilot's support review was performed by Codex, not a specialist panel.

## Storage and scope

Source PDFs were read using public text/rendering services; no full applicant/IPCC
PDF is redistributed and no state-document copyright assumption is made. Runtime
report generation is fully local. UI, original CSV/Parquet, registry, MODEL code
and checked ML results are preserved. New sources are proposed in this module and
its handoff, rather than overwriting a concurrently maintained global SOURCES.md.
The report source citations are independently readable, but current download
availability of every historical URL is not guaranteed.
