# Построчное объяснение интеграции экологических отчётов

Документ построен по фактическим файлам после интеграции. Каждая добавленная или изменённая непустая строка кода приведена отдельно. Пустые строки служат только разделителями.

Основной экран читает публикацию через существующий read_report. Он не обучает модель, не ищет источники и не создаёт текст отчёта. Одна проверенная версия используется и в основном тексте, и в технической методике.

## Как читать таблицы

Номера относятся к текущим файлам. Старые строки приложения, перенесённые в render_technical, помечены как перенос: алгоритмы, исходные числа и формулы сохранены. Прежние тесты лишь открывают новый технический раздел перед теми же проверками.

## src/ui/environment_loader.py

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | `"""Read published evidence-report v1 without generating, fitting or caching."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 2 | `from dataclasses import dataclass` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 3 | `from datetime import date` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 4 | `import hashlib` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 5 | `import importlib` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 6 | `import json` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 7 | `import logging` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 8 | `from pathlib import Path` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 9 | `from urllib.parse import urlsplit` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 11 | `ROOT = Path(__file__).resolve().parents[2]` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 12 | `REPORTS = Path('data/environment_reports/v1')` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 13 | `LOGGER = logging.getLogger(__name__)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 14 | `SECTION_IDS = ('water', 'animals_plants', 'people', 'climate', 'unknowns')` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 15 | `STATUSES = {'partial_evidence', 'insufficient_evidence', 'context_only'}` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 18 | `class ReviewRequired(ValueError):` | Объявляет отдельный тип результата, ошибки либо группу тестов. |
| 19 | `"""A publication contains evidence that cannot be shown before review."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 22 | `@dataclass(frozen=True)` | Создаёт неизменяемый контейнер результата одного чтения. |
| 23 | `class ReportSnapshot:` | Объявляет отдельный тип результата, ошибки либо группу тестов. |
| 24 | `state: str` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 25 | `report: dict \| None = None` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 26 | `technical: dict \| None = None` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 27 | `version: str \| None = None` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 30 | `def require(condition, reason):` | Останавливает чтение, если обязательное условие не выполнено. |
| 31 | `if not condition:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 32 | `raise ValueError(reason)` | Прерывает обработку неподходящих данных, не подставляя запасной отчёт. |
| 35 | `def text(value):` | Проверяет, что значение является непустым обычным текстом. |
| 36 | `return isinstance(value, str) and bool(value.strip())` | Возвращает результат текущего небольшого шага вызывающему коду. |
| 39 | `def validate_public(report, plant_id):` | Проверяет формат, язык, разделы и ссылки публичного отчёта. |
| 40 | `"""Check presentation fields that the publication reader does not inspect."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 41 | `require(isinstance(report, dict), 'report_shape')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 42 | `require(type(report['plant_id_eia']) is int and report['plant_id_eia'] == plant_id, 'identity')` | Отчёт обязан относиться к выбранному числовому EIA ID. |
| 43 | `require(type(report['report_version']) is int and report['report_version'] == 1, 'version')` | Принимается только поддерживаемая версия контракта. |
| 44 | `require(report['language'] == 'en', 'language')` | В пользовательском отчёте допускается английский язык. |
| 45 | `require(report['method'] == 'curated_evidence_rules_not_trained_safety_model', 'method')` | Не позволяет объявить этот модуль обученной экологической моделью. |
| 46 | `require(report['expert_review_status'] == 'not_performed', 'expert_review_status')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 47 | `require(report['status'] in STATUSES - {'context_only'}, 'report_status')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 48 | `for field in ('station_name', 'period_label', 'summary', 'as_of'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 49 | `require(text(report[field]), 'missing_' + field)` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 50 | `date.fromisoformat(report['as_of'])` | Проверяет корректность календарной даты в стандартном формате. |
| 51 | `sections = report['sections']` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 52 | `require(isinstance(sections, list), 'sections_shape')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 53 | `require([section['id'] for section in sections] == list(SECTION_IDS), 'section_order')` | Пять разделов должны существовать в согласованном порядке. |
| 54 | `for section in sections:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 55 | `require(text(section['title']) and section['status'] in STATUSES, 'section_header')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 56 | `require(isinstance(section['paragraphs'], list) and bool(section['paragraphs']), 'paragraphs_shape')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 57 | `require(all(text(p) for p in section['paragraphs']), 'paragraph_text')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 58 | `for field in ('claim_ids', 'references', 'periods', 'limitations'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 59 | `require(isinstance(section[field], list), 'section_' + field)` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 60 | `require(all(text(value) for value in section['claim_ids'] + section['limitations']), 'section_labels')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 61 | `for period in section['periods']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 62 | `require(text(period['label']), 'period_label')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 63 | `for bound in ('start', 'end'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 64 | `if period.get(bound) is not None:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 65 | `date.fromisoformat(period[bound])` | Проверяет корректность календарной даты в стандартном формате. |
| 66 | `for ref in section['references']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 67 | `for field in ('source_id', 'claim_id', 'title', 'url', 'role', 'public_locator', 'locator', 'support_note'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 68 | `require(text(ref[field]), 'reference_' + field)` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 69 | `url = urlsplit(ref['url'])` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 70 | `require(url.scheme in {'http', 'https'} and bool(url.netloc) and not url.username, 'source_url')` | Разрешает только обычные HTTP/HTTPS-ссылки без встроенных учётных данных. |
| 71 | `require(ref['claim_id'] in section['claim_ids'], 'reference_claim')` | Источник должен быть связан с утверждением своего раздела. |
| 74 | `def validate_scope(report, technical, plant_id):` | Сверяет станцию, область выводов и отсутствие неразрешённых противоречий. |
| 75 | `"""Do not turn a site publication or disputed claim into a wider verdict."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 76 | `require(isinstance(technical, dict), 'technical_shape')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 77 | `claims = technical['accepted_claims']` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 78 | `require(isinstance(claims, list) and isinstance(technical['local_checks'], dict), 'ledger_shape')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 79 | `by_id = {}` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 80 | `for claim in claims:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 81 | `require(claim['plant_id_eia'] == plant_id and type(claim['plant_id_eia']) is int, 'claim_identity')` | Утверждение нельзя переносить на другую станцию. |
| 82 | `require(claim['id'] not in by_id and text(claim['geography']), 'claim_scope')` | У каждого утверждения должны быть уникальный ID и описание места. |
| 83 | `require(claim['kind'] in {'observation', 'model_estimate', 'scenario', 'general_context'}, 'claim_kind')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 84 | `if claim['conflict_state'] == 'unresolved' or claim['review_status'] != 'reviewed_for_support':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 85 | `raise ReviewRequired('source_review')` | Блокирует показ спорных сведений до проверки источников. |
| 86 | `require(claim['conflict_state'] in {'none_identified', 'different_endpoint'}, 'conflict_state')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 87 | `by_id[claim['id']] = claim` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 88 | `for section in report['sections']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 89 | `for identifier in section['claim_ids']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 90 | `require(identifier in by_id and by_id[identifier]['section'] == section['id'], 'claim_section')` | Утверждение должно принадлежать именно своему разделу. |
| 91 | `if section['status'] == 'context_only':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 92 | `require(all(by_id[c]['kind'] == 'general_context' for c in section['claim_ids']), 'context_scope')` | Общий контекст нельзя выдать за измерение на станции. |
| 93 | `if report['status'] == 'insufficient_evidence':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 94 | `require(not claims and not any(s['references'] for s in report['sections']), 'insufficient_scope')` | Отказ из-за нехватки сведений не должен содержать одобренные выводы. |
| 95 | `water = technical['local_checks'].get('water')` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 96 | `if water is not None:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 97 | `require(isinstance(water, dict) and text(water['system']), 'water_system_scope')` | Температурное заключение должно иметь явное имя системы охлаждения. |
| 100 | `def report_snapshot(plant_id, root=ROOT):` | Читает одну завершённую публикацию для выбранной станции без кэша и генерации. |
| 101 | `"""Every call rereads the manifest and artifacts; no previous-site fallback."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 102 | `stage = 'station_selection'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 103 | `try:` | Начинает защищённое чтение: ожидаемые ошибки будут показаны без traceback. |
| 104 | `require(type(plant_id) is int and plant_id > 0, 'plant_id')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 105 | `directory = Path(root).resolve() / REPORTS / f'eia_{plant_id}'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 106 | `require(directory.resolve().is_relative_to(Path(root).resolve()), 'publication_path')` | Папка отчёта не может выходить за корень проекта. |
| 107 | `if not directory.exists():` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 108 | `return ReportSnapshot('missing')` | Возвращает состояние чтения и только проверенные данные; для отказа данных отчёта нет. |
| 109 | `for name in ('ready.json', 'report.en.json', 'report.en.md', 'technical.json'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 110 | `require((directory / name).resolve().is_relative_to(directory.resolve()), 'artifact_path')` | Отдельный файл не может вести за пределы папки публикации. |
| 111 | `stage = 'module_import'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 112 | `reader = importlib.import_module('src.model.environment_report').read_report` | Находит существующий reader; не создаёт второй генератор отчётов. |
| 113 | `stage = 'manifest'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 114 | `manifest_bytes = (directory / 'ready.json').read_bytes()` | Читает реальные байты файла для JSON или проверки неизменности. |
| 115 | `manifest = json.loads(manifest_bytes)` | Разбирает сохранённый JSON; не создаёт нового содержания отчёта. |
| 116 | `require(type(manifest['report_version']) is int and manifest['report_version'] == 1, 'manifest_version')` | Проверяет обязательное поле или допустимый тип по контракту; при нарушении отчёт скрывается. |
| 117 | `stage = 'publication_reader'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 118 | `report = reader(directory, plant_id)` | Передаёт папку и ожидаемый ID официальному read_report, который сверяет публикацию и хеши. |
| 119 | `technical = json.loads((directory / 'technical.json').read_bytes())` | Читает реальные байты файла для JSON или проверки неизменности. |
| 120 | `stage = 'public_contract'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 121 | `validate_public(report, plant_id)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 122 | `stage = 'evidence_scope'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 123 | `validate_scope(report, technical, plant_id)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 124 | `stage = 'stable_publication'` | Запоминает безопасное имя текущего этапа для диагностики; исходный текст ошибки не журналируется. |
| 125 | `require((directory / 'ready.json').read_bytes() == manifest_bytes, 'publication_race')` | Манифест должен остаться тем же до завершения чтения. |
| 126 | `for name, expected in manifest['sha256'].items():` | Использует контрольную сумму для проверки целостности или обозначения версии публикации. |
| 127 | `require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected, 'artifact_race')` | Проверяет, что байты файлов не изменились во время чтения. |
| 128 | `state = 'ready' if report['status'] == 'partial_evidence' else 'insufficient_evidence'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 129 | `return ReportSnapshot(state, report, technical, hashlib.sha256(manifest_bytes).hexdigest())` | Использует контрольную сумму для проверки целостности или обозначения версии публикации. |
| 130 | `except ImportError:` | Перехватывает указанный отказ и переводит его в понятное состояние интерфейса. |
| 131 | `state, reason = 'module_unavailable', 'import'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 132 | `except ReviewRequired:` | Перехватывает указанный отказ и переводит его в понятное состояние интерфейса. |
| 133 | `state, reason = 'review_required', 'source_review'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 134 | `except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError):` | Перехватывает указанный отказ и переводит его в понятное состояние интерфейса. |
| 135 | `state, reason = 'evidence_unavailable', 'publication_validation'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 136 | `LOGGER.warning('Environmental report withheld: plant_id=%s state=%s reason=%s stage=%s', plant_id, state, reason, stage)` | Пишет в журнал ID станции, состояние и этап отказа без traceback, путей и содержимого файлов. |
| 137 | `return ReportSnapshot(state)` | Возвращает состояние чтения и только проверенные данные; для отказа данных отчёта нет. |

