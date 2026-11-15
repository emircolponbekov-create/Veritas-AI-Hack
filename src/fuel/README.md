# Impact scenarios — scope and verification

User-authorized extension, 15 November 2026. These are explicit-input physical
and literature scenarios, separate from ML. They do not determine actual
ecological damage, legal compliance, human health or plant safety.

UI: **Impact scenarios**, with Mixing / Water-body heat balance / Lifecycle
emissions / Ecological evidence. Inputs are initially blank and independent
of the selected station. No default flow, volume, limit or generation is
invented. Source/ML files are not changed. Requires no new package.

`CODE_WALKTHROUGH.md` explains each nonblank line of both new modules.

## Equations and assumptions

- Mixing: `(Qa*Ta + Qd*Td)/(Qa+Qd)`. Two distinct simultaneous streams of
  equal constant density/heat capacity, steady complete adiabatic mixing.
  Qa is bypass flow excluding the discharge, not total upstream flow before
  a withdrawal. No tides, stratification, recirculation or plume geometry.
- Closed box: `flow * system_delta * hours * 3600 / volume`. A fixed, perfectly
  mixed water volume recirculated through a constant-ΔT cooling system. No
  added water, atmosphere, heat losses, evaporation, natural exchange or
  varying heat capacity. Not a validated real-waterbody forecast or general
  upper bound. Constant-load long-duration results may be nonphysical.
- Lifecycle: `generation_TWh * factor_g_per_kWh * 1000` tonnes CO2e. IPCC AR5
  final Annex III Table A.III.2 nuclear min/median/max 3.7/12/110. A 2014
  literature scenario, not a station emissions inventory or confidence
  interval. Includes lifecycle; do not add mining emissions again.
- Reference comparison: entered temperature minus an entered documented
  reference. Source/applicability declaration is user-provided, not verified
  by the app. No automatic safe-temperature limit or compliance verdict.

Real site assessment additionally needs locations/depths and temperature
time series, synchronized flows, geometry/tides/weather, species and life
stages, season/exposure, oxygen/chemistry and appropriate monitoring records.
Monthly mean products are not generally mean heat fluxes. Health/radiological
safety requires a separate assessment. EPA/IPCC links are recorded in
docs/SOURCES.md and displayed in the UI.

## Tests

```powershell
.\src\ui\.venv\Scripts\python.exe -B -m unittest discover -s tests/fuel -v
.\src\ui\.venv\Scripts\python.exe -B -m unittest discover -s tests/ui -v
```

Five arithmetic tests cover heat conservation, limiting cases, signs, unit
conversion, invalid/missing/nonfinite inputs and overflow. One new UI test
covers blank states, all three calculations and the reference source gate.
Existing fifteen UI/data checks were also executed successfully.

Browser examples verified: mixing 20/30 °C and 90/10 m³/s ->21 °C (+1 °C);
generation 1 TWh ->12000 t CO2e at the literature median. These are explicitly
illustrative inputs, not Surry observations. Do not use them as demo site facts.

The earlier release archive and submission text require refresh before these
features can be submitted. Models, feature selection and evaluation stay fixed.
