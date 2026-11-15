# Sources — integrated release evidence, 14 November 2026

## Scenario extension — 15 November 2026 (user-authorized scope expansion)

- IPCC **AR5 WGIII (2014), final Annex III, Table A.III.2**, Nuclear row,
  lifecycle emissions minimum / median / maximum: **3.7 / 12 / 110 g CO2e/kWh**.
  https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf .
  Final official table values retrieved through indexed primary-source text on
  2026-11-15; direct PDF open returned 403. Not the final-draft document.
  Used only as a dated generic lifecycle scenario, not station observations,
  a probability interval, an operational inventory or a mining-only coefficient.
  Unit conversion: TWh × g/kWh × 1000 = tonnes CO2e.
- EPA, **Thermal Discharges in NPDES Permits: Overview of Resources and Tools**,
  June 2023: https://www.epa.gov/system/files/documents/2023-07/Thermal-Discharges-Report.pdf .
  Primary text retrieved 2026-11-15. Supports the need for flow/mixing geometry
  and site models; it does not validate our simple scenario for a real site.
- EPA CADDIS, **Temperature**: https://www.epa.gov/caddis/temperature .
  Primary page read 2026-11-15. Temperature is a candidate stressor requiring
  site and biological evidence; flow, oxygen and other factors matter.
- Two-stream equation is a derived equal-property, steady, adiabatic heat
  balance; closed-volume equation is a derived perfectly mixed constant-volume
  recirculating box with constant heat input and no losses/natural exchange.
  Neither is calibrated or spatially validated. No numeric safe-temperature,
  health, radionuclide or uranium/mining factor is supplied.

The earlier release scope below remains historical. These new scenarios are
not yet included in the old release ZIP or its submission claims.

Current evidence is listed first; the initial scaffold document is preserved verbatim below as history.

## Public data and frozen local paths

