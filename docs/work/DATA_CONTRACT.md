# MODEL → UI: контракт v2 — реестр отдельных систем

Дата: 2026-11-14. Область этого изменения — подготовка данных, без обучения и изменения UI.
v2 добавляет реестр и адаптер; прежний формат Surry v1 ниже остаётся совместимым.
Архивная формулировка v1 о несуществующих файлах устарела: фактические входы и Surry results уже есть.

## Идентичность и пути

Единица набора: (plant_id_eia, cooling_id_eia). dataset_id = eia_<plant_id>_<hex UTF-8 system_id>.
Hex позволяет обратимо различать 1, CW1, CW-1, регистр и любые символы без коллизий/опасных путей.
Реестр: data/model_artifacts/multistation/registry.json (UTF-8 JSON, schema_version=2).
Одна запись на каждую из 102 систем 66 EIA ID локального проверенного снимка.
Системы/старые ID не склеиваются. Нет утверждения о всех АЭС мира или текущем лицензионном статусе.

Реестр содержит:
- dataset_id, plant_id_eia, plant_name, cooling_id_eia;
- observations: format csv|parquet, path относительно корня, sha256; selector ID и период 2010–2025;
- provenance: table, units °F→°C, URL, snapshot sha256 и ссылка на исходный INVENTORY;
- inventory_status (предварительная категория импорта), status и limitations после повторной проверки;
- rows, eligible_rows, period, split_counts train/validation/test, excluded_months, review_months;
- artifacts: отдельный audit_path, future_results_path, future_artifacts_dir;
- model_status: not_trained либо existing_verified для прежней Surry; results_path=null без готовых результатов.

Все пути разрешать внутри корня проекта; абсолютные пути, выход через ../ и symlink за корень запрещены.
При несовпадении хеша/идентичности/eligibility/arithmetic загрузка должна остановиться.
Пути CSV существующих 7 наборов переиспользуются; новые конкурирующие CSV не создаются.
Для остальных observations указывает исходный Parquet и selector; стандартизация выполняется в памяти.

## Статусы данных и подозрительные строки

- ready_for_model_check: измеренные пары проверены, все три временные части непустые,
  train содержит все 12 календарных месяцев, схема охлаждения совместима с предварительной целью,
  нет нерешённых подозрительных measured-значений. Это данные, не готовая модель/гарантия качества.
- review_required: сомнительный ΔT<=0 или температура вне [-5,100]°C в measured строке.
  Диапазон — маркер предметной проверки, не физический закон. Строки остаются eligible_measured,
  но подготовка задания обучения всего набора блокируется до отдельного решения.
- measurements_only: измерения есть, но нет нужных поздних частей/календаря либо требуется
  согласовать смысл intake/discharge для оборотной/смешанной схемы.
- blocked: нет явно измеренных пар либо не подтверждена ядерная атрибуция (Crystal River).
- reference_only: нет полных пар температуры.

eligible_measured реконструируется по конечным среднемесячным температурам и точному source method:
Measured continuously with a thermometer ИЛИ Measured at intervals (for example, daily) with a thermometer.
Перед сравнением только trim. Оценки, permitted, Other и unknown не являются measured.
CSV helper-флаги дополнительно сверяются с источником; строки "False" не считаются True.
Скрининг импорта сохраняется как объяснение первоначальной категории; не фильтрует train/test молча.
Никаких исключений по ошибке модели; training на этом этапе отсутствует.

## Общий pipeline и исходы

Канонические поля в памяти: report_month, date, plant_id_eia, plant_name, cooling_id_eia,
intake_temperature_f/c, discharge_temperature_f/c, delta_t_c, temperature_method,
temperature_value_class, pair_available, eligible_measured, split.
Температуры °C; delta_t_c вычислен из разности исходных °F до округления, допуск CSV 1.1e-6°C.
Train 2010–2021, validation 2022–2023, test 2024–2025, хронологически и без заполнения целей.
Преобразования/медианы только train; validation для выбора; test только финальная оценка.
Признаки неизменны: intake текущего месяца и sin/cos календаря. Ретроспективная оценка.

