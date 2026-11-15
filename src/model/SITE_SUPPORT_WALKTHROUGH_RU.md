# Построчный разбор поддержки сайта

Добавлены только общий backend-адаптер и его тесты. Прежние модели, их методика, источники, публикации отчётов и UI не изменены. SITE_SUPPORT.md описывает поля, научные границы и примеры использования.

SiteSupport — один запрос/refresh, а не долгоживущий кэш. Система определяется dataset_id; экологический отчёт остаётся уровня площадки, а каждое утверждение имеет отдельную scope. Ни наличие модели, ни общий литературный контекст не дают заключения о безопасности.

Ниже каждая непустая физическая строка приведена дословно, блоками до восьми строк. Пустые строки лишь разделяют блоки. JSON содержит курируемые данные, а не ещё один алгоритм; его поля объяснены в SITE_SUPPORT.md.

## src/model/site_support.py

SHA-256: `8531dc16ff7c2dc80984ef225ca45b76613fbf5da5e3ce45b84c9d640eeb968b`.

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 1 | <code>"""Read-only data for drop journeys, month ribbons, evidence cards and catalogs."""</code> | Поясняет назначение блока; само по себе не выполняет вычислений. |
| 2 | <code>from copy import deepcopy</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 3 | <code>from datetime import date</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 4 | <code>import hashlib</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 5 | <code>import importlib</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 6 | <code>import json</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 7 | <code>from pathlib import Path</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 8 | <code>import sys</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 10 | <code>import pandas as pd</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 12 | <code>from .datasets import load_observations</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 13 | <code>from .environment_report import load_evidence, validate_claim, read_report</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 14 | <code>from .registry import REGISTRY_PATH, project_path, read_registry, sha256</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 16 | <code>CONTENT = 'src/model/site_support_data'</code> | Указывает единственную новую папку курируемых текстов/привязок без копии глобального SOURCES. |
| 17 | <code>AI_ROLE = ('Ridge estimates the temperature difference across a cooling system for a completed month. '</code> | Фиксирует честное короткое объяснение: Ridge оценивает температуру; отчёты формируются по источникам/правилам. |
| 18 | <code>           'Environmental reports use reviewed sources and rules, not a trained environmental-safety model.')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 19 | <code>ERRORS = (OSError, ValueError, KeyError, TypeError, ImportError)</code> | Перечисляет предсказуемые ошибки чтения/проверки для явных состояний API. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 22 | <code>def require(condition, message):</code> | Проверяет обязательное условие и даёт понятный отказ вместо неверных данных. |
| 23 | <code>    if not condition:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 24 | <code>        raise ValueError(message)</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 27 | <code>def catalog_version(dependencies):</code> | Считает версию каталога из отсортированных зависимостей, включая явно отсутствующие файлы. |
| 28 | <code>    return hashlib.sha256(json.dumps(dependencies, sort_keys=True).encode('utf-8')).hexdigest()</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 31 | <code>def read_catalog(root, relative_path='data/site_support/v1/catalog.json'):</code> | Читает сохранённый каталог только если все проверенные файлы и отсутствия по-прежнему совпадают. Новый появившийся отчёт тоже делает старый каталог устаревшим. |
| 32 | <code>    """A saved catalog is usable only while all checked files/absences still match."""</code> | Поясняет назначение блока; само по себе не выполняет вычислений. |
| 33 | <code>    catalog = json.loads(project_path(root, relative_path).read_text(encoding='utf-8'))</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 34 | <code>    require(catalog['schema_version'] == 1, 'Unsupported catalog version')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 35 | <code>    require(catalog_version(catalog['dependencies']) == catalog['catalog_version'], 'Catalog version mismatch')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 36 | <code>    for name, expected in catalog['dependencies'].items():</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 37 | <code>        path = project_path(root, name)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 38 | <code>        actual = sha256(path) if path.is_file() else None</code> | Проверяет текущие байты или реальное отсутствие файла, не только ранее записанный статус. |
| 39 | <code>        require(actual == expected, 'Catalog is stale; rebuild without training: ' + name)</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 40 | <code>    return catalog</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 43 | <code>def existing_readers():</code> | Переиспользует два существующих чистых read-only загрузчика, не копируя проверку результатов и не импортируя app.py/Streamlit. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 44 | <code>    """Reuse pure read-only UI adapters; never import app.py or Streamlit."""</code> | Поясняет назначение блока; само по себе не выполняет вычислений. |
| 45 | <code>    ui = str(Path(__file__).resolve().parents[1] / 'ui')</code> | Находит папку уже существующих read-only валидаторов по расположению файла. |
| 46 | <code>    if ui not in sys.path:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 47 | <code>        sys.path.insert(0, ui)</code> | Добавляет локальную область импорта для совместимости существующего legacy data_loader; приложение не запускает. |
| 48 | <code>    return (importlib.import_module('src.ui.multistation_loader'),</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 49 | <code>            importlib.import_module('src.ui.environment_loader'))</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 52 | <code>class SiteSupport:</code> | Объединяет методы одного read-only запроса или независимые проверки в понятную группу. |
| 53 | <code>    """One request/refresh snapshot. Do not retain this object in a global UI cache."""</code> | Поясняет назначение блока; само по себе не выполняет вычислений. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 54 | <code>    def __init__(self, root):</code> | Начинает один запрос/обновление: определяет корень, запоминает версию реестра и создаёт пустой локальный кэш таблиц. |
| 55 | <code>        self.root = Path(root).resolve()</code> | Определяет абсолютный корень, независимый от текущего пути запуска. |
| 56 | <code>        self.version = sha256(project_path(self.root, REGISTRY_PATH))</code> | Запоминает SHA-256 версии реестра для согласованного запроса. |
| 57 | <code>        registry = read_registry(self.root, verify=False)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 58 | <code>        self.entries = {entry['dataset_id']: entry for entry in registry['datasets']}</code> | Создаёт lookup точных dataset_id из проверенного реестра, а не имён файлов. |
| 59 | <code>        self.frames = {}</code> | Начинает пустой кэш только текущего запроса, не всех пользователей/станций. |
| 60 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 62 | <code>    def _stable(self):</code> | Не позволяет смешать данные двух версий реестра в одном запросе. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 63 | <code>        require(sha256(project_path(self.root, REGISTRY_PATH)) == self.version,</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 64 | <code>                'Registry changed; start a fresh request')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 66 | <code>    def _entry(self, identifier):</code> | Находит только точный dataset_id; неизвестный ID не заменяется Surry. |
| 67 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 68 | <code>        require(identifier in self.entries, 'Unknown dataset_id; no fallback system')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 69 | <code>        return self.entries[identifier]</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 71 | <code>    def _base(self, entry=None):</code> | Добавляет версию формата/реестра и при необходимости точную пару площадка/система. |
| 72 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 73 | <code>        result = {'schema_version': 1, 'registry_version': self.version}</code> | Хранит проверенный ответ/каталог, не необработанное предположение о готовности. |
| 74 | <code>        if entry:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 75 | <code>            result.update({key: entry[key] for key in ('dataset_id', 'plant_id_eia', 'plant_name', 'cooling_id_eia')})</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 76 | <code>        return result</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 78 | <code>    def _frame(self, entry):</code> | Проверяет заявленные единицы и хеши, вызывает существующий адаптер наблюдений; повторные вызовы сверяют хеши даже при локальном кэше. |
| 79 | <code>        require(entry['provenance']['source_units'] == 'degF' and entry['provenance']['units'] == 'degC',</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 80 | <code>                'Source units need review; do not infer units from values')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 81 | <code>        for metadata, path_key, hash_key in [(entry['observations'], 'path', 'sha256'),</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 82 | <code>                                             (entry['provenance'], 'raw_path', 'raw_sha256')]:</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 83 | <code>            require(sha256(project_path(self.root, metadata[path_key])) == metadata[hash_key], 'Source hash changed')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 84 | <code>        identifier = entry['dataset_id']</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 85 | <code>        if identifier not in self.frames:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 86 | <code>            self.frames[identifier] = load_observations(self.root, entry)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 87 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 88 | <code>        return self.frames[identifier]</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 90 | <code>    def timeline(self, identifier):</code> | Возвращает все192 календарных месяца с исходными пригодными измерениями или явным статусом/null, не прогнозами и не интерполяцией. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 91 | <code>        entry = self._entry(identifier)</code> | Выбирает точную запись системы из реестра. |
| 92 | <code>        payload = {**self._base(entry), 'units': 'degC', 'source_units': 'degF',</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 93 | <code>                   'kind': 'reported_measurement', 'data_status': entry['status'],</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 94 | <code>                   'limitations': entry['limitations'], 'calendar_period': ['2010-01', '2025-12']}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 95 | <code>        try:</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 96 | <code>            frame = self._frame(entry).set_index('report_month')</code> | Получает исходные канонические строки существующего адаптера; месяцы не перемешиваются. |
| 97 | <code>        except ERRORS as exc:</code> | Перехватывает перечисленные ошибки и возвращает явное состояние недоступности/проверки без чужого fallback. |
| 98 | <code>            return {**payload, 'state': 'source_unavailable', 'rows': [], 'reason': str(exc)}</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 99 | <code>        rows = []</code> | Начинает локальный список месяцев/оценок; записи не копируются из другой системы. |
| 100 | <code>        for month in pd.period_range('2010-01', '2025-12', freq='M').astype(str):</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 101 | <code>            row = {'report_month': month, 'intake_temperature_c': None, 'discharge_temperature_c': None,</code> | Создаёт месяц с null до подтверждения существования и пригодности реальной исходной записи. |
| 102 | <code>                   'delta_t_c': None, 'record_present': month in frame.index, 'eligible_measured': False,</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 103 | <code>                   'pair_available': False, 'source_method': None, 'status': 'missing_month',</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 104 | <code>                   'reasons': ['No source record for this month'], 'kind': 'reported_measurement'}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 105 | <code>            if row['record_present']:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 106 | <code>                source = frame.loc[month]</code> | Берёт строку именно совпавшего отчётного месяца. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 107 | <code>                row.update(eligible_measured=bool(source.eligible_measured), pair_available=bool(source.pair_available),</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 108 | <code>                           source_method=str(source.temperature_method), reasons=[])</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 109 | <code>                if entry['status'] in {'review_required', 'blocked', 'reference_only'}:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 110 | <code>                    row['status'] = 'review_required' if entry['status'] == 'review_required' else 'blocked'</code> | Записывает соответствующий реальный статус/проверенное число; исключённые значения остаются null. |
| 111 | <code>                    row['reasons'] = entry['limitations'] + entry.get('review_months', {}).get(month, [])</code> | Записывает соответствующий реальный статус/проверенное число; исключённые значения остаются null. |
| 112 | <code>                elif not source.pair_available:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 113 | <code>                    row.update(status='missing_temperatures', reasons=['Incomplete or nonfinite source temperature pair'])</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 114 | <code>                elif not source.eligible_measured:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 115 | <code>                    row.update(status='excluded_method', reasons=['Source method is not an explicitly measured thermometer method'])</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 116 | <code>                else:</code> | Обрабатывает другой случай отдельно, не смешивая подтверждённые, исключённые и неизвестные данные. |
| 117 | <code>                    row['status'] = 'verified_measurement'</code> | Записывает соответствующий реальный статус/проверенное число; исключённые значения остаются null. |
| 118 | <code>                    for field in ('intake_temperature_c', 'discharge_temperature_c', 'delta_t_c'):</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 119 | <code>                        row[field] = float(source[field])</code> | Записывает соответствующий реальный статус/проверенное число; исключённые значения остаются null. |
| 120 | <code>            rows.append(row)</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 121 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 122 | <code>        return {**payload, 'state': 'available', 'rows': rows}</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 124 | <code>    def predictions(self, identifier):</code> | Отдельно читает только сохранённые проверенные оценки и baseline; ничего не обучает и не дополняет ими измерения. |
| 125 | <code>        entry = self._entry(identifier)</code> | Выбирает точную запись системы из реестра. |
| 126 | <code>        payload = {**self._base(entry), 'kind': 'model_estimate', 'units': 'degC', 'rows': [],</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 127 | <code>                   'label': 'Saved retrospective estimates, not measured temperatures'}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 128 | <code>        if entry['status'] != 'ready_for_model_check' or entry['model_status'] not in {'existing_verified', 'evaluated_verified'}:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 129 | <code>            return {**payload, 'state': 'model_not_ready'}</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 130 | <code>        try:</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 131 | <code>            frame = self._frame(entry)</code> | Получает исходные канонические строки существующего адаптера; месяцы не перемешиваются. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 132 | <code>            measured = frame.loc[frame.eligible_measured].copy()</code> | Берёт только eligible-строки для сверки сохранённых оценок, не создавая новые цели. |
| 133 | <code>            measured['reported_delta_t_c'] = measured.delta_t_c</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 134 | <code>            verifier, _ = existing_readers()</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 135 | <code>            result, scores = verifier.verified_results(entry, measured, self.version, self.root)</code> | Переиспользует существующую независимую проверку полного экспортного набора и MAE. |
| 136 | <code>            fields = ('model_delta_t_c', 'median_baseline_delta_t_c', 'seasonal_baseline_delta_t_c')</code> | Явно разрешает только поля сохранённых модельной/двух baseline-оценок. |
| 137 | <code>            payload['rows'] = [{'report_month': month, 'kind': 'model_estimate',</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 138 | <code>                                **{field: float(row[field]) for field in fields}} for month, row in result.iterrows()]</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 139 | <code>            payload.update(mae_c=scores, test_n=len(result))</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 140 | <code>        except ERRORS as exc:</code> | Перехватывает перечисленные ошибки и возвращает явное состояние недоступности/проверки без чужого fallback. |
| 141 | <code>            return {**payload, 'state': 'results_unavailable', 'rows': [], 'reason': str(exc)}</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 142 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 143 | <code>        return {**payload, 'state': 'verified'}</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 145 | <code>    def _content(self):</code> | Проверяет хеши прошедшего содержательную проверку текста/привязок, затем читает JSON. Хеш подтверждает версию курации, не научную истинность. |
| 146 | <code>        index = json.loads(project_path(self.root, CONTENT + '/review.json').read_text(encoding='utf-8'))</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 147 | <code>        for name, expected in index['sha256'].items():</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 148 | <code>            require(sha256(project_path(self.root, CONTENT + '/' + name)) == expected, 'Story content changed since review')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 149 | <code>        return {name: json.loads(project_path(self.root, CONTENT + '/' + name).read_text(encoding='utf-8'))</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 150 | <code>                for name in index['sha256']}</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 152 | <code>    def journey(self, identifier):</code> | Выбирает семейство охлаждения по проверенным словарям кодов. Неизвестное/смешанное становится учебным примером; Surry site-контекст не переносится другим. |
| 153 | <code>        entry = self._entry(identifier)</code> | Выбирает точную запись системы из реестра. |
| 154 | <code>        content = self._content()['journey.json']</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 155 | <code>        codes = set(entry['cooling_types'])</code> | Берёт реально сообщённые исторические типы из выбранной записи. |
| 156 | <code>        family = next((key for key, allowed in content['families'].items() if codes and codes &lt;= set(allowed)), 'unknown')</code> | Допускает семейство только при непустом наборе полностью известных совместимых кодов; иначе unknown. |
| 157 | <code>        mode = 'general_educational' if family == 'unknown' else 'historical_reported_family'</code> | Заметно отделяет исторически сообщённый класс от общей учебной схемы. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 158 | <code>        steps = deepcopy(content['steps'][family])</code> | Копирует подходящую курируемую схему в отдельный ответ без изменения общих шаблонов. |
| 159 | <code>        for step in steps:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 160 | <code>            step['confirmed_for_system'] = (f"Historical registry codes {', '.join(sorted(codes))} report this cooling family. "</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 161 | <code>                                            'This is not a current pipe map.' if family != 'unknown'</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 162 | <code>                                            else 'The cooling-system type is not established for this explanation.')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 163 | <code>            step['sources'].append({'title': 'Selected-system registry provenance',</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 164 | <code>                                    'url': entry['provenance']['source_url'], 'role': 'official_statistics',</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 165 | <code>                                    'locator': entry['dataset_id'] + ' / cooling_types', 'period': entry['period']})</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 166 | <code>        if entry['plant_id_eia'] == 3806 and family == 'once_through':</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 167 | <code>            for step in steps:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 168 | <code>                step['site_context'] = content['surry_site_context'][step['id']]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 169 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 170 | <code>        return {**self._base(entry), 'cooling_family': family, 'scheme_mode': mode,</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 171 | <code>                'cooling_type_codes': sorted(codes), 'period': entry['period'], 'steps': steps,</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 172 | <code>                'limitations': content['limitations'], 'ai_role': AI_ROLE}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 174 | <code>    def claim_details(self, plant_id, cooling_id=None):</code> | Связывает атомарные части неизменённого отчёта с проверенными утверждениями/источниками/периодами; проверяет полное покрытие и исключает CW1 при выборе CW2. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 175 | <code>        require(type(plant_id) is int, 'Use an integer plant ID')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 176 | <code>        systems = [entry for entry in self.entries.values() if entry['plant_id_eia'] == plant_id]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 177 | <code>        require(bool(systems), 'Unknown plant ID')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 178 | <code>        if cooling_id is not None:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 179 | <code>            require(any(e['cooling_id_eia'] == cooling_id for e in systems), 'Cooling system belongs to another plant')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 180 | <code>        _, reader = existing_readers()</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 181 | <code>        snapshot = reader.report_snapshot(plant_id, self.root)</code> | Читает существующую атомарную публикацию через прежний reader. |
| 182 | <code>        base = {**self._base(), 'plant_id_eia': plant_id, 'cooling_id_eia': cooling_id,</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 183 | <code>                'report_state': snapshot.state, 'statements': [], 'omitted_system_statement_ids': []}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 184 | <code>        if snapshot.state != 'ready':</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 185 | <code>            return base</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 186 | <code>        try:</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 187 | <code>            sources, ledger = load_evidence(self.root)</code> | Читает существующий проверенный корпус источников/утверждений. |
| 188 | <code>            public, technical = snapshot.report, snapshot.technical</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 189 | <code>            approved = {c['id']: c for c in ledger['claims'] if c['review_status'] == 'reviewed_for_support'}</code> | Отбирает только source-support-reviewed утверждения; отвергнутые не используются. |
| 190 | <code>            for claim in technical['accepted_claims']:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 191 | <code>                require(claim == approved.get(claim['id']), 'Published claim differs from reviewed ledger')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 192 | <code>                validate_claim(claim, sources, plant_id, date.today())</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 193 | <code>            bundle = self._content()['claim_links.json'][str(plant_id)]</code> | Берёт дополнение привязок только для нужной площадки. |
| 194 | <code>            directory = project_path(self.root, f'data/environment_reports/v1/eia_{plant_id}')</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 195 | <code>            require(sha256(directory / 'report.en.json') == bundle['report_sha256'], 'Claim annotations need review for new report')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 196 | <code>            require(technical['review_index_sha256'] == bundle['evidence_index_sha256'], 'Evidence review version changed')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 197 | <code>            targets = {'summary': [public['summary']], **{s['id']: s['paragraphs'] for s in public['sections']}}</code> | Связывает summary/разделы с неизменённым опубликованным текстом. |
| 198 | <code>            coverage = {(key, i): set() for key, texts in targets.items() for i in range(len(texts))}</code> | Отслеживает покрытие каждого символа фраз, а не приписывает источник целому абзацу. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 199 | <code>            identifiers = set()</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 200 | <code>            for card in bundle['statements']:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 201 | <code>                require(card['statement_id'] not in identifiers, 'Duplicate statement ID')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 202 | <code>                identifiers.add(card['statement_id'])</code> | Запоминает стабильный смысловой ID и позволяет обнаружить повтор. |
| 203 | <code>                target = targets[card['target']][card['paragraph_index']]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 204 | <code>                start, end = card['span']</code> | Получает точные границы фрагмента в привязанной по хешу версии текста. |
| 205 | <code>                require(0 &lt;= start &lt; end &lt;= len(target) and target[start:end] == card['display_span'], 'Statement span mismatch')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 206 | <code>                covered = coverage[(card['target'], card['paragraph_index'])]</code> | Находит уже покрытые позиции этого абзаца для проверки пересечений. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 207 | <code>                require(not covered.intersection(range(start, end)), 'Overlapping statement annotations')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 208 | <code>                covered.update(range(start, end))</code> | Отмечает символы, для которых уже есть отдельная связь с источником или явно указанная граница знания. |
| 209 | <code>                require(bool(card['limitation']) and bool(card['review_basis']), 'Statement lacks review boundary')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 210 | <code>                require(card['text_role'] in {'source_fact', 'scope_limit', 'evidence_gap', 'method_explanation'}, 'Unknown text role')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 211 | <code>                require(card['text_role'] != 'source_fact' or bool(card['sources'] and card['parent_claim_ids']),</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 212 | <code>                        'Factual statement lacks evidence')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 213 | <code>                for parent in card['parent_claim_ids']:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 214 | <code>                    require(parent in approved and approved[parent]['plant_id_eia'] == plant_id, 'Unsupported parent claim')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 215 | <code>                for ref in card['sources']:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 216 | <code>                    require(ref['source_id'] in sources and sources[ref['source_id']]['access_state'] == 'reviewed_content', 'Unreviewed card source')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 217 | <code>                    require(ref['url'] == sources[ref['source_id']]['url'] and ref['role'] == sources[ref['source_id']]['role'],</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 218 | <code>                            'Source URL or role differs from reviewed source')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 219 | <code>                    require(any(ref['source_id'] == item['source_id'] and ref['locator'] == item['locator']</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 220 | <code>                                for parent in card['parent_claim_ids'] for item in approved[parent]['references']), 'Citation does not support this span')</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 221 | <code>                scope = card['scope']</code> | Берёт явно записанный уровень: система, площадка или общий контекст. |
| 222 | <code>                require(scope['plant_id_eia'] == plant_id, 'Statement scope belongs to another plant')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 223 | <code>                if cooling_id and scope['level'] == 'system' and scope['cooling_id_eia'] != cooling_id:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 224 | <code>                    base['omitted_system_statement_ids'].append(card['statement_id'])</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 225 | <code>                else:</code> | Обрабатывает другой случай отдельно, не смешивая подтверждённые, исключённые и неизвестные данные. |
| 226 | <code>                    base['statements'].append(deepcopy(card))</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 227 | <code>            for (key, i), positions in coverage.items():</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 228 | <code>                require(all(j in positions or character.isspace() for j, character in enumerate(targets[key][i])),</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 229 | <code>                        'A displayed phrase has no evidence or explicit review-boundary annotation')</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 230 | <code>            require(sha256(directory / 'ready.json') == snapshot.version, 'Report changed during request')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 231 | <code>        except ERRORS as exc:</code> | Перехватывает перечисленные ошибки и возвращает явное состояние недоступности/проверки без чужого fallback. |
| 232 | <code>            return {**base, 'report_state': 'review_required', 'statements': [], 'reason': str(exc)}</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 233 | <code>        self._stable()</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 234 | <code>        return base</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 236 | <code>    def catalog(self):</code> | Заново проверяет измерения, оценки и отчёты, затем собирает раздельные признаки площадки и систем без экологического рейтинга. |
| 237 | <code>        dependencies = self._dependencies()</code> | Фиксирует все текущие версии/отсутствия до проверки каталога. |
| 238 | <code>        systems = []</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 239 | <code>        for entry in self.entries.values():</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 240 | <code>            timeline = self.timeline(entry['dataset_id'])</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 241 | <code>            predictions = self.predictions(entry['dataset_id'])</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 242 | <code>            count = sum(row['status'] == 'verified_measurement' for row in timeline['rows'])</code> | Считает только действительно отображаемые проверенные месяцы. |
| 243 | <code>            systems.append({**self._base(entry), 'data_status': entry['status'],</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 244 | <code>                            'has_verified_measurements': count &gt; 0, 'verified_measurement_months': count,</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 245 | <code>                            'has_verified_model_results': predictions['state'] == 'verified',</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 246 | <code>                            'model_result_months': predictions.get('test_n', 0),</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 247 | <code>                            'requires_review': entry['status'] == 'review_required' or timeline['state'] == 'source_unavailable'</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 248 | <code>                                               or predictions['state'] == 'results_unavailable',</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 249 | <code>                            'data_blocked': entry['status'] == 'blocked', 'no_temperature_pairs': entry['status'] == 'reference_only',</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 250 | <code>                            'measurement_state': timeline['state'], 'model_state': predictions['state'],</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 251 | <code>                            'limitations': entry['limitations']})</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 252 | <code>        _, reader = existing_readers()</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 253 | <code>        plants = []</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 254 | <code>        for plant_id in sorted({entry['plant_id_eia'] for entry in self.entries.values()}):</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 255 | <code>            entries = [entry for entry in systems if entry['plant_id_eia'] == plant_id]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 256 | <code>            report = reader.report_snapshot(plant_id, self.root)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 257 | <code>            details = self.claim_details(plant_id) if report.state == 'ready' else None</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 258 | <code>            substantive = bool(details and details['report_state'] == 'ready' and any(</code> | Считает отчёт содержательным только после проверки связей и наличия site-наблюдения/оценки, а не имени файла. |
| 259 | <code>                c['kind'] in {'observation', 'model_estimate'} for c in report.technical['accepted_claims']))</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 260 | <code>            plants.append({'plant_id_eia': plant_id, 'plant_name': entries[0]['plant_name'],</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 261 | <code>                           'has_substantive_environment_report': substantive,</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 262 | <code>                           'has_insufficient_evidence_report': report.state == 'insufficient_evidence',</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 263 | <code>                           'report_state': details['report_state'] if details else report.state,</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 264 | <code>                           'expert_review_status': 'not_performed',</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 265 | <code>                           'system_count': len(entries),</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 266 | <code>                           **{'any_system_' + flag: any(e[flag] for e in entries) for flag in</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 267 | <code>                              ('has_verified_measurements', 'has_verified_model_results', 'requires_review', 'data_blocked')},</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 268 | <code>                           'verified_measurement_systems': sum(e['has_verified_measurements'] for e in entries),</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 269 | <code>                           'verified_model_systems': sum(e['has_verified_model_results'] for e in entries)})</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 270 | <code>        require(self._dependencies() == dependencies, 'Catalog inputs changed during verification; retry')</code> | Требует точно указанное условие; нарушение приводит к объяснённому отказу, а не выдуманному значению. |
| 271 | <code>        return {**self._base(), 'plants': plants, 'systems': systems, 'ai_role': AI_ROLE,</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 272 | <code>                'dependencies': dependencies, 'catalog_version': catalog_version(dependencies)}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 274 | <code>    def _dependencies(self):</code> | Собирает версии всех входов каталога: источники, результаты, код/курация и в том числе отсутствующие экологические публикации. |
| 275 | <code>        names = {REGISTRY_PATH, 'src/model/site_support.py', 'src/model/environment_report.py',</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 276 | <code>                 'src/model/datasets.py', 'src/model/registry.py', 'src/ui/multistation_loader.py',</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 277 | <code>                 'src/ui/environment_loader.py', 'src/ui/data_loader.py',</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 278 | <code>                 CONTENT + '/review.json', CONTENT + '/claim_links.json', CONTENT + '/journey.json'}</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 279 | <code>        names.update('src/model/environment_evidence/' + name for name in</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 280 | <code>                     ['review_index.json', 'claims.json', 'source_catalog.json', 'technical_values.json'])</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 281 | <code>        for entry in self.entries.values():</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 282 | <code>            names.update([entry['observations']['path'], entry['provenance']['raw_path']])</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 283 | <code>            if entry['results_path']:</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 284 | <code>                names.update([entry['results_path'], entry['artifacts']['future_artifacts_dir'] + '/metrics.json'])</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 285 | <code>                if entry.get('evaluation'):</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 286 | <code>                    names.add(entry['evaluation']['verification_path'])</code> | Добавляет путь в множество зависимостей, чтобы разные версии артефактов не делали каталог незаметно устаревшим. |
| 287 | <code>            names.update(f"data/environment_reports/v1/eia_{entry['plant_id_eia']}/{name}" for name in</code> | Добавляет перечисленные поля/запись только в локальную структуру ответа; исходный реестр/отчёт не переписывается. |
| 288 | <code>                         ['ready.json', 'report.en.json', 'report.en.md', 'technical.json'])</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 289 | <code>        return {name: sha256(project_path(self.root, name)) if project_path(self.root, name).is_file() else None</code> | Возвращает указанную структуру текущей системы/площадки, не записывает исходники и не вызывает fit. |
| 290 | <code>                for name in sorted(names)}</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |

## tests/model/test_site_support.py

SHA-256: `c9c48ffb6ad685e1251d9360695cf5c9087c35c7c2802dff70c9f269677c3c96`.

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 1 | <code>"""Scientific scope, identity and read-only data contracts for future UI work."""</code> | Поясняет назначение блока; само по себе не выполняет вычислений. |
| 2 | <code>from copy import deepcopy</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 3 | <code>import json</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 4 | <code>from pathlib import Path</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 5 | <code>import sys</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 6 | <code>import tempfile</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 7 | <code>import unittest</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 8 | <code>from unittest.mock import patch</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 10 | <code>ROOT = Path(__file__).resolve().parents[2]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 11 | <code>sys.path.insert(0, str(ROOT))</code> | Добавляет локальную область импорта для совместимости существующего legacy data_loader; приложение не запускает. |
| 12 | <code>from src.model.site_support import SiteSupport, AI_ROLE, read_catalog, catalog_version</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 13 | <code>from src.model.environment_report import read_report</code> | Подключает указанную библиотеку или существующий reader/адаптер; обучение и онлайн-поиск не запускаются. |
| 15 | <code>SURRY = 'eia_3806_435731'</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 16 | <code>CW2 = 'eia_3806_435732'</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 17 | <code>CALVERT = 'eia_6011_535953303432'</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 20 | <code>class StorySupportTests(unittest.TestCase):</code> | Объединяет методы одного read-only запроса или независимые проверки в понятную группу. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 21 | <code>    def setUp(self):</code> | Создаёт новый контекст для каждого теста, чтобы состояние другой системы/проверки не переносилось. |
| 22 | <code>        self.provider = SiteSupport(ROOT)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 24 | <code>    def test_actual_calendar_units_and_exclusions(self):</code> | На настоящем Surry проверяет192/188 месяцев, Fahrenheit/Celsius, арифметику и исключённый2024-08 без чисел. |
| 25 | <code>        data = self.provider.timeline(SURRY)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 26 | <code>        self.assertEqual(len(data['rows']), 192)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 27 | <code>        good = [r for r in data['rows'] if r['status'] == 'verified_measurement']</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 28 | <code>        self.assertEqual(len(good), 188)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 29 | <code>        self.assertEqual((data['source_units'], data['units']), ('degF', 'degC'))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 30 | <code>        frame = self.provider._frame(self.provider._entry(SURRY)).set_index('report_month')</code> | Получает исходные канонические строки существующего адаптера; месяцы не перемешиваются. |
| 31 | <code>        for row in good:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 32 | <code>            original = frame.loc[row['report_month']]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 33 | <code>            self.assertAlmostEqual(row['intake_temperature_c'], (original.intake_temperature_f - 32) * 5 / 9, places=5)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 34 | <code>            self.assertAlmostEqual(row['delta_t_c'], row['discharge_temperature_c'] - row['intake_temperature_c'], places=5)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 35 | <code>        excluded = next(r for r in data['rows'] if r['report_month'] == '2024-08')</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 36 | <code>        self.assertFalse(excluded['eligible_measured'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 37 | <code>        self.assertIsNone(excluded['delta_t_c'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 38 | <code>        self.assertEqual(excluded['status'], 'excluded_method')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 40 | <code>    def test_missing_row_and_temperature_not_interpolated(self):</code> | В памяти имитирует отсутствующую строку и неполную пару, проверяя явные статусы без интерполяции. |
| 41 | <code>        entry = self.provider._entry(SURRY)</code> | Выбирает точную запись системы из реестра. |
| 42 | <code>        frame = self.provider._frame(entry).copy()</code> | Получает исходные канонические строки существующего адаптера; месяцы не перемешиваются. |
| 43 | <code>        frame = frame.loc[frame.report_month.ne('2010-02')].copy()</code> | Получает исходные канонические строки существующего адаптера; месяцы не перемешиваются. |
| 44 | <code>        index = frame.index[frame.report_month.eq('2010-01')][0]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 45 | <code>        frame.loc[index, 'pair_available'] = False</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 46 | <code>        frame.loc[index, 'eligible_measured'] = False</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 47 | <code>        with patch.object(self.provider, '_frame', return_value=frame):</code> | Временно меняет только тестовый вход/функцию в памяти; настоящие файлы и модели не изменяет. |
| 48 | <code>            rows = {r['report_month']: r for r in self.provider.timeline(SURRY)['rows']}</code> | Начинает локальный список месяцев/оценок; записи не копируются из другой системы. |
| 49 | <code>        self.assertEqual(rows['2010-02']['status'], 'missing_month')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 50 | <code>        self.assertFalse(rows['2010-02']['record_present'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 51 | <code>        self.assertEqual(rows['2010-01']['status'], 'missing_temperatures')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 52 | <code>        self.assertIsNone(rows['2010-01']['intake_temperature_c'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 54 | <code>    def test_review_numbers_withheld_and_no_cross_system_model(self):</code> | Проверяет блокировку сомнительной CW2, точные22/24 месяца моделей и возврат к Surry без чужих оценок. |
| 55 | <code>        data = self.provider.timeline(CW2)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 56 | <code>        self.assertTrue(any(row['eligible_measured'] for row in data['rows']))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 57 | <code>        self.assertTrue(all(row['delta_t_c'] is None for row in data['rows']))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 58 | <code>        self.assertEqual(self.provider.predictions(CW2)['state'], 'model_not_ready')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 59 | <code>        for identifier, count in [(SURRY, 22), (CALVERT, 24), (SURRY, 22)]:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 60 | <code>            result = self.provider.predictions(identifier)</code> | Хранит проверенный ответ/каталог, не необработанное предположение о готовности. |
| 61 | <code>            self.assertEqual(result['state'], 'verified')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 62 | <code>            self.assertEqual(len(result['rows']), count)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 63 | <code>            self.assertTrue(all(row['kind'] == 'model_estimate' for row in result['rows']))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 64 | <code>            self.assertEqual(result['dataset_id'], identifier)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 66 | <code>    def test_unavailable_source_or_result_never_fake(self):</code> | Проверяет пустой ответ при сломанном источнике/результате и отказ неизвестному ID. |
| 67 | <code>        with patch.object(self.provider, '_frame', side_effect=ValueError('source changed')):</code> | Временно меняет только тестовый вход/функцию в памяти; настоящие файлы и модели не изменяет. |
| 68 | <code>            timeline = self.provider.timeline(SURRY)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 69 | <code>            self.assertEqual((timeline['state'], timeline['rows']), ('source_unavailable', []))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 70 | <code>            self.assertEqual(self.provider.predictions(SURRY)['state'], 'results_unavailable')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 71 | <code>        with self.assertRaisesRegex(ValueError, 'Unknown dataset'):</code> | Требует ожидаемый отказ/причину в отрицательном сценарии. |
| 72 | <code>            self.provider.timeline('eia_3806_fake')</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 74 | <code>    def test_units_are_not_guessed(self):</code> | Неизвестная исходная единица не должна превращаться в предполагаемые градусы по величине чисел. |
| 75 | <code>        self.provider.entries[SURRY]['provenance']['source_units'] = 'unknown'</code> | Изменяет только тестовую копию/контекст в памяти для проверки ошибки или другого семейства. |
| 76 | <code>        result = self.provider.timeline(SURRY)</code> | Хранит проверенный ответ/каталог, не необработанное предположение о готовности. |
| 77 | <code>        self.assertEqual(result['state'], 'source_unavailable')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 78 | <code>        self.assertEqual(result['rows'], [])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 80 | <code>    def test_journey_family_and_general_fallback(self):</code> | Проверяет прямоточный Surry, отсутствие переноса site-контекста на Calvert и учебный/оборотный варианты. |
| 81 | <code>        path = self.provider.journey(SURRY)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 82 | <code>        self.assertEqual(path['cooling_family'], 'once_through')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 83 | <code>        self.assertEqual(len(path['steps']), 3)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 84 | <code>        self.assertTrue(all(s['site_context']['source']['role'] == 'operator' for s in path['steps']))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 85 | <code>        other = self.provider.journey(CALVERT)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 86 | <code>        self.assertFalse(any('site_context' in step for step in other['steps']))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 87 | <code>        for codes, family in [([], 'unknown'), (['O', 'R'], 'unknown'), (['RC'], 'recirculating')]:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 88 | <code>            altered = deepcopy(self.provider._entry(SURRY))</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 89 | <code>            altered['cooling_types'] = codes</code> | Изменяет только тестовую копию/контекст в памяти для проверки ошибки или другого семейства. |
| 90 | <code>            with patch.object(self.provider, '_entry', return_value=altered):</code> | Временно меняет только тестовый вход/функцию в памяти; настоящие файлы и модели не изменяет. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 91 | <code>                data = self.provider.journey(SURRY)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 92 | <code>            self.assertEqual(data['cooling_family'], family)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 93 | <code>            if family == 'unknown':</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 94 | <code>                self.assertEqual(data['scheme_mode'], 'general_educational')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 95 | <code>            if family == 'recirculating':</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 96 | <code>                self.assertIn('reuse', data['steps'][2]['general_explanation'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 98 | <code>    def test_atomic_claim_sources_and_system_scope(self):</code> | Проверяет25 связей, раздельные ссылки VDH для находки/метода, общий климатический контекст, исключениеCW1 и честный отказ других площадок. |
| 99 | <code>        data = self.provider.claim_details(3806)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 100 | <code>        self.assertEqual(data['report_state'], 'ready')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 101 | <code>        self.assertEqual(len(data['statements']), 25)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 102 | <code>        cards = {c['statement_id']: c for c in data['statements']}</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 103 | <code>        h3 = cards['eia_3806.water.tritium_detected']</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 104 | <code>        self.assertEqual(len(h3['sources']), 1)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 105 | <code>        self.assertNotIn('p. 10', h3['sources'][0]['locator'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 106 | <code>        method = cards['eia_3806.water.nondetection_boundary']</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 107 | <code>        self.assertEqual(method['text_role'], 'method_explanation')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 108 | <code>        self.assertIn('p. 10', method['sources'][0]['locator'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 109 | <code>        self.assertEqual(cards['eia_3806.climate.general_lifecycle_context']['scope']['level'], 'general')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 110 | <code>        other = self.provider.claim_details(3806, 'CW2')</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 111 | <code>        self.assertEqual(len(other['omitted_system_statement_ids']), 3)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 112 | <code>        self.assertFalse(any(c['scope']['level'] == 'system' for c in other['statements']))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 113 | <code>        self.assertEqual(self.provider.claim_details(6011)['statements'], [])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 114 | <code>        self.assertEqual(self.provider.claim_details(6014)['report_state'], 'missing')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 115 | <code>        with self.assertRaisesRegex(ValueError, 'another plant'):</code> | Требует ожидаемый отказ/причину в отрицательном сценарии. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 116 | <code>            self.provider.claim_details(6011, 'CW1')</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 118 | <code>    def test_bad_link_or_incomplete_span_fails_closed(self):</code> | Ломает ссылку или удаляет часть покрытия только в памяти: карточки должны быть скрыты до проверки. |
| 119 | <code>        for mutation in ['citation', 'span']:</code> | Повторяет эту проверку/действие для перечисленных записей только в текущей области. |
| 120 | <code>            content = self.provider._content()</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 121 | <code>            card = content['claim_links.json']['3806']['statements'][0]</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 122 | <code>            if mutation == 'citation':</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 123 | <code>                card['sources'][0]['source_id'] = 'operator_legacy'</code> | Изменяет только тестовую копию/контекст в памяти для проверки ошибки или другого семейства. |
| 124 | <code>            else:</code> | Обрабатывает другой случай отдельно, не смешивая подтверждённые, исключённые и неизвестные данные. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 125 | <code>                content['claim_links.json']['3806']['statements'].pop()</code> | Продолжает предшествующий вызов/словарь: перечисляет его точные поля, параметры или условия; отдельного скрытого действия нет. |
| 126 | <code>            with patch.object(self.provider, '_content', return_value=content):</code> | Временно меняет только тестовый вход/функцию в памяти; настоящие файлы и модели не изменяет. |
| 127 | <code>                data = self.provider.claim_details(3806)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 128 | <code>            self.assertEqual(data['report_state'], 'review_required')</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 129 | <code>            self.assertEqual(data['statements'], [])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 131 | <code>    def test_existing_report_reader_unchanged_and_registry_refresh(self):</code> | Проверяет совместимость опубликованного v1-отчёта, устаревший контекст и точную роль ИИ. |
| 132 | <code>        old = read_report(ROOT / 'data/environment_reports/v1/eia_3806', 3806)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 133 | <code>        self.assertEqual(old['report_version'], 1)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 134 | <code>        self.provider.claim_details(3806)</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 135 | <code>        self.assertEqual(read_report(ROOT / 'data/environment_reports/v1/eia_3806', 3806), old)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 136 | <code>        self.provider.version = 'outdated'</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 137 | <code>        with self.assertRaisesRegex(ValueError, 'fresh request'):</code> | Требует ожидаемый отказ/причину в отрицательном сценарии. |
| 138 | <code>            self.provider.timeline(SURRY)</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 139 | <code>        self.assertIn('not a trained environmental-safety model', AI_ROLE)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 141 | <code>    def test_checked_catalog_has_combining_flags(self):</code> | Читает фактически проверенный каталог и проверяет одновременные независимые признаки Surry/Calvert,66/102,17 моделей и38 измеренных систем. |
| 142 | <code>        catalog = read_catalog(ROOT)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 143 | <code>        self.assertEqual((len(catalog['plants']), len(catalog['systems'])), (66, 102))</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 144 | <code>        self.assertEqual(sum(s['has_verified_model_results'] for s in catalog['systems']), 17)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 145 | <code>        self.assertEqual(sum(s['has_verified_measurements'] for s in catalog['systems']), 38)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 146 | <code>        surry = next(p for p in catalog['plants'] if p['plant_id_eia'] == 3806)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 147 | <code>        self.assertTrue(surry['has_substantive_environment_report'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 148 | <code>        self.assertTrue(surry['any_system_requires_review'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 149 | <code>        self.assertEqual(surry['verified_model_systems'], 1)</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 150 | <code>        calvert = next(p for p in catalog['plants'] if p['plant_id_eia'] == 6011)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 151 | <code>        self.assertTrue(calvert['has_insufficient_evidence_report'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 152 | <code>        self.assertTrue(calvert['any_system_has_verified_model_results'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 153 | <code>        self.assertFalse(calvert['has_substantive_environment_report'])</code> | Сравнивает настоящий результат с явно указанным ожиданием и делает тест неуспешным при нарушении. |
| 155 | <code>    def test_saved_catalog_not_stale_when_a_report_appears(self):</code> | В temp проверяет, что появление ранее отсутствовавшего файла инвалидирует сохранённый каталог. |
| 156 | <code>        with tempfile.TemporaryDirectory() as directory:</code> | Создаёт отдельную временную папку для проверки появления файла, не затрагивая проектные данные. |
| 157 | <code>            root = Path(directory)</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 158 | <code>            deps = {'new-report.json': None}</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 159 | <code>            value = {'schema_version': 1, 'dependencies': deps, 'catalog_version': catalog_version(deps)}</code> | Создаёт тестовый каталог с явной отсутствующей зависимостью. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 160 | <code>            (root / 'catalog.json').write_text(json.dumps(value), encoding='utf-8')</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 161 | <code>            read_catalog(root, 'catalog.json')</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 162 | <code>            (root / 'new-report.json').write_text('{}', encoding='utf-8')</code> | Сохраняет явно указанное промежуточное значение в текущем запросе/тесте без изменения модели или исходника. |
| 163 | <code>            with self.assertRaisesRegex(ValueError, 'stale'):</code> | Требует ожидаемый отказ/причину в отрицательном сценарии. |
| 164 | <code>                read_catalog(root, 'catalog.json')</code> | Запускает описанную выше проверку/действие с явным ID или путём, без обучения. |
| 167 | <code>if __name__ == '__main__':</code> | Проверяет конкретное условие перед соответствующей веткой; статус/область не угадываются. |
| 168 | <code>    unittest.main()</code> | Разрешает отдельный запуск только этого тестового файла. |