- EIA-923 monthly cooling-system information through Catalyst Cooperative PUDL: `_core_eia923__monthly_cooling_system_information`. [EIA-923](https://www.eia.gov/electricity/data/eia923/), [instructions](https://www.eia.gov/survey/form/eia_923/instructions.pdf), [PUDL](https://github.com/catalyst-cooperative/pudl).
- Actual inputs: data/incoming/collected-20261114-150548/raw/{cooling,entity_plants,nuclear_generation}.parquet; six original CSVs in its station_csv/; legacy data/surry_cw1_monthly.csv. Exact selectors/URLs/hashes: data/model_artifacts/multistation/registry.json and incoming INVENTORY.md. They are local frozen inputs, not new downloads in this pass. Registry covers 102 systems/66 EIA IDs, with no global completeness claim.
- Original mean intake/discharge fields are Fahrenheit; C=(F−32)×5/9; ΔT=(F_out−F_in)×5/9. They are cooling-system monthly means, not downstream water-body temperature or temperature maxima. Source method must exactly match continuous/interval thermometer after trimming; eligible flags are independently checked by the existing adapter.
- Inputs with suspicious measured values remain review_required, not cleaned by model error. Missing temperatures stay missing. Raw inputs and saved Surry results are unchanged. Some existing provenance points to moving nightly URLs: hashes identify our bytes; no assertion that the online object is unchanged.

## Licensing, rechecked against primary sources

- [EIA reuse policy](https://www.eia.gov/about/copyrights_reuse.php): government data are generally public domain; acknowledge EIA, with reporting/source dates. No endorsement, logo or licensed imagery rights are implied.
- [PUDL licensing](https://github.com/catalyst-cooperative/pudl): data/documentation CC BY 4.0, software MIT; [license](https://creativecommons.org/licenses/by/4.0/). Attribution: U.S. Energy Information Administration / Catalyst Cooperative PUDL, reporting years 2010–2025, local collection 14 November 2026. Project transformations are system/date selection, measured-method eligibility, unit conversion, derived ΔT, chronological splits and model estimates. Preserve these explanations when sharing the derived tables.
- Our own code license has not been chosen. Do not infer it from PUDL's software license. Library links/licenses and actual tool roles are in submission/CREDITS.md; packages are not vendored.

## Rules, AI and scientific limits

Official Project Briefs PDF, Drive ID 15tYD48XRmCgWbk1_lLDtc8lebi6qm-4-, reread through connected Drive during this pass; sections 2/3/4.3/5/6 support the submission checklist. AI + Climate uses our own energy/water question, not a causal emissions or ecosystem-health calculation.

ChatGPT/Codex assisted data discovery/import/auditing, MODEL/UI code, debugging, tests, explanations, design and writing. Actual libraries: Python, pandas, NumPy, scikit-learn, matplotlib, PyArrow and Streamlit. No pretrained temperature model or external inference API. Google Colab is optional; PowerShell and unittest support local checks. Real participant contributions remain for the team to fill in.

No numerical uranium/mining/milling coefficient has been verified here; Fuel & Climate remains outside the release. No safety, health, downstream mixing, worldwide coverage, future forecast or statistical significance claim is supported by this dataset.

## Link-access evidence, anonymous checks

Known GitHub repository API returned 404; private/renamed/missing cannot be distinguished. Both known Colab Drive IDs were anonymously downloadable as valid JSON, but each contains one empty code cell and zero outputs. Neither contains this prepared release. New local RESULTS_REVIEW.ipynb has executed artifact-review outputs; it has not been uploaded/shared by this Work. Localhost is not judge-accessible.

---

## Historical document — retained verbatim, superseded status

Original SHA-256: `a025a3247d3ddeb4d0f5c2acd78ea16f2712366d7a64ffe19a03552695363c69`.

# Источники и инструменты

Создано 14 ноября 2026. Прежнего SOURCES.md локально нет; этот документ не восстанавливает неизвестные записи.

| Источник | Для чего | Статус |
| --- | --- | --- |
| [Veritas AI — Project Briefs](https://drive.google.com/file/d/15tYD48XRmCgWbk1_lLDtc8lebi6qm-4-/view) | Правила, трек, критерии, комплект и срок сдачи | Текст PDF прочитан через Google Drive 14.11.2026; разделы 2, 3, 4.3, 5, 6 |
| Текущее техническое задание пользователя | Идея, Surry / EIA 3806 / CW1, сведения предыдущего аудита и границы MVP | Контекст команды; не независимая верификация данных |
| `data/surry_cw1_monthly.csv` | Будущая исходная выборка | **Файл отсутствует**, первичная ссылка и локальный аудит ещё не добавлены |

## Данные: что проверить до обучения

MODEL должен указать первичный URL/выпуск и дату получения данных, лицензию/условия использования, преобразования, источник полей, исходные единицы и конверсию в °C, методы измерения и логику `eligible_measured`, временное покрытие и исключения. Затем сопоставить ожидаемые 192/188/142/24/22 с фактом. EIA ID и название файла сами по себе не заменяют происхождение и проверку данных.

## Fuel & Climate: коэффициентов пока нет

Нет проверенного источника коэффициентов. Не подставлять значения из памяти или предполагаемого прежнего SOURCES.md. Перед числовой реализацией нужны:

| Величина | Что записать |
| --- | --- |
| Годовая выработка | Единица входа, например TWh/год, и явная конверсия в единицу коэффициента |
| Природный уран на выработку | Источник, численное значение/диапазон, единица (например tU/TWh), допущения топливного цикла |
| Выбросы добычи и переработки руды | Источник, значение/диапазон, единица с точным знаменателем; границы процессов и неопределённость |

Не смешивать массу урана с массой руды/соединений и не выдавать добычу/переработку за полный LCA. Если коэффициент задан на массу руды, нужны отдельно проверенные данные для перехода к массе природного урана. Формулы и результаты должны быть размерностно согласованы.

## Инструменты и credits

- ChatGPT / Codex (OpenAI): использован при настройке структуры и документации; генерация кода модели/приложения на этом этапе не выполнялась. [OpenAI](https://openai.com/).
- Подключённый Google Drive: чтение официального брифа.
- PowerShell: проверка папки; Git: read-only проверка, репозиторий не обнаружен; apply_patch: создание документации.
- Streamlit — запланированный инструмент, пока не использован в реализации. Остальные модели, библиотеки, руководства и AI-инструменты добавлять по фактическому использованию.

Новые источники при параллельной работе сначала записывать в отдельный handoff, затем переносить сюда последовательно. Публичные утверждения об экологии и здоровье требуют собственных надёжных источников; текущий проект их по ΔT не доказывает.