Новый адаптер принимает dataset_id и передаёт проверенные части существующим
model.prepare_splits и model.make_features; алгоритмы Ridge/выбора/метрик не копируются.
Он возвращает описание задания и пути; prepare и проверка не вызывают model.train_model/fit.
Будущее обучение — отдельное действие следующего Work с повторным использованием model.train_model
и predict_table. UI читает реестр стандартной библиотекой; импорт reader не импортирует sklearn
и не запускает подготовку/обучение. В этом этапе UI не меняется.

Для новых систем audit: data/model_artifacts/multistation/datasets/<dataset_id>/audit.json;
будущие results.csv и артефакты в том же отдельном каталоге.
До обучения results_path=null, model_status=not_trained, UI показывает Model not ready.
Планируемый results.csv сохраняет шесть числовых/месячных полей v1, одну строку на подходящий
test-месяц выбранной системы. N зависит от данных, не фиксируется 22 для всех.
UI соединяет по dataset_id+report_month либо report_month внутри явно выбранной системы.

## Совместимость Surry и воспроизводимость

Surry CW1 использует data/surry_cw1_monthly.csv, data/results.csv и data/model_artifacts,
включая прежние 142/24/22. Исходные модельные файлы, notebook и артефакты не переписываются.
Реестр лишь ссылается на уже существующий результат после проверки его контракта/измерений/медиан.
Surry CW2 — отдельный набор и не получает результат CW1.

Подготовка из локальных файлов без сети; хеши входов сверяются с INVENTORY.
Детерминированные JSON без времени запуска: повторная подготовка должна дать те же байты.
Операция не перезаписывает отличающиеся подготовленные файлы: новое содержимое требует
отдельного согласованного обновления, а совпавшие JSON остаются нетронутыми.
В handoff передаются реестр, новый код/документация, audit, точные пути исходников и хеши.
Общие README/TASKS/SOURCES/LOG остаются за отдельным интегрирующим Work.

---

## Архивная спецификация v1 (совместимость Surry)

# MODEL → UI: предложенный контракт v1

Статус: согласуемый интерфейс до реализации, не описание уже созданных результатов. На 14 ноября 2026 оба CSV отсутствуют. Все пути относительно корня проекта.

## Вход

`data/surry_cw1_monthly.csv` — ожидаемая исходная выборка Surry / EIA 3806 / CW1. Не менять без отдельной задачи и не копировать в несколько мест. Фактические имена столбцов, кодировку, пропуски, единицы и методы проверяет MODEL после добавления файла; не считать выходные имена ниже схемой входного CSV. Известно ожидаемое поле фильтра `eligible_measured`; фактическое представление true нужно проверить.

UI читает исходник только после сверки схемы, чтобы показывать отчётные температуры. Если файл отсутствует или поля не соответствуют ожиданиям — понятное сообщение, без выдуманных значений.

## Выход MODEL

`data/results.csv` — **будущий** CSV UTF-8 с заголовком, десятичной точкой, одна строка на каждый подходящий финальный тестовый месяц, отсортировано по месяцу. Не создавать до фактической оценки.

| Поле | Формат и смысл |
| --- | --- |
| report_month | Уникальный месяц `YYYY-MM`, только test 2024–2025 |
| intake_temperature_c | Отчётная средняя температура на входе, °C |
| reported_delta_t_c | Отчётная ΔT = сброс − вход, °C; наблюдаемая цель, не признак |
| median_baseline_delta_t_c | Оценка общей медианой ΔT только по train, °C |
| seasonal_baseline_delta_t_c | Оценка медианой ΔT календарного месяца только по train, °C |
| model_delta_t_c | Фактическая оценка обученной моделью, °C |