## src/ui/environment_panel.py

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | `"""Plain-language view of a checked publication; no report generation here."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 2 | `import streamlit as st` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 3 | `from environment_loader import report_snapshot` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 5 | `STATUS_LABELS = {` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 6 | `'partial_evidence': 'Historical evidence with limits',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 7 | `'insufficient_evidence': 'Not enough evidence',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 8 | `'context_only': 'General context, not a site finding',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 9 | `}` | Закрывает ранее начатый вызов, список или таблицу настроек. |
| 10 | `SOURCE_ROLES = {` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 11 | `'government_reports_via_pudl': 'Government reporting via PUDL',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 12 | `'state_monitoring': 'State monitoring',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 13 | `'regulator_synthesis': 'Regulator review of earlier studies',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 14 | `'operator': 'Operator account',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 15 | `'scientific_assessment': 'Scientific literature assessment',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 16 | `}` | Закрывает ранее начатый вызов, список или таблицу настроек. |
| 17 | `MESSAGES = {` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 18 | `'missing': 'No environmental report has been published for this station. Measurements and saved model results remain available below.',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 19 | `'module_unavailable': 'Environmental reports are temporarily unavailable. Try Refresh data; the measurement explorer is still available below.',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 20 | `'evidence_unavailable': 'This report is unavailable because its files are incomplete or could not be verified. Try Refresh data. Measurements remain available below.',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 21 | `'review_required': 'The evidence needs review before this report can be shown, including any unresolved source disagreements. Measurements remain available below.',` | Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 22 | `}` | Закрывает ранее начатый вызов, список или таблицу настроек. |
| 25 | `def environment_panel(plant_id, system, root):` | Выводит проверенный английский отчёт и его источники. |
| 26 | `st.header('Environmental report', anchor='environment-report')` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 27 | `snapshot = report_snapshot(plant_id, root)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 28 | `if snapshot.report is None:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 29 | `message = MESSAGES[snapshot.state]` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 30 | `if snapshot.state == 'review_required':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 31 | `st.warning(message)` | Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 32 | `else:` | Обрабатывает альтернативный случай отдельно от предыдущего. |
| 33 | `st.info(message)` | Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 34 | `st.subheader('Sources', anchor='evidence-methods')` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 35 | `st.caption('No verified report sources can be displayed for this station right now.')` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 36 | `return snapshot` | Возвращает результат текущего небольшого шага вызывающему коду. |
| 37 | `report = snapshot.report` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 38 | `st.caption(f"Site report: {report['station_name']} (EIA {plant_id}). Prepared from reviewed sources; specialist review has not been performed.")` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 39 | `st.caption('Evidence period: ' + report['period_label'])` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 40 | `st.caption(f"Compiled {report['as_of']}; this date is not an observation date. The report does not change with the historical month selector.")` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 41 | `water = snapshot.technical['local_checks'].get('water')` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 42 | `if water:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 43 | `st.caption(f"The water-temperature finding covers system {water['system']} only. Your selected system is {system}; findings are not transferred between systems.")` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 44 | `with st.container(border=True, key='environment_summary'):` | Группирует содержимое нативным контейнером Streamlit с устойчивым ключом. |
| 45 | `st.subheader('At a glance')` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 46 | `st.text(report['summary'])` | Показывает исходный текст без Markdown и без переписывания проверенного утверждения. |
| 47 | `if snapshot.state == 'insufficient_evidence':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 48 | `st.info('Not enough reviewed evidence for site-specific environmental conclusions. This is not a favourable or unfavourable assessment.')` | Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 49 | `with st.container(key='environment_sections'):` | Группирует содержимое нативным контейнером Streamlit с устойчивым ключом. |
| 50 | `for section in report['sections']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 51 | `anchor = {'animals_plants': 'ecosystem-context', 'climate': 'climate-context'}.get(section['id'], f"report-{section['id']}")` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 52 | `st.subheader(section['title'], anchor=anchor)` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 53 | `st.caption(STATUS_LABELS[section['status']])` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 54 | `for paragraph in section['paragraphs']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 55 | `st.text(paragraph)` | Показывает исходный текст без Markdown и без переписывания проверенного утверждения. |
| 56 | `if section['periods']:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 57 | `st.caption('Period: ' + '; '.join(period['label'] for period in section['periods']))` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 58 | `st.subheader('Sources and limitations', anchor='evidence-methods')` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 59 | `st.caption('Sources are grouped by the findings they support. An operator account is distinguished from independent monitoring and general literature.')` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 60 | `if not any(section['references'] for section in report['sections']):` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 61 | `st.caption('No site-specific sources have been approved in this report.')` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 62 | `for section in report['sections']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 63 | `if section['references'] or section['limitations']:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 64 | `with st.expander('Sources and limits: ' + section['title']):` | Создаёт раскрывающийся блок для источников, ограничений либо технических подробностей. |
| 65 | `seen = set()` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 66 | `for reference in section['references']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 67 | `identity = (reference['url'], reference['public_locator'], reference['role'])` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 68 | `if identity in seen:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 69 | `continue` | Пропускает уже обработанный повтор источника. |
| 70 | `seen.add(identity)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 71 | `st.link_button(reference['title'], reference['url'], wrap=True, width='stretch')` | Создаёт настоящую доступную ссылку на источник; длинная подпись переносится. |
| 72 | `st.caption(reference['public_locator'])` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 73 | `st.caption('Source role: ' + SOURCE_ROLES.get(reference['role'], reference['role'].replace('_', ' ')))` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 74 | `for limitation in section['limitations']:` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 75 | `st.text(limitation)` | Показывает исходный текст без Markdown и без переписывания проверенного утверждения. |
| 76 | `return snapshot` | Возвращает результат текущего небольшого шага вызывающему коду. |
| 79 | `def report_method_panel(snapshot):` | Показывает метод подготовки и технический журнал того же снимка отчёта. |
| 80 | `"""Keep the evidence method and audit out of the consumer report."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 81 | `st.subheader('How the environmental report is prepared')` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 82 | `st.write('This is a local publication assembled by curated evidence rules, not a trained ecological-safety model. No runtime source search, external API, model fitting or safety score is used.')` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 83 | `if snapshot.report is not None:` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 84 | `st.caption(f"Evidence-report contract v{snapshot.report['report_version']} · publication {snapshot.version[:12]}")` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 85 | `with st.expander('Reviewed claims, scope and technical audit'):` | Создаёт раскрывающийся блок для источников, ограничений либо технических подробностей. |
| 86 | `st.json(snapshot.technical, expanded=False)` | Оставляет подробный журнал только в техническом разделе. |

## src/ui/app.py

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 13 | `from environment_panel import environment_panel, report_method_panel` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 91 | `def render_technical(entry, identifier, plant_id, token, root, publication):` | Собирает прежние измерения, графики, Ridge и сценарии в отдельном разделе. |
| 92 | `status_label = {'ready_for_model_check': 'Measured records available', 'measurements_only': 'Measurements with limitations',` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 93 | `'review_required': 'Data review required', 'blocked': 'Data unavailable', 'reference_only': 'Reference only'}` | Перенос без изменения прежней логики. Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 94 | `st.markdown(f'<div class="lab-context"><h2>{escape(entry["plant_name"])}</h2>'` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 95 | `f'<p>System {escape(str(entry["cooling_id_eia"]))} &nbsp; · &nbsp; EIA {plant_id}'` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 96 | `f' &nbsp; · &nbsp; {status_label.get(entry["status"], "See source details")}</p></div>', unsafe_allow_html=True)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 97 | `measurements = None` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 98 | `month = None` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 99 | `if entry['status'] in {'blocked', 'reference_only'}:` | Перенос без изменения прежней логики. Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 100 | `st.warning('Temperature data unavailable for confirmed measurement display. See reasons above; no numbers are substituted.')` | Перенос без изменения прежней логики. Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 101 | `elif entry['status'] == 'review_required':` | Перенос без изменения прежней логики. Обрабатывает альтернативный случай отдельно от предыдущего. |
| 102 | `st.error('Data review required. Unresolved suspect measurements: temperature cards and model comparisons are withheld pending review.')` | Перенос без изменения прежней логики. Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 103 | `else:` | Перенос без изменения прежней логики. Обрабатывает альтернативный случай отдельно от предыдущего. |
| 104 | `try:` | Перенос без изменения прежней логики. Начинает защищённое чтение: ожидаемые ошибки будут показаны без traceback. |
| 105 | `measurements, audit = measurements_snapshot(entry, token, root)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 106 | `except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:` | Перенос без изменения прежней логики. Перехватывает указанный отказ и переводит его в понятное состояние интерфейса. |
| 107 | `st.warning(f'Measured data temporarily unavailable or need review: {exc}. Refresh data to retry.')` | Перенос без изменения прежней логики. Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 108 | `else:` | Перенос без изменения прежней логики. Обрабатывает альтернативный случай отдельно от предыдущего. |
| 109 | `if measurements.empty:` | Перенос без изменения прежней логики. Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 110 | `st.warning('No eligible measured temperature pairs are available.')` | Перенос без изменения прежней логики. Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 111 | `else:` | Перенос без изменения прежней логики. Обрабатывает альтернативный случай отдельно от предыдущего. |
| 112 | `months = measurements.report_month.tolist()` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 113 | `month = st.selectbox('Historical reporting month', months, index=len(months) - 1, key=f'month_{identifier}', persist_state='session')` | Сохраняет выбор исторического месяца в сессии, даже когда технический раздел скрыт. |
| 114 | `row = measurements.set_index('report_month').loc[month]` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 115 | `st.caption('Source-reported measured monthly averages · °C')` | Перенос без изменения прежней логики. Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 116 | `for col, label, field in zip(st.columns(3), ['Intake temperature, °C', 'Discharge temperature, °C', 'Reported ΔT, °C'],` | Перенос без изменения прежней логики. Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 117 | `['intake_temperature_c', 'discharge_temperature_c', 'reported_delta_t_c']):` | Перенос без изменения прежней логики. Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 118 | `col.metric(label, f'{row[field]:.2f}')` | Перенос без изменения прежней логики. Задаёт элемент словаря: машинному состоянию сопоставляется понятная подпись или сообщение. |
| 119 | `st.markdown('<div class="lab-note"><b>Read this difference correctly.</b> ΔT = discharge − intake temperature across the cooling system. '` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 120 | `'It is not the heating of the whole water body.</div>', unsafe_allow_html=True)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 121 | `overview, performance, evidence, impacts = st.tabs(['Water overview', 'Model performance', 'Sources & context', 'Impact scenarios'])` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 122 | `with overview:` | Перенос без изменения прежней логики. Ограничивает действие контекстом контейнера, временного файла или тестовой подмены. |
| 123 | `st.subheader('The historical picture')` | Перенос без изменения прежней логики. Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 124 | `st.caption('Reported monthly cooling-system ΔT · explore the trend, not an environmental safety score.')` | Перенос без изменения прежней логики. Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 125 | `if measurements is not None and not measurements.empty:` | Перенос без изменения прежней логики. Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 126 | `water_chart(history_chart(measurements).rename(columns={'reported_delta_t_c': 'Reported measurement'}),` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 127 | `x_label='Reporting month', y_label='Cooling-system ΔT (°C)', height=330, color=['#70eee4'], selected_month=month)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 128 | `temperatures = measurements.set_index('report_month')[['intake_temperature_c', 'discharge_temperature_c']].copy()` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 129 | `temperatures.index = pd.to_datetime(temperatures.index)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 130 | `temperatures = temperatures.reindex(pd.date_range(temperatures.index.min(), temperatures.index.max(), freq='MS'))` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 131 | `st.subheader('Intake & discharge temperature')` | Перенос без изменения прежней логики. Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 132 | `st.caption(f'Selected month: {month}. Source-reported monthly averages; gaps remain unavailable.')` | Перенос без изменения прежней логики. Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 133 | `water_chart(temperatures.rename(columns={'intake_temperature_c': 'Measured intake', 'discharge_temperature_c': 'Measured discharge'}),` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 134 | `x_label='Reporting month', y_label='Temperature (°C)', height=270, color=['#70eee4', '#ffc86b'], selected_month=month)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 135 | `st.caption(f"{audit['eligible']} eligible months out of {audit['total']} rows · {months[0]} to {months[-1]}. Gaps are unavailable/excluded months, not zero. Rounding does not imply sensor precision.")` | Перенос без изменения прежней логики. Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 136 | `with st.expander('Excluded months and split coverage'):` | Перенос без изменения прежней логики. Создаёт раскрывающийся блок для источников, ограничений либо технических подробностей. |
| 137 | `st.write(', '.join(audit['excluded']) or 'None')` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 138 | `st.write(entry['split_counts'])` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 139 | `else:` | Перенос без изменения прежней логики. Обрабатывает альтернативный случай отдельно от предыдущего. |
| 140 | `st.info('No confirmed measurement series to display. See Sources & context for limitations.')` | Перенос без изменения прежней логики. Показывает понятное сообщение о состоянии, не раскрывая техническое исключение. |
| 141 | `st.markdown('<div id="measurement-context" class="lab-eyebrow">02 / Ecosystem context</div>', unsafe_allow_html=True)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 142 | `left, right = st.columns(2)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 143 | `with left:` | Перенос без изменения прежней логики. Ограничивает действие контекстом контейнера, временного файла или тестовой подмены. |
| 144 | `st.subheader('What we know')` | Перенос без изменения прежней логики. Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 145 | `st.write('Eligible records describe source-reported monthly intake and discharge temperatures for the selected system. Saved estimates are checked against that system and its test months.')` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 146 | `with right:` | Перенос без изменения прежней логики. Ограничивает действие контекстом контейнера, временного файла или тестовой подмены. |
| 147 | `st.subheader("What we don't know")` | Перенос без изменения прежней логики. Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 148 | `st.write('These records cannot establish harm or safety for people, animals or plants. Monthly averages do not describe local peaks, mixing or downstream temperatures. Results do not automatically apply to Akkuyu or another system.')` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 149 | `with performance:` | Перенос без изменения прежней логики. Ограничивает действие контекстом контейнера, временного файла или тестовой подмены. |
| 150 | `model_panel(entry, measurements, month, token, root)` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 151 | `with evidence:` | Перенос без изменения прежней логики. Ограничивает действие контекстом контейнера, временного файла или тестовой подмены. |
| 152 | `st.subheader('Evidence behind this view')` | Перенос без изменения прежней логики. Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 153 | `st.caption('EIA Form 923 · distributed by Catalyst Cooperative PUDL. Historical records, not live monitoring.')` | Перенос без изменения прежней логики. Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 154 | `st.markdown('[Open data & methodology](#measurement-methods)')` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 155 | `with impacts:` | Перенос без изменения прежней логики. Ограничивает действие контекстом контейнера, временного файла или тестовой подмены. |
| 156 | `impact_panel()` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 157 | `st.markdown('<section id="measurement-methods" class="section-heading"><div class="lab-eyebrow">04 / Data &amp; methodology</div>'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 158 | `'<h2>Follow the evidence.</h2><p>Reported measurements and saved model estimates are kept separate. '` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 159 | `'Explore the source, reporting method and limits for this cooling system.</p></section>', unsafe_allow_html=True)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 160 | `source_panel(entry)` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 161 | `st.markdown('<section id="scenario-context" class="lab-note"><div class="lab-eyebrow">03 / Climate &amp; emissions</div><h3>Explore explicit scenarios</h3>'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 162 | `'Open Impact scenarios for idealized mixing and water-volume heat balances, a literature-based lifecycle '` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 163 | `'emissions scenario and an ecological evidence checklist. Inputs are independent of the selected station. '` | Перенос без изменения прежней логики. Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 164 | `'These calculations do not establish site impacts, legal compliance or safety.</section>', unsafe_allow_html=True)` | Перенос без изменения прежней логики. Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 165 | `report_method_panel(publication)` | Передаёт уже прочитанный снимок в методику, чтобы основной текст и аудит не расходились. |
| 195 | `publication = environment_panel(plant_id, entry['cooling_id_eia'], root)` | Размещает экологический отчёт сразу после выбора станции и получает снимок публикации. |
| 196 | `st.header('Explore the details', anchor='technical-details')` | Добавляет понятный заголовок и, где задано, ссылочный якорь раздела. |
| 197 | `st.caption('Historical measurements, saved model comparisons and user-entered scenarios. These do not replace the source-based environmental report above.')` | Показывает пояснение, дату, период или роль источника отдельно от выводов. |
| 198 | `if st.toggle('Show measurements, model results and scenarios', key='technical_details'):` | Создаёт переключатель подробностей: по умолчанию виден простой отчёт. |
| 199 | `with st.container(key='technical_explorer'):` | Группирует содержимое нативным контейнером Streamlit с устойчивым ключом. |
| 200 | `render_technical(entry, identifier, plant_id, token, root, publication)` | Показывает прежние инструменты и передаёт им тот же проверенный снимок отчёта. |

## src/ui/style.css

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 67 | `.st-key-environment_sections, .st-key-environment_summary { max-width:880px; }` | Оформляет только новые именованные блоки отчёта: ширину чтения, межстрочный интервал, фон или отступ якоря. |
| 68 | `.st-key-environment_sections { line-height:1.65; }` | Оформляет только новые именованные блоки отчёта: ширину чтения, межстрочный интервал, фон или отступ якоря. |
| 69 | `.st-key-environment_summary { background:#123e46b0; border-color:var(--lab-line); }` | Оформляет только новые именованные блоки отчёта: ширину чтения, межстрочный интервал, фон или отступ якоря. |
| 70 | `#environment-report, #technical-details, #measurement-methods { scroll-margin-top:85px; }` | Комментарий объясняет границу или назначение следующего действия; не выполняется. |

## tests/ui/test_environment.py

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | `"""Publication identity, failure isolation, refresh and consumer/technical views."""` | Краткое пояснение назначения блока, не выводится пользователю. |
| 2 | `import asyncio` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 3 | `from copy import deepcopy` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 4 | `import hashlib` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 5 | `import json` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 6 | `import os` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 7 | `from pathlib import Path` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 8 | `import shutil` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 9 | `import sys` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 10 | `import tempfile` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 11 | `import unittest` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 12 | `from unittest.mock import MagicMock, patch` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 14 | `ROOT = Path(__file__).resolve().parents[2]` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 15 | `sys.path.insert(0, str(ROOT / 'src/ui'))` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 16 | `from environment_loader import REPORTS, ReportSnapshot, report_snapshot` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 19 | `class ReportReaderTests(unittest.TestCase):` | Объявляет отдельный тип результата, ошибки либо группу тестов. |
| 20 | `def setUp(self):` | Создаёт изолированные условия проверки; исходные публикации не меняются. |
| 21 | `folder = tempfile.TemporaryDirectory()` | Готовит временную копию публикации, не изменяя рабочие данные. |
| 22 | `self.addCleanup(folder.cleanup)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 23 | `self.root = Path(folder.name)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 24 | `shutil.copytree(ROOT / REPORTS, self.root / REPORTS)` | Готовит временную копию публикации, не изменяя рабочие данные. |
| 26 | `def update(self, filename, value, plant=3806):` | Изменяет только временную тестовую публикацию и пересчитывает её манифест. |
| 27 | `directory = self.root / REPORTS / f'eia_{plant}'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 28 | `path = directory / filename` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 29 | `path.write_text(json.dumps(value), encoding='utf-8')` | Меняет только временный тестовый файл, чтобы проверить обновление или повреждение. |
| 30 | `manifest_path = directory / 'ready.json'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 31 | `manifest = json.loads(manifest_path.read_text())` | Разбирает сохранённый JSON; не создаёт нового содержания отчёта. |
| 32 | `manifest['sha256'][filename] = hashlib.sha256(path.read_bytes()).hexdigest()` | Читает реальные байты файла для JSON или проверки неизменности. |
| 33 | `manifest_path.write_text(json.dumps(manifest), encoding='utf-8')` | Меняет только временный тестовый файл, чтобы проверить обновление или повреждение. |
| 35 | `def test_real_report_scope_period_and_other_station(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 36 | `surry = report_snapshot(3806, self.root)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 37 | `self.assertEqual(surry.state, 'ready')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 38 | `self.assertIn('1970s', surry.report['period_label'])` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 39 | `self.assertIn('2010', surry.report['period_label'])` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 40 | `self.assertIn('2025', surry.report['period_label'])` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 41 | `self.assertEqual(surry.technical['local_checks']['water']['start'], '2010-01')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 42 | `self.assertEqual(surry.technical['local_checks']['water']['end'], '2025-12')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 43 | `self.assertEqual(surry.technical['local_checks']['water']['system'], 'CW1')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 44 | `calvert = report_snapshot(6011, self.root)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 45 | `self.assertEqual(calvert.state, 'insufficient_evidence')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 46 | `self.assertNotIn('Surry', json.dumps(calvert.report))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 47 | `self.assertEqual(report_snapshot(6000, self.root).state, 'missing')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 48 | `self.assertEqual(report_snapshot(3806, self.root).report, surry.report)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 50 | `def test_missing_corrupt_and_wrong_identity_are_withheld(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 51 | `directory = self.root / REPORTS / 'eia_3806'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 52 | `report = json.loads((directory / 'report.en.json').read_text())` | Разбирает сохранённый JSON; не создаёт нового содержания отчёта. |
| 53 | `report['plant_id_eia'] = 6011` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 54 | `self.update('report.en.json', report)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 55 | `self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 56 | `(directory / 'report.en.json').write_text('{broken')` | Меняет только временный тестовый файл, чтобы проверить обновление или повреждение. |
| 57 | `self.assertIsNone(report_snapshot(3806, self.root).report)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 58 | `(directory / 'ready.json').unlink()` | Меняет только временный тестовый файл, чтобы проверить обновление или повреждение. |
| 59 | `self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 61 | `def test_contract_shape_and_unsafe_link_rejected_even_with_new_hash(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 62 | `publication = report_snapshot(3806, self.root).report` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 63 | `for value in ('javascript:alert(1)', 'file:///private'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 64 | `report = deepcopy(publication)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 65 | `report['sections'][0]['references'][0]['url'] = value` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 66 | `self.update('report.en.json', report)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 67 | `self.assertIsNone(report_snapshot(3806, self.root).report)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 68 | `report = deepcopy(publication)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 69 | `report['sections'] = []` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 70 | `self.update('report.en.json', report)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 71 | `self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 73 | `def test_unresolved_conflict_blocks_public_copy(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 74 | `technical = deepcopy(report_snapshot(3806, self.root).technical)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 75 | `technical['accepted_claims'][0]['conflict_state'] = 'unresolved'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 76 | `self.update('technical.json', technical)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 77 | `result = report_snapshot(3806, self.root)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 78 | `self.assertEqual(result.state, 'review_required')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 79 | `self.assertIsNone(result.report)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 81 | `def test_refresh_reads_new_publication_without_cached_copy(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 82 | `before = report_snapshot(3806, self.root)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 83 | `report = deepcopy(before.report)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 84 | `report['as_of'] = '2026-11-14'` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 85 | `self.update('report.en.json', report)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 86 | `after = report_snapshot(3806, self.root)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 87 | `self.assertEqual(after.state, 'ready')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 88 | `self.assertNotEqual(before.version, after.version)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 89 | `self.assertEqual(after.report['as_of'], '2026-11-14')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 91 | `def test_missing_module_and_publication_race(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 92 | `with patch('environment_loader.importlib.import_module', side_effect=ImportError('private detail')):` | Находит существующий reader; не создаёт второй генератор отчётов. |
| 93 | `self.assertEqual(report_snapshot(3806, self.root).state, 'module_unavailable')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 94 | `from src.model.environment_report import read_report` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 95 | `real_import = __import__('importlib').import_module` | Находит существующий reader; не создаёт второй генератор отчётов. |
| 96 | `module = real_import('src.model.environment_report')` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 97 | `def changing_read(directory, plant):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 98 | `report = read_report(directory, plant)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 99 | `(directory / 'technical.json').write_text('{}')` | Меняет только временный тестовый файл, чтобы проверить обновление или повреждение. |
| 100 | `return report` | Возвращает результат текущего небольшого шага вызывающему коду. |
| 101 | `with patch.object(module, 'read_report', side_effect=changing_read):` | Имитирует конкретный сбой только внутри теста. |
| 102 | `self.assertEqual(report_snapshot(3806, self.root).state, 'evidence_unavailable')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 105 | `class ReportScreenTests(unittest.TestCase):` | Объявляет отдельный тип результата, ошибки либо группу тестов. |
| 106 | `def setUp(self):` | Создаёт изолированные условия проверки; исходные публикации не меняются. |
| 107 | `if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 108 | `def nonrunning_loop():` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 109 | `loop = MagicMock(spec=asyncio.AbstractEventLoop)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 110 | `loop.is_closed.return_value = False` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 111 | `return loop` | Возвращает результат текущего небольшого шага вызывающему коду. |
| 112 | `factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop', side_effect=nonrunning_loop)` | Имитирует конкретный сбой только внутри теста. |
| 113 | `factory.start()` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 114 | `self.addCleanup(factory.stop)` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |
| 116 | `def screen(self):` | Запускает настоящий код приложения в AppTest без браузера. |
| 117 | `from streamlit.testing.v1 import AppTest` | Подключает указанный готовый модуль; не запускает обучение или сетевой поиск. |
| 118 | `return AppTest.from_file(str(ROOT / 'src/ui/app.py')).run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 120 | `def public_copy(self, screen):` | Собирает обычный текст, чтобы проверить отсутствие чужих выводов. |
| 121 | `return '\n'.join(node.value for node in screen.text)` | Возвращает результат текущего небольшого шага вызывающему коду. |
| 123 | `def test_consumer_view_switching_sources_and_technical_details(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 124 | `screen = self.screen()` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 125 | `self.assertFalse(screen.exception, str(screen.exception))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 126 | `self.assertIn('James River', self.public_copy(screen))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 127 | `self.assertEqual(len(screen.metric), 0)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 128 | `self.assertEqual(len(screen.selectbox), 2)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 129 | `self.assertTrue(any('vdh.virginia.gov' in node.url for node in screen.link_button))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 130 | `captions = ' '.join(node.value for node in screen.caption)` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 131 | `self.assertIn('does not change with the historical month', captions)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 132 | `self.assertIn('CW1 only', captions)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 133 | `screen.selectbox(key='system_3806').select('eia_3806_435732').run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 134 | `self.assertIn('selected system is CW2', ' '.join(node.value for node in screen.caption))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 135 | `screen.selectbox(key='plant').select(6011).run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 136 | `self.assertNotIn('James River', self.public_copy(screen))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 137 | `self.assertEqual(len(screen.link_button), 0)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 138 | `self.assertIn('No station-specific environmental evidence', self.public_copy(screen))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 139 | `screen.selectbox(key='plant').select(6000).run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 140 | `self.assertTrue(any('No environmental report' in node.value for node in screen.info))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 141 | `self.assertNotIn('James River', self.public_copy(screen))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 142 | `screen.selectbox(key='plant').select(3806).run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 143 | `screen.selectbox(key='system_3806').select('eia_3806_435731').run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 144 | `screen.toggle(key='technical_details').set_value(True).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |
| 145 | `self.assertFalse(screen.exception)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 146 | `self.assertEqual(screen.metric[2].value, '6.67')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 147 | `self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [22] * 3)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 148 | `screen.selectbox[2].select('2025-10').run(timeout=30)` | Запускает приложение в тесте после действия и ждёт окончания обработки. |
| 149 | `self.assertIn('James River', self.public_copy(screen))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 150 | `screen.toggle(key='technical_details').set_value(False).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |
| 151 | `screen.toggle(key='technical_details').set_value(True).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |
| 152 | `self.assertEqual(screen.selectbox[2].value, '2025-10')` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 154 | `def test_report_failures_keep_legacy_results_and_hide_diagnostics(self):` | Начинает отдельную проверку сценария, указанного в имени теста. |
| 155 | `for state in ('evidence_unavailable', 'review_required', 'module_unavailable'):` | Последовательно обрабатывает указанные разделы, поля, источники или тестовые случаи. |
| 156 | `with self.subTest(state=state), patch('environment_panel.report_snapshot', return_value=ReportSnapshot(state)):` | Возвращает состояние чтения и только проверенные данные; для отказа данных отчёта нет. |
| 157 | `screen = self.screen()` | Сохраняет промежуточное значение, настройку или подпись, названную слева; не изменяет исходные измерения. |
| 158 | `self.assertFalse(screen.exception)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 159 | `self.assertNotIn('James River', self.public_copy(screen))` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 160 | `screen.toggle(key='technical_details').set_value(True).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |
| 161 | `self.assertFalse(screen.exception)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 162 | `self.assertEqual(len(screen.metric), 5)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 163 | `self.assertEqual(len(screen.dataframe), 1)` | Проверяет ожидаемое поведение указанного тестового сценария; несоответствие провалит тест. |
| 166 | `if __name__ == '__main__':` | Выбирает ветку только при указанном условии; не придумывает недостающие сведения. |
| 167 | `unittest.main()` | Продолжает выражение этого блока; выполняет ту же операцию, что описана для начала строки выше. |

## tests/ui/test_multistation.py

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 101 | `screen.toggle(key='technical_details').set_value(True).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |
| 156 | `screen.toggle(key='technical_details').set_value(True).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |
| 192 | `screen.toggle(key='technical_details').set_value(True).run(timeout=30)` | В тесте открывает или закрывает технический экран так же, как пользователь. |

## Что не менялось

Исходные CSV/Parquet, реестр v2, код генератора экологических отчётов, опубликованные отчёты v1, Ridge, FUEL-вычисления и сохранённые модельные результаты не редактировались. Контракт не переписан.

Команда запуска в UI README использует существующий интерпретатор .venv, запускает Streamlit и привязывает его к 127.0.0.1:8503. Она не публикует сайт в интернете.

Полный набор проверок, ограничения и перечень передачи записаны в отдельном UI-handoff. Старый release ZIP и материалы сдачи нужно обновить отдельным проходом.