Все пять числовых полей конечны, без подмены отсутствующих значений нулями. Строки относятся к одной станции и системе, `eligible_measured=true`. Ожидаются 22 тестовых месяца из прошлого аудита, **но число требует проверки CSV**. Изменение фактического состава задокументировать, не добивать таблицу до 22 выдуманными строками. При невозможности оценить месяцы сначала разобраться и явно описать исключения; все методы сравнивать на одинаковых строках. Не скрывать неполный результат.

Оба baseline используют train 2010–2021. Validation 2022–2023 — для выбора модели. Test 2024–2025 — финальная оценка. MAE = среднее абсолютное отклонение от `reported_delta_t_c` в °C, отдельно для трёх методов. Выбор модели и преобразований не зависит от финального test. Отчёт об оценке должен фиксировать признаки, seed при наличии случайности, версии зависимостей, обработку пропусков и команды воспроизведения.

## Состояния UI

- Нет исходника: сообщить, что данные не добавлены.
- Есть исходник, нет results.csv: показывать отчётные измерения и `Model not ready`, без графика фиктивных оценок.
- Есть корректные results.csv: соединять по `report_month`, а не по номеру строки. Показывать оценку только для месяцев, присутствующих в results.csv; для остальных — `No model estimate for this month`.
- Неверная схема, дубли, единицы или неполные значения: показать проблему данных; не молча вычислять/подменять предсказания в UI. UI не обучает модель.
- Температуру сброса для измерений брать из проверенного исходника; в этом контракте её нет. Не использовать `reported_delta_t_c` в качестве модельного входа.

## Изменение и передача между копиями

Перед изменением формата последовательно обновить этот документ (версия, причина), затем оставить для UI отдельный MODEL-handoff. Не редактировать контракт одновременно.

Разные Work, worktree или локальные копии не обязаны видеть изменения. Для MODEL → UI передать:

1. `docs/work/DATA_CONTRACT.md` соответствующей версии и MODEL-handoff.
2. Настоящий `data/results.csv` и отчёт оценки из `data/model_artifacts/` после их появления.
3. Проверенный исходный `data/surry_cw1_monthly.csv`, если его нет у получателя; сравнить хеши уже имеющихся файлов вместо перезаписи.
4. Код `src/model/`, относящиеся проверки и фактические зависимости/команды для воспроизводимости, если нужна полная передача.

В handoff перечислить существующие файлы и версии/хеши. UI передаёт свой `src/ui/`, связанные проверки и handoff; FUEL — свой модуль/проверки и handoff. Сверить схему, источники, входы и общий статус перед ручной стыковкой. Автоматическое объединение и публикация не разрешены.


---

## Additive MODEL → UI evidence-report contract v1 — 15 November 2026

This separately namespaced report contract does **not** change registry v2,
results.csv, scenarios, features, saved estimates or existing readers. Authorized
sequential report-format extension; UI implementation is not changed here.

### Station identity and publication

Reports are site-level by integer plant_id_eia, not by cooling-system label.
Each claim explicitly records its system/site/geographic scope. The Surry water
claim is CW1 only; a site report does not reassign it to CW2. Runtime names come
from the existing registry. Unsupported/unknown station IDs never reuse Surry.

Current outputs:
- data/environment_reports/v1/eia_3806/{report.en.md,report.en.json,technical.json,ready.json}
- data/environment_reports/v1/eia_6011/{report.en.md,report.en.json,technical.json,ready.json}

Read with src.model.environment_report.read_report(directory, expected_plant_id).
Require ready.json last-publication manifest, complete filenames, matching
SHA-256, identity/version and a stable read. Missing/changed files =>
evidence_unavailable; show a retry/absence message, never the previous site's
report. Export refuses existing directories, preserving previous publications.
Future updates should publish a new version directory and switch a pointer only
after validation. No pointer/registry/UI writer was added in this stage.

### Public JSON

report_version=1; plant_id_eia; station_name; language=en; status;
as_of (curation/generation date, **not** observation date); period_label (mixed
historical coverage, not one shared continuous monitoring interval); summary;
sections (fixed order: water, animals_plants, people, climate, unknowns);
expert_review_status=not_performed; method=curated_evidence_rules_not_trained_safety_model.

Each section: id, title, status, paragraphs, claim_ids, references, periods,
limitations. Render paragraphs and the readable public_locator/source title and
URL. Preserve period labels and limitations. Do not render internal source
column names, calculations or technical.json as consumer copy. No aggregate
score, safe/unsafe class, health diagnosis or automatic plant comparison.

Root status: partial_evidence / insufficient_evidence. No status here means
"safe" or "complete". Section status also supports context_only: general
literature is not a site observation. Runtime exceptions (invalid review,
unresolved direct contradiction) map to review_required; missing/corrupt inputs
map to evidence_unavailable. These two states are not fabricated ready reports.
People/land evidence may be insufficient even when water observations exist.
The short refusal is allowed to be shorter than the pilot's 300–500 words.

References retain source_id, claim_id, title, url, role, exact technical locator,
public_locator and support_note. Source role differentiates operator,
state_monitoring, regulator synthesis and scientific assessment. Hosting an
operator report on NRC does not make its contents independent measurements.

### Technical ledger and evidence gates

src/model/environment_evidence/{source_catalog.json,claims.json,review_index.json,
technical_values.json} records source publication/retrieval dates, document
locations/pages/tables, geographic scope, observation periods and support review.
Accepted kinds: observation / model_estimate / scenario / general_context.
Actual site effects, hypothetical scenarios and general context stay distinct.
Every claim carries limitations, impact_polarity, conflict_state/conflict_note,
conflicting_evidence and expert_review_required. Support-reviewed means source
text supports the scoped statement, **not** expert approval or sensor validation.

Unsupported/unread claims are omitted from public output and listed in the
technical audit. General literature cannot support a site observation. A
scenario requires explicit labelling. Unresolved direct contradiction blocks
publication pending adjudication; differing endpoints remain explained (individual
fish capture versus failure to detect a population change). Detection is not
harm; nondetection is not literal absence or proof of safety.

review_index locks local curation hashes, not authenticity/truth of external
sources. Curation changes require renewed source-to-claim checking before the
index is refreshed. Source links alone never authorize a claim. Local water
statements also rerun the existing source adapter/eligibility/identity check.
No online API, runtime source search, paid service, fitting or Ridge call occurs.

### Future integration

UI should load this report alongside existing measurements/ML, not replace
them. Key selection/cache by plant ID + ready.json content version; invalidate
on changes and clear the previous report on every site switch. Keep the whole
report's mixed-period header and distinguish no evidence from a favourable
assessment. Expert assessment remains needed, as listed in CAPABILITY_AUDIT_RU.md.
The old release ZIP predates this module and must not be described as containing
it until a separately authorized release refresh. No UI change or publication
performed in this task.


---

## Additive MODEL → UI story-support v1 — 15 November 2026

Backend-only support for drop journey, month ribbon, claim provenance and catalog.
No registry v2, environmental report v1, saved CSV, report publication or UI
schema is replaced. Existing loaders stay compatible. This extension is specified
before its implementation; the module and own technical guide are src/model/site_support.py
and src/model/SITE_SUPPORT.md.

### Identity, reads and scientific scope

Site identity is integer plant_id_eia. Measurement/journey/prediction identity is
exact registry dataset_id, which binds plant_id_eia plus cooling_id_eia. Never
select a system by name alone or use a model/publication from another identity.
The provider uses the existing registry reader, observation adapter, published
report reader and existing read-only result verifier; no preparation/fit/search.
All payloads carry schema_version=1, identity and registry_version (SHA-256).
One provider instance is a request snapshot, never a persistent UI cache. Registry
changes during reads invalidate that request; start a fresh provider on refresh.

### Drop journey

journey(dataset_id) returns cooling_family (once_through/recirculating/unknown),
scheme_mode (historical_reported_family/general_educational), cooling_type_codes,
period, steps and limitations. Each step has id/title, confirmed_for_system,
general_explanation, sources, unknowns. For unconfirmed/mixed/empty metadata,
confirmed_for_system contains no invented plumbing and general_educational is
prominent. A recirculating scheme must describe reuse/heat rejection and only
conditional releases; never force it into the direct river-return animation.
The historical family is not a current engineering verification or pipe map.
Surry site descriptions are labelled operator-authored and site-level, never
copied to other plants. No plume shape/distance/speed, organism impact or safety
calculation is returned. Animations must be labelled explanatory, not a measured
water particle or validated thermal field.

### Month ribbon

timeline(dataset_id) returns rows for the fixed calendar 2010-01 through 2025-12,
including gaps. Each row: report_month, intake_temperature_c,
discharge_temperature_c, delta_t_c, record_present, eligible_measured,
pair_available, status, reasons, source_method, kind=reported_measurement.
Source units degF; output units degC; the existing adapter checks conversions.
No interpolation or predictions inside measurements. status is
verified_measurement / excluded_method / missing_temperatures / missing_month /
review_required / blocked. Unavailable, excluded or review-blocked values are
null, not zero. The measured-eligibility flag is preserved even where dataset
review status prevents numerical display. A source read failure returns
source_unavailable and no rows, not 192 fabricated missing observations.

predictions(dataset_id) is separate: kind=model_estimate, state verified /
model_not_ready / results_unavailable, clearly labelled saved-model and baseline
estimates. Only registered and independently verified exports enter rows. All
three methods have exactly the verified common test months; no future inference,
no training, no fallback for missing months. Never call these observed values.

### Why this statement?

claim_details(plant_id_eia, cooling_id_eia=None) reads the existing report and its
technical ledger, with an additive companion annotation file. It does not mutate
report v1 paragraphs/references. Every displayed paragraph/summary span has a
stable statement_id, standalone statement text, exact display span/target,
parent_claim_ids, evidence_kind, text_role (source_fact/scope_limit/evidence_gap/
method_explanation), source links, source roles, observation period, geography,
limitations and scope (site/system/general). A source link supports only its
specified span, not the rest of the paragraph. Source-free evidence_gap or
scope_limit records are explicitly module-review boundaries, not findings about
the physical world; they link to the local review basis, not invented field data.
Counterevidence/operator attribution and general-context labels remain visible.

Annotations bind to the published JSON hash and reviewed evidence index hash;
changed publication/curation without renewed annotation review fails closed.
Unknown paragraphs, missing IDs/references, unsupported claims or incomplete
span coverage cannot silently acquire an existing citation. The program checks
wiring; source support still depends on actual recorded content review.
System-filtered calls omit a CW1 claim for CW2. Site statements remain labelled
site context, not effects attributed to every cooling system. Site report access
and selected-system applicability are different fields. Missing/refusal reports
return their honest state and no Surry fallback/cards.

### Catalog and AI role

catalog() returns separate plant records and system records. Site flags:
has_substantive_environment_report / has_insufficient_evidence_report;
report_state and expert_review_status. Substantive requires reviewed site
observations/assessments, not only a general-context paragraph or file existence.
Missing/corrupt/unreviewed publications do not receive either positive flag.
System flags: has_verified_measurements / has_verified_model_results /
requires_review / data_blocked, with reason/state fields and counts. They may
coexist. Site aggregates say any_system and give counts, not all systems ready.
A model does not imply ecological coverage. Preserve reference_only and missing
pairs separately from source corruption. The catalog is a checked snapshot,
not a safety/quality ranking; revalidate on underlying-artifact change.

AI explanation: Ridge estimates a completed month's intake-to-discharge
temperature difference. Environmental reports use reviewed sources and rules;
they are not trained environmental-safety models. No new packages or external
APIs are needed. UI changes, existing artifact replacement and release refresh
are outside this task. Own examples and verification evidence may be saved under
data/site_support/v1 without replacing any earlier results/publications.

Catalog snapshots additionally include dependencies (relative path to SHA-256 or null for an absent artifact) and catalog_version. read_catalog(root, relative_path) rejects changed files or newly appeared reports; rebuild catalog() on refresh. A snapshot is not a live availability guarantee.
