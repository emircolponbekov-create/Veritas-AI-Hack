# Построчный разбор многосистемной подготовки

Разбор относится к новым файлам; прежний model.py не изменён. Каждый блок содержит до 12 строк; номера — настоящие номера в файле. Пустые строки только разделяют блоки и не выполняют действий.
Запускать подготовку, а не обучение. Для команд и общих понятий сначала прочитайте MULTISTATION.md. Для регрессий используется блокировка train_model и Ridge.fit.

## src/model/registry.py

### Строки 1–12

```python
"""Read dataset metadata without importing or executing the ML pipeline."""
from pathlib import Path
import hashlib
import json

REGISTRY_PATH = 'data/model_artifacts/multistation/registry.json'
STATUSES = {'ready_for_model_check', 'review_required', 'measurements_only',
            'blocked', 'reference_only'}


def dataset_id(plant_id, system_id):
    return f'eia_{int(plant_id)}_{str(system_id).encode("utf-8").hex()}'
```

| Строка | Что делает и зачем |
| ---: | --- |
| 1 | Описывает назначение блока; эта строка не выполняет расчётов. |
| 2 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 3 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 4 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 6 | Вычисляет/сохраняет REGISTRY_PATH для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 7 | Вычисляет/сохраняет STATUSES для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 8 | Продолжает выражение блока «уровень модуля»: подготовка/проверка по явным условиям без обучения. |
| 11 | Создаёт обратимый ключ одной станции и одной системы без коллизий имён. |
| 12 | Возвращает f'eia_{int(plant_id)}_{str(system_id).encode("utf-8").hex()}' — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 13–24

```python


def project_path(root, relative):
    root = Path(root).resolve()
    text = str(relative)
    path = Path(text)
    if path.is_absolute() or ':' in text or '\\' in text or '..' in path.parts:
        raise ValueError(f'Not a safe relative project path: {relative}')
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f'Path escapes project: {relative}')
    return resolved
```

| Строка | Что делает и зачем |
| ---: | --- |
| 15 | Проверяет, что путь остаётся в текущем проекте, включая разрешение symlink. |
| 16 | Вычисляет/сохраняет root для следующего шага блока. Проверяет, что путь остаётся в текущем проекте, включая разрешение symlink. |
| 17 | Вычисляет/сохраняет text для следующего шага блока. Проверяет, что путь остаётся в текущем проекте, включая разрешение symlink. |
| 18 | Вычисляет/сохраняет path для следующего шага блока. Проверяет, что путь остаётся в текущем проекте, включая разрешение symlink. |
| 19 | Выбирает ветку по явному условию if path.is_absolute() or ':' in text or '\\' in text or '..' in path.parts. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 20 | Останавливает текущую операцию с конкретной причиной: ValueError(f'Not a safe relative project path: {relative}'). Данные при этом не исправляются. |
| 21 | Вычисляет/сохраняет resolved для следующего шага блока. Проверяет, что путь остаётся в текущем проекте, включая разрешение symlink. |
| 22 | Выбирает ветку по явному условию if not resolved.is_relative_to(root). Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 23 | Останавливает текущую операцию с конкретной причиной: ValueError(f'Path escapes project: {relative}'). Данные при этом не исправляются. |
| 24 | Возвращает resolved — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 25–36

```python


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_registry(root, verify=True):
    root = Path(root).resolve()
    data = json.loads(project_path(root, REGISTRY_PATH).read_text(encoding='utf-8'))
    if data.get('schema_version') != 2:
        raise ValueError('Unsupported dataset registry version')
    seen = set()
```

| Строка | Что делает и зачем |
| ---: | --- |
| 27 | Вычисляет контрольную сумму исходного файла для проверки неизменности. |
| 28 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 31 | Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 32 | Вычисляет/сохраняет root для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 33 | Вычисляет/сохраняет data для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 34 | Выбирает ветку по явному условию if data.get('schema_version') != 2. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 35 | Останавливает текущую операцию с конкретной причиной: ValueError('Unsupported dataset registry version'). Данные при этом не исправляются. |
| 36 | Вычисляет/сохраняет seen для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |

### Строки 37–48

```python
    outputs = set()
    checked = {}
    for entry in data['datasets']:
        expected = dataset_id(entry['plant_id_eia'], entry['cooling_id_eia'])
        if entry['dataset_id'] != expected or expected in seen:
            raise ValueError('Dataset identity collision or mismatch')
        seen.add(expected)
        if entry['status'] not in STATUSES:
            raise ValueError('Unknown dataset status')
        for name in ['audit_path', 'future_results_path', 'future_artifacts_dir']:
            project_path(root, entry['artifacts'][name])
        result_destination = entry['artifacts']['future_results_path']
```

| Строка | Что делает и зачем |
| ---: | --- |
| 37 | Вычисляет/сохраняет outputs для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 38 | Вычисляет/сохраняет checked для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 39 | Проверяет/обрабатывает по одному элементу указанной коллекции: for entry in data['datasets']. Порядок временных рядов не перемешивается. |
| 40 | Вычисляет/сохраняет expected для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 41 | Выбирает ветку по явному условию if entry['dataset_id'] != expected or expected in seen. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 42 | Останавливает текущую операцию с конкретной причиной: ValueError('Dataset identity collision or mismatch'). Данные при этом не исправляются. |
| 43 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 44 | Выбирает ветку по явному условию if entry['status'] not in STATUSES. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 45 | Останавливает текущую операцию с конкретной причиной: ValueError('Unknown dataset status'). Данные при этом не исправляются. |
| 46 | Проверяет/обрабатывает по одному элементу указанной коллекции: for name in ['audit_path', 'future_results_path', 'future_artifacts_dir']. Порядок временных рядов не перемешивается. |
| 47 | Продолжает выражение блока «read_registry»: Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 48 | Вычисляет/сохраняет result_destination для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |

### Строки 49–60

```python
        if result_destination in outputs:
            raise ValueError('Two systems share a result destination')
        outputs.add(result_destination)
        if entry['model_status']=='not_trained' and entry['results_path'] is not None:
            raise ValueError('Untrained dataset cannot advertise a result')
        if entry['results_path'] is not None:
            project_path(root, entry['results_path'])
        source = entry['observations']
        selector = source['selector']
        if source['format'] not in {'csv', 'parquet'}:
            raise ValueError('Unsupported observation format')
        if (selector['plant_id_eia'], selector['cooling_id_eia']) != (entry['plant_id_eia'], entry['cooling_id_eia']):
```

| Строка | Что делает и зачем |
| ---: | --- |
| 49 | Выбирает ветку по явному условию if result_destination in outputs. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 50 | Останавливает текущую операцию с конкретной причиной: ValueError('Two systems share a result destination'). Данные при этом не исправляются. |
| 51 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 52 | Выбирает ветку по явному условию if entry['model_status']=='not_trained' and entry['results_path'] is not None. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 53 | Останавливает текущую операцию с конкретной причиной: ValueError('Untrained dataset cannot advertise a result'). Данные при этом не исправляются. |
| 54 | Выбирает ветку по явному условию if entry['results_path'] is not None. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 55 | Продолжает выражение блока «read_registry»: Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 56 | Вычисляет/сохраняет source для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 57 | Вычисляет/сохраняет selector для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 58 | Выбирает ветку по явному условию if source['format'] not in {'csv', 'parquet'}. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 59 | Останавливает текущую операцию с конкретной причиной: ValueError('Unsupported observation format'). Данные при этом не исправляются. |
| 60 | Выбирает ветку по явному условию if (selector['plant_id_eia'], selector['cooling_id_eia']) != (entry['plant_id_eia'], entry['cooling_id_eia']). Важно различать отсутствие данных, нерешённую проверку и готовый результат. |

### Строки 61–72

```python
            raise ValueError('Source selector identity mismatch')
        if (selector['year_min'], selector['year_max']) != (2010,2025):
            raise ValueError('Source selector changes fixed date boundaries')
        path = project_path(root, source['path'])
        if verify:
            if str(path) not in checked:
                checked[str(path)] = sha256(path)
            if checked[str(path)] != source['sha256']:
                raise ValueError(f'Input hash mismatch: {source["path"]}')
    return data


```

| Строка | Что делает и зачем |
| ---: | --- |
| 61 | Останавливает текущую операцию с конкретной причиной: ValueError('Source selector identity mismatch'). Данные при этом не исправляются. |
| 62 | Выбирает ветку по явному условию if (selector['year_min'], selector['year_max']) != (2010,2025). Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 63 | Останавливает текущую операцию с конкретной причиной: ValueError('Source selector changes fixed date boundaries'). Данные при этом не исправляются. |
| 64 | Вычисляет/сохраняет path для следующего шага блока. Читает только JSON-метаданные и проверяет идентичность/пути; не импортирует ML. |
| 65 | Выбирает ветку по явному условию if verify. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 66 | Выбирает ветку по явному условию if str(path) not in checked. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 67 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 68 | Выбирает ветку по явному условию if checked[str(path)] != source['sha256']. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 69 | Останавливает текущую операцию с конкретной причиной: ValueError(f'Input hash mismatch: {source["path"]}'). Данные при этом не исправляются. |
| 70 | Возвращает data — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 73–77

```python
def find_dataset(root, identifier):
    matches = [e for e in read_registry(root)['datasets'] if e['dataset_id'] == identifier]
    if len(matches) != 1:
        raise ValueError(f'Unknown dataset_id: {identifier}')
    return matches[0]
```

| Строка | Что делает и зачем |
| ---: | --- |
| 73 | Выбирает единственную запись по точному dataset_id. |
| 74 | Вычисляет/сохраняет matches для следующего шага блока. Выбирает единственную запись по точному dataset_id. |
| 75 | Выбирает ветку по явному условию if len(matches) != 1. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 76 | Останавливает текущую операцию с конкретной причиной: ValueError(f'Unknown dataset_id: {identifier}'). Данные при этом не исправляются. |
| 77 | Возвращает matches[0] — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

## src/model/datasets.py

### Строки 1–12

```python
"""Prepare and validate single-system datasets from frozen local inputs; never fit."""
from pathlib import Path
import json
import re

import numpy as np
import pandas as pd

from .registry import REGISTRY_PATH, dataset_id, project_path, sha256

DEFAULT_INBOX = 'data/incoming/collected-20261114-150548'
METHODS = {'Measured continuously with a thermometer',
```

| Строка | Что делает и зачем |
| ---: | --- |
| 1 | Описывает назначение блока; эта строка не выполняет расчётов. |
| 2 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 3 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 4 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 6 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 7 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 9 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 11 | Вычисляет/сохраняет DEFAULT_INBOX для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 12 | Вычисляет/сохраняет METHODS для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |

### Строки 13–24

```python
           'Measured at intervals (for example, daily) with a thermometer'}
TABLE = '_core_eia923__monthly_cooling_system_information'
BASE_URL = 'https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/'
F_IN = 'monthly_average_intake_temperature_fahrenheit'
F_OUT = 'monthly_average_discharge_temperature_fahrenheit'
VALUE_FIELDS = ['intake_temperature_f', 'discharge_temperature_f',
                'intake_temperature_c', 'discharge_temperature_c', 'delta_t_c']


def require(condition, message):
    if not condition:
        raise ValueError(message)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 13 | Продолжает выражение блока «уровень модуля»: подготовка/проверка по явным условиям без обучения. |
| 14 | Вычисляет/сохраняет TABLE для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 15 | Вычисляет/сохраняет BASE_URL для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 16 | Вычисляет/сохраняет F_IN для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 17 | Вычисляет/сохраняет F_OUT для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 18 | Вычисляет/сохраняет VALUE_FIELDS для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 19 | Продолжает выражение блока «уровень модуля»: подготовка/проверка по явным условиям без обучения. |
| 22 | Останавливает обработку при противоречии вместо исправления данных молча. |
| 23 | Выбирает ветку по явному условию if not condition. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 24 | Останавливает текущую операцию с конкретной причиной: ValueError(message). Данные при этом не исправляются. |

### Строки 25–36

```python


def parse_flag(series):
    normalized = series.astype(str).str.strip().str.lower()
    require(normalized.isin(['true', 'false']).all(), f'Invalid boolean in {series.name}')
    return normalized.eq('true')


def assign_split(year):
    return np.where(year <= 2021, 'train', np.where(year <= 2023, 'validation', 'test'))


```

| Строка | Что делает и зачем |
| ---: | --- |
| 27 | Разбирает только явные true/false, чтобы строка False не стала истиной. |
| 28 | Вычисляет/сохраняет normalized для следующего шага блока. Разбирает только явные true/false, чтобы строка False не стала истиной. |
| 29 | Проверяет обязательное условие: Invalid boolean in {series.name}; при нарушении вызывает ValueError. |
| 30 | Возвращает normalized.eq('true') — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |
| 33 | Назначает неизменные временные части по году без случайного перемешивания. |
| 34 | Возвращает np.where(year <= 2021, 'train', np.where(year <= 2023, 'validation', 'test')) — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 37–48

```python
def from_raw(rows, plant_name):
    frame = rows[['report_month', 'plant_id_eia', 'cooling_id_eia']].copy()
    frame['plant_name'] = plant_name
    frame['intake_temperature_f'] = pd.to_numeric(rows[F_IN], errors='raise').to_numpy(dtype=float, na_value=np.nan)
    frame['discharge_temperature_f'] = pd.to_numeric(rows[F_OUT], errors='raise').to_numpy(dtype=float, na_value=np.nan)
    for point in ['intake', 'discharge']:
        frame[f'{point}_temperature_c'] = (frame[f'{point}_temperature_f'] - 32) * 5 / 9
    frame['delta_t_c'] = (frame.discharge_temperature_f - frame.intake_temperature_f) * 5 / 9
    frame['temperature_method'] = rows.temperature_method.fillna('').astype(str).str.strip()
    frame['pair_available'] = np.isfinite(frame[VALUE_FIELDS].to_numpy(dtype=float, na_value=np.nan)).all(axis=1)
    frame['eligible_measured'] = frame.pair_available & frame.temperature_method.isin(METHODS)
    frame['temperature_value_class'] = np.where(frame.temperature_method.isin(METHODS), 'measured',
```

| Строка | Что делает и зачем |
| ---: | --- |
| 37 | Приводит одну исходную систему Parquet к общим полям в памяти без экспорта копий CSV. |
| 38 | Вычисляет/сохраняет frame для следующего шага блока. Приводит одну исходную систему Parquet к общим полям в памяти без экспорта копий CSV. |
| 39 | Формирует или проверяет указанное поле канонической таблицы в памяти. Существующий исходный файл не меняется. |
| 40 | Явно переводит числовые значения в массив float, сохраняя пропуски как NaN; пропуск не должен ошибочно пройти проверку конечности. |
| 41 | Явно переводит числовые значения в массив float, сохраняя пропуски как NaN; пропуск не должен ошибочно пройти проверку конечности. |
| 42 | Проверяет/обрабатывает по одному элементу указанной коллекции: for point in ['intake', 'discharge']. Порядок временных рядов не перемешивается. |
| 43 | Выполняет документированную конверсию °F→°C либо разности °F→разность °C до округления; исходные значения не переписываются. |
| 44 | Выполняет документированную конверсию °F→°C либо разности °F→разность °C до округления; исходные значения не переписываются. |
| 45 | Создаёт/сверяет поле таблицы: отчётный метод измерения, отдельно от расхода. Существующий исходный файл не меняется. |
| 46 | Явно переводит числовые значения в массив float, сохраняя пропуски как NaN; пропуск не должен ошибочно пройти проверку конечности. |
| 47 | Создаёт/сверяет поле таблицы: производный флаг подтверждённого метода и полной пары. Существующий исходный файл не меняется. |
| 48 | Формирует или проверяет указанное поле канонической таблицы в памяти. Существующий исходный файл не меняется. |

### Строки 49–60

```python
        np.where(frame.temperature_method.str.contains('calculated|Estimated|Permitted', regex=True),
                 'estimated_or_calculated', 'unknown'))
    frame['split'] = assign_split(pd.to_datetime(frame.report_month).dt.year)
    frame['source_table'] = TABLE
    return frame


def validate_frame(frame, plant_id, system_id):
    frame = frame.copy()
    required = {'report_month', 'plant_id_eia', 'cooling_id_eia', 'temperature_method',
                'pair_available', 'eligible_measured', 'split', *VALUE_FIELDS}
    require(required.issubset(frame.columns), 'Missing observation columns')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 49 | Вычисляет/сохраняет np.where(frame.temperature_method.str.contains('calculated\|Estimated\|Permitted', regex для следующего шага блока. Приводит одну исходную систему Parquet к общим полям в памяти без экспорта копий CSV. |
| 50 | Продолжает выражение блока «from_raw»: Приводит одну исходную систему Parquet к общим полям в памяти без экспорта копий CSV. |
| 51 | Создаёт/сверяет поле таблицы: часть по фиксированному году. Существующий исходный файл не меняется. |
| 52 | Формирует или проверяет указанное поле канонической таблицы в памяти. Существующий исходный файл не меняется. |
| 53 | Возвращает frame — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |
| 56 | Проверяет идентичность, месяцы, единицы, арифметику, флаги и временные части. |
| 57 | Вычисляет/сохраняет frame для следующего шага блока. Проверяет идентичность, месяцы, единицы, арифметику, флаги и временные части. |
| 58 | Вычисляет/сохраняет required для следующего шага блока. Проверяет идентичность, месяцы, единицы, арифметику, флаги и временные части. |
| 59 | Продолжает выражение блока «validate_frame»: Проверяет идентичность, месяцы, единицы, арифметику, флаги и временные части. |
| 60 | Проверяет обязательное условие: Missing observation columns; при нарушении вызывает ValueError. |

### Строки 61–72

```python
    require(not frame.empty, 'No observation rows')
    require(frame.report_month.astype(str).str.fullmatch(r'\d{4}-\d{2}').all(), 'Invalid month format')
    frame['date'] = pd.to_datetime(frame.report_month, format='%Y-%m', errors='raise')
    require(frame.date.between('2010-01-01', '2025-12-01').all(), 'Date outside fixed protocol')
    require(frame.plant_id_eia.eq(plant_id).all() and frame.cooling_id_eia.eq(system_id).all(), 'Identity mismatch')
    require(not frame.report_month.duplicated().any(), 'Duplicate system month')
    frame[VALUE_FIELDS] = frame[VALUE_FIELDS].apply(pd.to_numeric, errors='raise')
    for flag in ['pair_available', 'eligible_measured']:
        frame[flag] = parse_flag(frame[flag])
    pair = np.isfinite(frame[VALUE_FIELDS].to_numpy(dtype=float, na_value=np.nan)).all(axis=1)
    methods = frame.temperature_method.fillna('').astype(str).str.strip()
    require(frame.pair_available.eq(pair).all(), 'Pair flag mismatch')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 61 | Проверяет обязательное условие: No observation rows; при нарушении вызывает ValueError. |
| 62 | Проверяет обязательное условие: Invalid month format; при нарушении вызывает ValueError. |
| 63 | Создаёт/сверяет поле таблицы: дата для сортировки и временного разделения. Существующий исходный файл не меняется. |
| 64 | Проверяет обязательное условие: Date outside fixed protocol; при нарушении вызывает ValueError. |
| 65 | Проверяет обязательное условие: Identity mismatch; при нарушении вызывает ValueError. |
| 66 | Проверяет обязательное условие: Duplicate system month; при нарушении вызывает ValueError. |
| 67 | Формирует или проверяет указанное поле канонической таблицы в памяти. Существующий исходный файл не меняется. |
| 68 | Проверяет/обрабатывает по одному элементу указанной коллекции: for flag in ['pair_available', 'eligible_measured']. Порядок временных рядов не перемешивается. |
| 69 | Формирует или проверяет указанное поле канонической таблицы в памяти. Существующий исходный файл не меняется. |
| 70 | Явно переводит числовые значения в массив float, сохраняя пропуски как NaN; пропуск не должен ошибочно пройти проверку конечности. |
| 71 | Вычисляет/сохраняет methods для следующего шага блока. Проверяет идентичность, месяцы, единицы, арифметику, флаги и временные части. |
| 72 | Проверяет обязательное условие: Pair flag mismatch; при нарушении вызывает ValueError. |

### Строки 73–84

```python
    require(frame.eligible_measured.eq(pair & methods.isin(METHODS)).all(), 'Measured eligibility mismatch')
    for point in ['intake', 'discharge']:
        require(np.allclose(frame[f'{point}_temperature_c'], (frame[f'{point}_temperature_f']-32)*5/9,
                            atol=1.1e-6, rtol=0, equal_nan=True), 'Celsius conversion mismatch')
    require(np.allclose(frame.delta_t_c, (frame.discharge_temperature_f-frame.intake_temperature_f)*5/9,
                        atol=1.1e-6, rtol=0, equal_nan=True), 'Delta arithmetic mismatch')
    require(frame.split.eq(assign_split(frame.date.dt.year)).all(), 'Fixed split mismatch')
    if 'source_table' in frame:
        require(frame.source_table.eq(TABLE).all(), 'Source table mismatch')
    return frame.sort_values('date').reset_index(drop=True)


```

| Строка | Что делает и зачем |
| ---: | --- |
| 73 | Проверяет обязательное условие: Measured eligibility mismatch; при нарушении вызывает ValueError. |
| 74 | Проверяет/обрабатывает по одному элементу указанной коллекции: for point in ['intake', 'discharge']. Порядок временных рядов не перемешивается. |
| 75 | Проверяет обязательное условие: {point}_temperature_f; при нарушении вызывает ValueError. |
| 76 | Сравнивает числовые представления с указанным допуском округления °C; rtol=0 исключает скрытое увеличение допуска на больших числах. |
| 77 | Проверяет обязательное условие согласованности текущих данных; при нарушении вызывает ValueError. |
| 78 | Сравнивает числовые представления с указанным допуском округления °C; rtol=0 исключает скрытое увеличение допуска на больших числах. |
| 79 | Проверяет обязательное условие: Fixed split mismatch; при нарушении вызывает ValueError. |
| 80 | Выбирает ветку по явному условию if 'source_table' in frame. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 81 | Проверяет обязательное условие: Source table mismatch; при нарушении вызывает ValueError. |
| 82 | Возвращает frame.sort_values('date').reset_index(drop=True) — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 85–96

```python
def validate_csv(path, raw_frame, plant_id, system_id):
    frame = validate_frame(pd.read_csv(path), plant_id, system_id)
    expected = validate_frame(raw_frame, plant_id, system_id)
    require(frame.report_month.tolist() == expected.report_month.tolist(), 'CSV/raw months disagree')
    require(frame.plant_name.eq(expected.plant_name).all(), 'CSV station name mismatch')
    for field in VALUE_FIELDS:
        require(np.allclose(frame[field], expected[field], rtol=0, atol=1.1e-6, equal_nan=True), 'CSV/raw values disagree')
    actual_method = frame.temperature_method.fillna('').astype(str).str.strip()
    require(actual_method.eq(expected.temperature_method).all(), 'CSV/raw method mismatch')
    return frame


```

| Строка | Что делает и зачем |
| ---: | --- |
| 85 | Сопоставляет оригинальный CSV с теми же месяцами и значениями первичного Parquet. |
| 86 | Читает существующий оригинальный CSV; новая конкурирующая копия наблюдений не создаётся. |
| 87 | Вычисляет/сохраняет expected для следующего шага блока. Сопоставляет оригинальный CSV с теми же месяцами и значениями первичного Parquet. |
| 88 | Проверяет обязательное условие: CSV/raw months disagree; при нарушении вызывает ValueError. |
| 89 | Проверяет обязательное условие: CSV station name mismatch; при нарушении вызывает ValueError. |
| 90 | Проверяет/обрабатывает по одному элементу указанной коллекции: for field in VALUE_FIELDS. Порядок временных рядов не перемешивается. |
| 91 | Проверяет обязательное условие: CSV/raw values disagree; при нарушении вызывает ValueError. |
| 92 | Вычисляет/сохраняет actual_method для следующего шага блока. Сопоставляет оригинальный CSV с теми же месяцами и значениями первичного Parquet. |
| 93 | Проверяет обязательное условие: CSV/raw method mismatch; при нарушении вызывает ValueError. |
| 94 | Возвращает frame — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 97–108

```python
def review_flags(frame):
    measured = frame.eligible_measured
    flags = pd.DataFrame({
        'nonpositive_delta': measured & frame.delta_t_c.le(0),
        'temperature_range_review': measured & (~frame.intake_temperature_c.between(-5, 100)
                                                | ~frame.discharge_temperature_c.between(-5, 100)),
    }, index=frame.index)
    return {str(frame.loc[index, 'report_month']): flags.columns[row].tolist()
            for index, row in flags.iterrows() if row.any()}


def classify(frame, cooling_types, plant_id):
```

| Строка | Что делает и зачем |
| ---: | --- |
| 97 | Отмечает подозрительные measured-строки, сохраняя их в таблице и не меняя eligibility. |
| 98 | Вычисляет/сохраняет measured для следующего шага блока. Отмечает подозрительные measured-строки, сохраняя их в таблице и не меняя eligibility. |
| 99 | Вычисляет/сохраняет flags для следующего шага блока. Отмечает подозрительные measured-строки, сохраняя их в таблице и не меняя eligibility. |
| 100 | Продолжает выражение блока «review_flags»: Отмечает подозрительные measured-строки, сохраняя их в таблице и не меняя eligibility. |
| 101 | Продолжает выражение блока «review_flags»: Отмечает подозрительные measured-строки, сохраняя их в таблице и не меняя eligibility. |
| 102 | Продолжает выражение блока «review_flags»: Отмечает подозрительные measured-строки, сохраняя их в таблице и не меняя eligibility. |
| 103 | Закрывает начатый блок/словарь/вызов; самостоятельных изменений данных не делает. |
| 104 | Возвращает {str(frame.loc[index, 'report_month']): flags.columns[row].tolist() — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |
| 105 | Проверяет/обрабатывает по одному элементу указанной коллекции: for index, row in flags.iterrows() if row.any()}. Порядок временных рядов не перемешивается. |
| 108 | Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |

### Строки 109–120

```python
    eligible = frame.loc[frame.eligible_measured]
    counts = {name: int(eligible.split.eq(name).sum()) for name in ['train', 'validation', 'test']}
    reviews = review_flags(frame)
    calendar = sorted(eligible.loc[eligible.split.eq('train'), 'date'].dt.month.unique().tolist())
    screened = frame.eligible_measured & frame.delta_t_c.gt(0) & frame.intake_temperature_c.between(-5,100) & frame.discharge_temperature_c.between(-5,100) & (plant_id != 628)
    screen_counts = {name: int((screened & frame.split.eq(name)).sum()) for name in counts}
    screen_calendar = frame.loc[screened & frame.split.eq('train'), 'date'].dt.month.nunique()
    compatible = bool(cooling_types) and not (set(cooling_types)-{'O','ON','OC'})
    provisional = all(screen_counts.values()) and screen_calendar == 12 and compatible
    limitations = []
    if plant_id == 628:
        status = 'blocked'; limitations.append('mixed_site_nuclear_attribution_unconfirmed')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 109 | Вычисляет/сохраняет eligible для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 110 | Вычисляет/сохраняет counts для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 111 | Вычисляет/сохраняет reviews для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 112 | Вычисляет/сохраняет calendar для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 113 | Вычисляет/сохраняет screened для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 114 | Вычисляет/сохраняет screen_counts для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 115 | Вычисляет/сохраняет screen_calendar для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 116 | Вычисляет/сохраняет compatible для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 117 | Вычисляет/сохраняет provisional для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 118 | Вычисляет/сохраняет limitations для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 119 | Выбирает ветку по явному условию if plant_id == 628. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 120 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |

### Строки 121–132

```python
    elif not frame.pair_available.any():
        status = 'reference_only'; limitations.append('no_complete_pairs')
    elif eligible.empty:
        status = 'blocked'; limitations.append('no_explicit_measured_pairs')
    elif reviews:
        status = 'review_required'; limitations.append('suspect_measured_rows_retained_no_automatic_exclusion')
    elif not compatible:
        status = 'measurements_only'; limitations.append('cooling_scheme_semantics_require_review')
    elif not all(counts.values()) or len(calendar) != 12:
        status = 'measurements_only'; limitations.append('fixed_time_coverage_insufficient')
    else:
        status = 'ready_for_model_check'
```

| Строка | Что делает и зачем |
| ---: | --- |
| 121 | Выбирает ветку по явному условию elif not frame.pair_available.any(). Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 122 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 123 | Выбирает ветку по явному условию elif eligible.empty. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 124 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 125 | Выбирает ветку по явному условию elif reviews. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 126 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 127 | Выбирает ветку по явному условию elif not compatible. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 128 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 129 | Выбирает ветку по явному условию elif not all(counts.values()) or len(calendar) != 12. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 130 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 131 | Обрабатывает оставшийся случай той же проверки, не меняя условия предыдущих веток. |
| 132 | Вычисляет/сохраняет status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |

### Строки 133–144

```python
    if not compatible:
        limitations.append('recirculating_mixed_or_unknown_cooling_codes')
    if frame.intake_temperature_c.isna().any() or frame.discharge_temperature_c.isna().any():
        limitations.append('missing_temperatures_retained_and_ineligible')
    limitations.extend(['reported_measurement_not_independent_sensor_validation',
                        'historical_monthly_retrospective_only_no_ecosystem_inference',
                        'historical_cooling_metadata_incomplete_or_changed'])
    inventory_status = 'model_check_candidate' if provisional else (
        'verified_reported_measurements' if screened.any() else 'blocked' if frame.pair_available.any() else 'reference_only')
    return status, inventory_status, counts, reviews, limitations


```

| Строка | Что делает и зачем |
| ---: | --- |
| 133 | Выбирает ветку по явному условию if not compatible. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 134 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 135 | Выбирает ветку по явному условию if frame.intake_temperature_c.isna().any() or frame.discharge_temperature_c.isna().any(). Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 136 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 137 | Продолжает выражение блока «classify»: Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 138 | Продолжает выражение блока «classify»: Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 139 | Продолжает выражение блока «classify»: Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 140 | Вычисляет/сохраняет inventory_status для следующего шага блока. Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 141 | Продолжает выражение блока «classify»: Разделяет готовность данных и наличие модели, не выдаёт предварительный скрининг за очистку. |
| 142 | Возвращает status, inventory_status, counts, reviews, limitations — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 145–156

```python
def write_same_or_new(root, relative, value):
    target = project_path(root, relative)
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')
    if target.exists():
        require(target.read_bytes() == payload, f'Prepared artifact differs; refusing overwrite: {relative}')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(payload)


def inventory_evidence(root, inbox):
```

| Строка | Что делает и зачем |
| ---: | --- |
| 145 | Пишет детерминированный новый JSON либо подтверждает точное совпадение существующего. |
| 146 | Вычисляет/сохраняет target для следующего шага блока. Пишет детерминированный новый JSON либо подтверждает точное совпадение существующего. |
| 147 | Создаёт стабильное JSON-представление; сортировка ключей и запрет NaN нужны для повторяемых байтов и строгого чтения. |
| 148 | Выбирает ветку по явному условию if target.exists(). Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 149 | Проверяет обязательное условие: Prepared artifact differs; refusing overwrite: {relative}; при нарушении вызывает ValueError. |
| 150 | Заканчивает функцию: существующий JSON уже совпал, поэтому запись не нужна. |
| 151 | Вычисляет/сохраняет target.parent.mkdir(parents для следующего шага блока. Пишет детерминированный новый JSON либо подтверждает точное совпадение существующего. |
| 152 | Ограничивает ресурс контекстом; тестовые изменения идут во временный каталог, а новые артефакты создаются без перезаписи. |
| 153 | Сравнивает/записывает точные байты; отличающийся уже существующий артефакт не должен быть затёрт. |
| 156 | Читает фактический INVENTORY и сверяет все зафиксированные хеши входов. |

### Строки 157–168

```python
    inventory = project_path(root, inbox + '/INVENTORY.md')
    text = inventory.read_text(encoding='utf-8')
    hashes = dict(re.findall(r'\| `([^`]+)` \| `([0-9a-f]{64})` \|', text))
    for absolute, digest in hashes.items():
        path = Path(absolute)
        require(path.resolve().is_relative_to(Path(root).resolve()), 'Inventory path outside project')
        require(sha256(path) == digest, f'Inventory input hash mismatch: {path}')
    return inventory, hashes, text


def prepare_registry(root, inbox=DEFAULT_INBOX):
    root = Path(root).resolve()
```

| Строка | Что делает и зачем |
| ---: | --- |
| 157 | Вычисляет/сохраняет inventory для следующего шага блока. Читает фактический INVENTORY и сверяет все зафиксированные хеши входов. |
| 158 | Вычисляет/сохраняет text для следующего шага блока. Читает фактический INVENTORY и сверяет все зафиксированные хеши входов. |
| 159 | Вычисляет/сохраняет hashes для следующего шага блока. Читает фактический INVENTORY и сверяет все зафиксированные хеши входов. |
| 160 | Проверяет/обрабатывает по одному элементу указанной коллекции: for absolute, digest in hashes.items(). Порядок временных рядов не перемешивается. |
| 161 | Вычисляет/сохраняет path для следующего шага блока. Читает фактический INVENTORY и сверяет все зафиксированные хеши входов. |
| 162 | Проверяет обязательное условие: Inventory path outside project; при нарушении вызывает ValueError. |
| 163 | Проверяет обязательное условие: Inventory input hash mismatch: {path}; при нарушении вызывает ValueError. |
| 164 | Возвращает inventory, hashes, text — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |
| 167 | Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 168 | Вычисляет/сохраняет root для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |

### Строки 169–180

```python
    inventory, hashes, text = inventory_evidence(root, inbox)
    raw_path = project_path(root, inbox + '/raw/cooling.parquet')
    entity_path = project_path(root, inbox + '/raw/entity_plants.parquet')
    generation_path = project_path(root, inbox + '/raw/nuclear_generation.parquet')
    for path in [raw_path, entity_path, generation_path]:
        require(str(path) in hashes, 'Raw input not anchored in inventory')
    raw = pd.read_parquet(raw_path)
    raw['report_month'] = pd.to_datetime(raw.report_date).dt.strftime('%Y-%m')
    raw = raw.loc[pd.to_datetime(raw.report_date).dt.year.between(2010, 2025)].copy()
    entities = pd.read_parquet(entity_path).set_index('plant_id_eia')
    nuclear_ids = set(pd.read_parquet(generation_path).plant_id_eia.astype(int))
    require(len(nuclear_ids) == 66, 'Source membership changed; review inventory')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 169 | Вычисляет/сохраняет inventory, hashes, text для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 170 | Вычисляет/сохраняет raw_path для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 171 | Вычисляет/сохраняет entity_path для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 172 | Вычисляет/сохраняет generation_path для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 173 | Проверяет/обрабатывает по одному элементу указанной коллекции: for path in [raw_path, entity_path, generation_path]. Порядок временных рядов не перемешивается. |
| 174 | Проверяет обязательное условие: Raw input not anchored in inventory; при нарушении вызывает ValueError. |
| 175 | Читает локальный зафиксированный Parquet; сетевых запросов и обучения здесь нет. |
| 176 | Вычисляет/сохраняет raw['report_month'] для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 177 | Вычисляет/сохраняет raw для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 178 | Читает локальный зафиксированный Parquet; сетевых запросов и обучения здесь нет. |
| 179 | Читает локальный зафиксированный Parquet; сетевых запросов и обучения здесь нет. |
| 180 | Проверяет обязательное условие: Source membership changed; review inventory; при нарушении вызывает ValueError. |

### Строки 181–192

```python
    originals = {}
    csv_paths = [root/'data/surry_cw1_monthly.csv', *project_path(root, inbox+'/station_csv').glob('*.csv')]
    for path in csv_paths:
        require(str(path) in hashes, f'CSV not anchored in inventory: {path}')
        header = pd.read_csv(path, usecols=['plant_id_eia','cooling_id_eia'])
        identities = header.drop_duplicates()
        require(len(identities) == 1, 'Original CSV mixes identities')
        key = (int(identities.iloc[0].plant_id_eia), str(identities.iloc[0].cooling_id_eia))
        require(key not in originals, f'Competing originals for {key}')
        originals[key] = path
    entries = []
    audit_jobs = []
```

| Строка | Что делает и зачем |
| ---: | --- |
| 181 | Вычисляет/сохраняет originals для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 182 | Вычисляет/сохраняет csv_paths для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 183 | Проверяет/обрабатывает по одному элементу указанной коллекции: for path in csv_paths. Порядок временных рядов не перемешивается. |
| 184 | Проверяет обязательное условие: CSV not anchored in inventory: {path}; при нарушении вызывает ValueError. |
| 185 | Читает существующий оригинальный CSV; новая конкурирующая копия наблюдений не создаётся. |
| 186 | Вычисляет/сохраняет identities для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 187 | Проверяет обязательное условие: Original CSV mixes identities; при нарушении вызывает ValueError. |
| 188 | Вычисляет/сохраняет key для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 189 | Проверяет обязательное условие: Competing originals for {key}; при нарушении вызывает ValueError. |
| 190 | Вычисляет/сохраняет originals[key] для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 191 | Вычисляет/сохраняет entries для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 192 | Вычисляет/сохраняет audit_jobs для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |

### Строки 193–204

```python
    raw_subset = raw.loc[raw.plant_id_eia.isin(nuclear_ids)]
    require(not raw_subset.cooling_id_eia.isna().any(), 'Missing system ID requires review')
    for (plant_id, system), rows in raw_subset.groupby(['plant_id_eia','cooling_id_eia'], sort=True):
        plant_id = int(plant_id); system = str(system)
        identifier = dataset_id(plant_id, system)
        name = str(entities.loc[plant_id, 'plant_name_eia'])
        frame = validate_frame(from_raw(rows, name), plant_id, system)
        original = originals.get((plant_id, system))
        if original:
            frame = validate_csv(original, frame, plant_id, system)
        types = sorted(rows.cooling_type.dropna().astype(str).str.strip().unique().tolist())
        status, previous, counts, reviews, limits = classify(frame, types, plant_id)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 193 | Вычисляет/сохраняет raw_subset для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 194 | Проверяет обязательное условие: Missing system ID requires review; при нарушении вызывает ValueError. |
| 195 | Проверяет/обрабатывает по одному элементу указанной коллекции: for (plant_id, system), rows in raw_subset.groupby(['plant_id_eia','cooling_id_eia'], sort=True). Порядок временных рядов не перемешивается. |
| 196 | Вычисляет/сохраняет plant_id для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 197 | Вычисляет/сохраняет identifier для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 198 | Вычисляет/сохраняет name для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 199 | Вычисляет/сохраняет frame для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 200 | Вычисляет/сохраняет original для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 201 | Выбирает ветку по явному условию if original. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 202 | Вычисляет/сохраняет frame для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 203 | Вычисляет/сохраняет types для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 204 | Вычисляет/сохраняет status, previous, counts, reviews, limits для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |

### Строки 205–216

```python
        directory = f'data/model_artifacts/multistation/datasets/{identifier}'
        legacy = plant_id == 3806 and system == 'CW1'
        source_path = original or raw_path
        relative = source_path.relative_to(root).as_posix()
        entry = {'dataset_id': identifier, 'plant_id_eia': plant_id, 'plant_name': name, 'cooling_id_eia': system,
            'observations': {'format': 'csv' if original else 'parquet', 'path': relative, 'sha256': sha256(source_path),
                             'selector': {'plant_id_eia': plant_id, 'cooling_id_eia': system, 'year_min': 2010, 'year_max': 2025}},
            'provenance': {'table': TABLE, 'source_url': BASE_URL+TABLE+'.parquet', 'source_units': 'degF', 'units': 'degC',
                           'raw_path': raw_path.relative_to(root).as_posix(), 'raw_sha256': sha256(raw_path),
                           'inventory_path': inventory.relative_to(root).as_posix(), 'inventory_sha256': sha256(inventory),
                           'license': 'CC-BY-4.0 (PUDL); public EIA data with acknowledgment'},
            'inventory_status': previous, 'status': status, 'limitations': limits,
```

| Строка | Что делает и зачем |
| ---: | --- |
| 205 | Вычисляет/сохраняет directory для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 206 | Вычисляет/сохраняет legacy для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 207 | Вычисляет/сохраняет source_path для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 208 | Вычисляет/сохраняет relative для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 209 | Заполняет метаданные: стабильный ключ площадки и системы, точный идентификатор площадки EIA, точный ID системы без склейки с другими ID. Это описание данных/будущего пути, а не готовая модель. |
| 210 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 211 | Заполняет метаданные: точный идентификатор площадки EIA, точный ID системы без склейки с другими ID, нижняя граница 2010, верхняя граница 2025. Это описание данных/будущего пути, а не готовая модель. |
| 212 | Заполняет метаданные: проверяемое происхождение, исходные °F по документации, производные °C. Это описание данных/будущего пути, а не готовая модель. |
| 213 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 214 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 215 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 216 | Заполняет метаданные: первоначальный статус импорта для сравнения, готовность данных, отдельно от готовности модели, причины и научные ограничения. Это описание данных/будущего пути, а не готовая модель. |

### Строки 217–228

```python
            'rows': len(frame), 'eligible_rows': int(frame.eligible_measured.sum()),
            'period': [frame.report_month.min(),frame.report_month.max()], 'split_counts': counts,
            'excluded_months': frame.loc[~frame.eligible_measured,'report_month'].tolist(),
            'review_months': reviews, 'cooling_types': types,
            'model_status': 'existing_verified' if legacy else 'not_trained',
            'results_path': 'data/results.csv' if legacy else None,
            'artifacts': {'audit_path': directory+'/audit.json',
                          'future_results_path': 'data/results.csv' if legacy else directory+'/results.csv',
                          'future_artifacts_dir': 'data/model_artifacts' if legacy else directory+'/model_artifacts'}}
        audit = {'dataset_id':identifier, 'split_counts':counts, 'status':status, 'review_months':reviews,
                 'excluded_months':entry['excluded_months'], 'methods': frame.temperature_method.fillna('MISSING').value_counts().to_dict(),
                 'missing': {k:int(v) for k,v in frame.isna().sum().items() if v},
```

| Строка | Что делает и зачем |
| ---: | --- |
| 217 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 218 | Заполняет метаданные: число подходящих месяцев в фиксированных train/validation/test. Это описание данных/будущего пути, а не готовая модель. |
| 219 | Заполняет метаданные: месяцы без подтверждённых measured-пар. Это описание данных/будущего пути, а не готовая модель. |
| 220 | Заполняет метаданные: сомнительные месяцы, не удалённые из исходника. Это описание данных/будущего пути, а не готовая модель. |
| 221 | Заполняет метаданные: состояние модели; not_trained не означает ошибку. Это описание данных/будущего пути, а не готовая модель. |
| 222 | Заполняет метаданные: только существующий результат; иначе null. Это описание данных/будущего пути, а не готовая модель. |
| 223 | Заполняет метаданные: отдельный JSON проверки данных. Это описание данных/будущего пути, а не готовая модель. |
| 224 | Заполняет метаданные: отдельный будущий выход этой системы. Это описание данных/будущего пути, а не готовая модель. |
| 225 | Заполняет метаданные: отдельное место будущих модельных артефактов. Это описание данных/будущего пути, а не готовая модель. |
| 226 | Заполняет метаданные: стабильный ключ площадки и системы, число подходящих месяцев в фиксированных train/validation/test, готовность данных, отдельно от готовности модели, сомнительные месяцы, не удалённые из исходника. Это описание данных/будущего пути, а не готовая модель. |
| 227 | Заполняет метаданные: месяцы без подтверждённых measured-пар. Это описание данных/будущего пути, а не готовая модель. |
| 228 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |

### Строки 229–240

```python
                 'missing_internal_months':pd.date_range(frame.date.min(),frame.date.max(),freq='MS').strftime('%Y-%m').difference(frame.report_month).tolist(),
                 'cooling_types':types, 'input_sha256':entry['observations']['sha256'],
                 'validation':'identity, source, units, arithmetic, strict flags, fixed splits; no fitting or imputation',
                 'limitations':limits}
        audit_jobs.append((entry['artifacts']['audit_path'],audit))
        entries.append(entry)
    require(len(entries)==102, 'System membership changed; review inventory')
    candidate_keys = set()
    section = text.split('## Подробная проверка систем')[1].split('### Методы')[0]
    for line in section.splitlines():
        if 'структурные проверки пройдены' in line:
            plant, system = line.split('|')[1].strip().split(' / ')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 229 | Вычисляет/сохраняет 'missing_internal_months':pd.date_range(frame.date.min(),frame.date.max(),freq для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 230 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 231 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 232 | Заполняет метаданные: причины и научные ограничения. Это описание данных/будущего пути, а не готовая модель. |
| 233 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 234 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 235 | Проверяет обязательное условие: System membership changed; review inventory; при нарушении вызывает ValueError. |
| 236 | Вычисляет/сохраняет candidate_keys для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 237 | Вычисляет/сохраняет section для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 238 | Проверяет/обрабатывает по одному элементу указанной коллекции: for line in section.splitlines(). Порядок временных рядов не перемешивается. |
| 239 | Выбирает ветку по явному условию if 'структурные проверки пройдены' in line. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 240 | Вычисляет/сохраняет plant, system для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |

### Строки 241–252

```python
            candidate_keys.add(dataset_id(int(plant),system))
    actual_candidates = {e['dataset_id'] for e in entries if e['inventory_status']=='model_check_candidate'}
    require(candidate_keys == actual_candidates, 'Provisional candidates differ from inventory')
    legacy_entry = next(e for e in entries if e['plant_id_eia']==3806 and e['cooling_id_eia']=='CW1')
    verify_legacy_result(root, legacy_entry)
    registry = {'schema_version':2, 'contract':'DATA_CONTRACT v2; v1 Surry preserved',
                'source_inventory':inventory.relative_to(root).as_posix(), 'datasets':entries}
    for relative, value in audit_jobs:
        write_same_or_new(root,relative,value)
    write_same_or_new(root, REGISTRY_PATH,registry)
    return registry

```

| Строка | Что делает и зачем |
| ---: | --- |
| 241 | Добавляет проверенную запись/причину в текущую коллекцию, сохраняя отдельность систем. |
| 242 | Вычисляет/сохраняет actual_candidates для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 243 | Проверяет обязательное условие: Provisional candidates differ from inventory; при нарушении вызывает ValueError. |
| 244 | Вычисляет/сохраняет legacy_entry для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 245 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 246 | Вычисляет/сохраняет registry для следующего шага блока. Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 247 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 248 | Проверяет/обрабатывает по одному элементу указанной коллекции: for relative, value in audit_jobs. Порядок временных рядов не перемешивается. |
| 249 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 250 | Продолжает выражение блока «prepare_registry»: Последовательно проверяет все системы и формирует реестр/аудиты, без вызовов обучения. |
| 251 | Возвращает registry — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 253–264

```python

def verify_legacy_result(root, entry):
    frame = pd.read_csv(project_path(root,entry['observations']['path']))
    frame = validate_frame(frame,3806,'CW1')
    test = frame.loc[frame.eligible_measured & frame.split.eq('test')].set_index('report_month')
    train = frame.loc[frame.eligible_measured & frame.split.eq('train')]
    result = pd.read_csv(project_path(root,'data/results.csv'))
    fields = ['report_month','intake_temperature_c','reported_delta_t_c','median_baseline_delta_t_c',
              'seasonal_baseline_delta_t_c','model_delta_t_c']
    require(result.columns.tolist()==fields and result.report_month.is_unique,'Legacy result schema mismatch')
    require(result.report_month.tolist()==test.index.tolist(),'Legacy test months mismatch')
    require(np.isfinite(result.iloc[:,1:]).all().all(),'Legacy nonfinite result')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 254 | Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 255 | Читает существующий оригинальный CSV; новая конкурирующая копия наблюдений не создаётся. |
| 256 | Вычисляет/сохраняет frame для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 257 | Вычисляет/сохраняет test для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 258 | Вычисляет/сохраняет train для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 259 | Читает существующий оригинальный CSV; новая конкурирующая копия наблюдений не создаётся. |
| 260 | Вычисляет/сохраняет fields для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 261 | Продолжает выражение блока «verify_legacy_result»: Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 262 | Проверяет обязательное условие: Legacy result schema mismatch; при нарушении вызывает ValueError. |
| 263 | Проверяет обязательное условие: Legacy test months mismatch; при нарушении вызывает ValueError. |
| 264 | Проверяет обязательное условие: Legacy nonfinite result; при нарушении вызывает ValueError. |

### Строки 265–276

```python
    require(np.allclose(result.reported_delta_t_c,test.delta_t_c,rtol=0,atol=1e-9),'Legacy target mismatch')
    require(np.allclose(result.intake_temperature_c,test.intake_temperature_c,rtol=0,atol=1e-9),'Legacy inlet mismatch')
    median=train.delta_t_c.median()
    seasonal=train.groupby(train.date.dt.month).delta_t_c.median()
    require(np.allclose(result.median_baseline_delta_t_c,median,rtol=0,atol=5.1e-7),'Legacy median mismatch')
    require(np.allclose(result.seasonal_baseline_delta_t_c,pd.to_datetime(result.report_month).dt.month.map(seasonal),rtol=0,atol=5.1e-7),'Legacy seasonal mismatch')
    metrics=json.loads(project_path(root,'data/model_artifacts/metrics.json').read_text())
    require(metrics['input_sha256']==entry['observations']['sha256'],'Legacy metrics/source mismatch')
    for field in fields[3:]:
        score=float(np.abs(result[field]-result.reported_delta_t_c).mean())
        require(abs(score-metrics['test_mae_c'][field])<1e-6,'Legacy metric mismatch')
    return {field:float(np.abs(result[field]-result.reported_delta_t_c).mean()) for field in fields[3:]}
```

| Строка | Что делает и зачем |
| ---: | --- |
| 265 | Проверяет обязательное условие: Legacy target mismatch; при нарушении вызывает ValueError. |
| 266 | Проверяет обязательное условие: Legacy inlet mismatch; при нарушении вызывает ValueError. |
| 267 | Вычисляет/сохраняет median для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 268 | Вычисляет/сохраняет seasonal для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 269 | Проверяет обязательное условие: Legacy median mismatch; при нарушении вызывает ValueError. |
| 270 | Проверяет обязательное условие: Legacy seasonal mismatch; при нарушении вызывает ValueError. |
| 271 | Вычисляет/сохраняет metrics для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 272 | Проверяет обязательное условие: Legacy metrics/source mismatch; при нарушении вызывает ValueError. |
| 273 | Проверяет/обрабатывает по одному элементу указанной коллекции: for field in fields[3:]. Порядок временных рядов не перемешивается. |
| 274 | Вычисляет/сохраняет score для следующего шага блока. Проверяет прежний Surry по сохранённому results.csv, исходнику и метрикам, без fit. |
| 275 | Проверяет обязательное условие: Legacy metric mismatch; при нарушении вызывает ValueError. |
| 276 | Возвращает {field:float(np.abs(result[field]-result.reported_delta_t_c).mean()) for field in fields[3:]} — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |

### Строки 277–288

```python


def load_observations(root, entry):
    source=entry['observations']
    path=project_path(root,source['path'])
    require(sha256(path)==source['sha256'],'Observation hash changed')
    raw_path=project_path(root,entry['provenance']['raw_path'])
    require(sha256(raw_path)==entry['provenance']['raw_sha256'],'Raw source hash changed')
    raw=pd.read_parquet(raw_path,
        filters=[('plant_id_eia','==',entry['plant_id_eia']),('cooling_id_eia','==',entry['cooling_id_eia'])],
        columns=['plant_id_eia','cooling_id_eia','report_date',F_IN,F_OUT,'temperature_method'])
    raw['report_month']=pd.to_datetime(raw.report_date).dt.strftime('%Y-%m')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 279 | Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 280 | Вычисляет/сохраняет source для следующего шага блока. Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 281 | Вычисляет/сохраняет path для следующего шага блока. Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 282 | Проверяет обязательное условие: Observation hash changed; при нарушении вызывает ValueError. |
| 283 | Вычисляет/сохраняет raw_path для следующего шага блока. Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 284 | Проверяет обязательное условие: Raw source hash changed; при нарушении вызывает ValueError. |
| 285 | Читает локальный зафиксированный Parquet; сетевых запросов и обучения здесь нет. |
| 286 | Передаёт Parquet точные plant/system-фильтры, чтобы загрузка одной системы не читала ненужные строки. |
| 287 | Оставляет ключи, дату и средние температуры/метод из Parquet; максимумы и сведения другой системы не читаются как цель. |
| 288 | Вычисляет/сохраняет raw['report_month'] для следующего шага блока. Загружает выбранную систему по реестру и повторяет проверки исходных данных. |

### Строки 289–300

```python
    raw=raw.loc[raw.plant_id_eia.eq(entry['plant_id_eia']) & raw.cooling_id_eia.eq(entry['cooling_id_eia'])
                & pd.to_datetime(raw.report_date).dt.year.between(2010,2025)]
    frame=from_raw(raw,entry['plant_name'])
    return validate_csv(path,frame,entry['plant_id_eia'],entry['cooling_id_eia']) if source['format']=='csv' else validate_frame(frame,entry['plant_id_eia'],entry['cooling_id_eia'])


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    args=parser.parse_args()
    registry=prepare_registry(args.root)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 289 | Вычисляет/сохраняет raw для следующего шага блока. Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 290 | Продолжает выражение блока «load_observations»: Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 291 | Вычисляет/сохраняет frame для следующего шага блока. Загружает выбранную систему по реестру и повторяет проверки исходных данных. |
| 292 | Возвращает validate_csv(path,frame,entry['plant_id_eia'],entry['cooling_id_eia']) if source['format']=='csv' else validate_frame(frame,entry['plant_id_eia'],entry['cooling_id_eia']) — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |
| 295 | Запускает только подготовку из командной строки и показывает количество статусов. |
| 296 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 297 | Описывает/считывает параметр командной строки; по умолчанию используется корень этого проекта. |
| 298 | Описывает/считывает параметр командной строки; по умолчанию используется корень этого проекта. |
| 299 | Описывает/считывает параметр командной строки; по умолчанию используется корень этого проекта. |
| 300 | Вычисляет/сохраняет registry для следующего шага блока. Запускает только подготовку из командной строки и показывает количество статусов. |

### Строки 301–306

```python
    from collections import Counter
    print(json.dumps(dict(Counter(e['status'] for e in registry['datasets'])),indent=2))


if __name__=='__main__':
    main()
```

| Строка | Что делает и зачем |
| ---: | --- |
| 301 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 302 | Создаёт стабильное JSON-представление; сортировка ключей и запрет NaN нужны для повторяемых байтов и строгого чтения. |
| 305 | Выбирает ветку по явному условию if __name__=='__main__'. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |
| 306 | Продолжает выражение блока «уровень модуля»: подготовка/проверка по явным условиям без обучения. |

## src/model/pipeline.py

### Строки 1–12

```python
"""Parameterize the existing pipeline by dataset_id; preparation only, no fit."""
from .registry import find_dataset, project_path
from .datasets import load_observations, require


def prepare_job(root, identifier):
    entry = find_dataset(root, identifier)
    require(entry['status']=='ready_for_model_check',
            f'Dataset is not ready: {entry["status"]}; {entry["limitations"]}')
    frame = load_observations(root, entry)
    from . import model
    parts = model.prepare_splits(frame)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 1 | Описывает назначение блока; эта строка не выполняет расчётов. |
| 2 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 3 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 6 | Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |
| 7 | Вычисляет/сохраняет entry для следующего шага блока. Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |
| 8 | Проверяет обязательное условие: ready_for_model_check; при нарушении вызывает ValueError. |
| 9 | Продолжает выражение блока «prepare_job»: Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |
| 10 | Вычисляет/сохраняет frame для следующего шага блока. Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |
| 11 | Подключает уже существующий код модели для повторного использования функций; само обучение не вызывается. |
| 12 | Повторно использует прежнюю функцию хронологического разделения; алгоритм не скопирован и fit не вызывается. |

### Строки 13–21

```python
    require({name:len(part) for name,part in parts.items()}==entry['split_counts'],
            'Prepared split sizes changed')
    features = {name:model.make_features(part) for name,part in parts.items()}
    return {'dataset':entry, 'parts':parts, 'features':features,
            'target':'delta_t_c', 'shared_training_function':model.train_model,
            'shared_prediction_function':model.predict_table,
            'results_path':project_path(root,entry['artifacts']['future_results_path']),
            'artifacts_dir':project_path(root,entry['artifacts']['future_artifacts_dir']),
            'preserve_existing_result':entry['model_status']=='existing_verified'}
```

| Строка | Что делает и зачем |
| ---: | --- |
| 13 | Проверяет обязательное условие: split_counts; при нарушении вызывает ValueError. |
| 14 | Продолжает выражение блока «prepare_job»: Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |
| 15 | Вызывает прежнее построение разрешённых признаков: вход и sin/cos месяца, без текущей цели/сброса. |
| 16 | Возвращает {'dataset':entry, 'parts':parts, 'features':features — проверенные данные, метаданные или ссылки на общие функции; сама строка не запускает обучение. |
| 17 | Заполняет метаданные: ссылка на старую train_model, без её вызова. Это описание данных/будущего пути, а не готовая модель. |
| 18 | Заполняет метаданные: ссылка на прежнюю predict_table, без её вызова. Это описание данных/будущего пути, а не готовая модель. |
| 19 | Заполняет метаданные: только существующий результат; иначе null. Это описание данных/будущего пути, а не готовая модель. |
| 20 | Продолжает выражение блока «prepare_job»: Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |
| 21 | Вычисляет/сохраняет 'preserve_existing_result':entry['model_status'] для следующего шага блока. Параметризует существующий pipeline конкретным dataset_id и возвращает входы/пути без fit. |

## tests/model/test_multistation.py

### Строки 1–12

```python
"""Preparation and saved-result regression checks; every fit is forbidden."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
```

| Строка | Что делает и зачем |
| ---: | --- |
| 1 | Описывает назначение блока; эта строка не выполняет расчётов. |
| 2 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 3 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 4 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 5 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 6 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 7 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 8 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 9 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 11 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 12 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |

### Строки 13–24

```python

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.model import datasets, registry, pipeline, model


class PreparationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = registry.read_registry(ROOT)
        cls.entries = cls.data['datasets']
        cls.surry = next(e for e in cls.entries if e['plant_id_eia']==3806 and e['cooling_id_eia']=='CW1')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 14 | Вычисляет/сохраняет ROOT для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 15 | Продолжает выражение блока «уровень модуля»: подготовка/проверка по явным условиям без обучения. |
| 16 | Подключает указанные средства: пути/хеши/JSON для воспроизводимости, pandas/NumPy для таблиц либо unittest/mock для проверок; без побочного запуска pipeline. |
| 19 | Объединяет проверки подготовки в один unittest-класс; тесты запрещают обучение. |
| 20 | Делает общий setup методом класса, чтобы реестр не перечитывался для каждого теста. |
| 21 | Один раз загружает тестируемый реестр и находит прежнюю запись Surry. |
| 22 | Вычисляет/сохраняет cls.data для следующего шага блока. Один раз загружает тестируемый реестр и находит прежнюю запись Surry. |
| 23 | Вычисляет/сохраняет cls.entries для следующего шага блока. Один раз загружает тестируемый реестр и находит прежнюю запись Surry. |
| 24 | Вычисляет/сохраняет cls.surry для следующего шага блока. Один раз загружает тестируемый реестр и находит прежнюю запись Surry. |

### Строки 25–36

```python

    def test_ui_reader_imports_no_ml_or_dataframe_library(self):
        code = (f'import sys;sys.path.insert(0,{str(ROOT)!r});'
                'from src.model.registry import read_registry;'
                f'd=read_registry({str(ROOT)!r});'
                'assert len(d["datasets"])==102;'
                'assert not any(x in sys.modules for x in ["sklearn","pandas","numpy"]);print("OK")')
        result = subprocess.run([sys.executable,'-I','-B','-c',code],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_ids_are_reversible_and_do_not_merge_different_systems(self):
        systems = ['1','CW1','CW-1','cw1','CW/1','CW_1']
```

| Строка | Что делает и зачем |
| ---: | --- |
| 26 | Определяет отдельную проверку test_ui_reader_imports_no_ml_or_dataframe_library; она запускается только тестовым runner. |
| 27 | Вычисляет/сохраняет code для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 28 | Продолжает выражение блока «test_ui_reader_imports_no_ml_or_dataframe_library»: подготовка/проверка по явным условиям без обучения. |
| 29 | Вычисляет/сохраняет f'd для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 30 | Вычисляет/сохраняет 'assert len(d["datasets"]) для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 31 | Продолжает выражение блока «test_ui_reader_imports_no_ml_or_dataframe_library»: подготовка/проверка по явным условиям без обучения. |
| 32 | Запускает изолированный Python-процесс для проверки лёгкого чтения реестра; ML не должен попасть в sys.modules. |
| 33 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 35 | Определяет отдельную проверку test_ids_are_reversible_and_do_not_merge_different_systems; она запускается только тестовым runner. |
| 36 | Вычисляет/сохраняет systems для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |

### Строки 37–48

```python
        identifiers = [registry.dataset_id(3806,s) for s in systems]
        self.assertEqual(len(set(identifiers)),len(systems))
        for identifier,system in zip(identifiers,systems):
            self.assertEqual(bytes.fromhex(identifier.split('_',2)[2]).decode(),system)
        self.assertEqual(len(self.entries),102)
        self.assertEqual(len({e['plant_id_eia'] for e in self.entries}),66)

    def test_original_csv_paths_are_reused(self):
        csv_entries = [e for e in self.entries if e['observations']['format']=='csv']
        self.assertEqual(len(csv_entries),7)
        self.assertEqual(self.surry['observations']['path'],'data/surry_cw1_monthly.csv')
        self.assertTrue(all('/station_csv/' in e['observations']['path'] for e in csv_entries if e!=self.surry))
```

| Строка | Что делает и зачем |
| ---: | --- |
| 37 | Вычисляет/сохраняет identifiers для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 38 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 39 | Проверяет/обрабатывает по одному элементу указанной коллекции: for identifier,system in zip(identifiers,systems). Порядок временных рядов не перемешивается. |
| 40 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 41 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 42 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 44 | Определяет отдельную проверку test_original_csv_paths_are_reused; она запускается только тестовым runner. |
| 45 | Вычисляет/сохраняет csv_entries для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 46 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 47 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 48 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |

### Строки 49–60

```python

    def test_all_ready_jobs_use_shared_pipeline_without_fitting(self):
        ready = [e for e in self.entries if e['status']=='ready_for_model_check']
        self.assertEqual(len(ready),17)
        with patch.object(model,'train_model',side_effect=AssertionError('Training forbidden')):
            with patch('sklearn.linear_model.Ridge.fit',side_effect=AssertionError('Fit forbidden')):
                for entry in ready:
                    job = pipeline.prepare_job(ROOT,entry['dataset_id'])
                    self.assertEqual({k:len(v) for k,v in job['parts'].items()},entry['split_counts'])
                    self.assertTrue(all(v.columns.tolist()==model.FEATURES for v in job['features'].values()))
                    self.assertTrue(all(np.isfinite(v.to_numpy()).all() for v in job['features'].values()))
                    self.assertFalse(entry['review_months'])
```

| Строка | Что делает и зачем |
| ---: | --- |
| 50 | Определяет отдельную проверку test_all_ready_jobs_use_shared_pipeline_without_fitting; она запускается только тестовым runner. |
| 51 | Вычисляет/сохраняет ready для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 52 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 53 | Подменяет указанную функцию исключением: любой случайный вызов обучения немедленно провалит проверку. |
| 54 | Подменяет указанную функцию исключением: любой случайный вызов обучения немедленно провалит проверку. |
| 55 | Проверяет/обрабатывает по одному элементу указанной коллекции: for entry in ready. Порядок временных рядов не перемешивается. |
| 56 | Вычисляет/сохраняет job для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 57 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 58 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 59 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 60 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |

### Строки 61–72

```python

    def test_suspect_measured_values_are_kept_but_job_is_blocked(self):
        entry = next(e for e in self.entries if e['plant_id_eia']==566 and e['cooling_id_eia']=='CIRC2')
        self.assertEqual(entry['status'],'review_required')
        frame = datasets.load_observations(ROOT,entry)
        row = frame.loc[frame.report_month.eq('2023-06')].iloc[0]
        self.assertTrue(row.eligible_measured)
        self.assertEqual(row.delta_t_c,0)
        self.assertEqual(entry['split_counts'],{'train':144,'validation':24,'test':24})
        with self.assertRaisesRegex(ValueError,'not ready'):
            pipeline.prepare_job(ROOT,entry['dataset_id'])

```

| Строка | Что делает и зачем |
| ---: | --- |
| 62 | Определяет отдельную проверку test_suspect_measured_values_are_kept_but_job_is_blocked; она запускается только тестовым runner. |
| 63 | Вычисляет/сохраняет entry для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 64 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 65 | Вычисляет/сохраняет frame для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 66 | Вычисляет/сохраняет row для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 67 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 68 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 69 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 70 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 71 | Продолжает выражение блока «test_suspect_measured_values_are_kept_but_job_is_blocked»: подготовка/проверка по явным условиям без обучения. |

### Строки 73–84

```python
    def test_strict_flags_missing_pair_and_units(self):
        self.assertEqual(datasets.parse_flag(pd.Series(['True','False','false'])).tolist(),[True,False,False])
        with self.assertRaisesRegex(ValueError,'Invalid boolean'):
            datasets.parse_flag(pd.Series(['unknown']))
        frame = datasets.load_observations(ROOT,self.surry)
        bad = frame.copy(); bad.loc[0,'intake_temperature_c'] += 1
        with self.assertRaisesRegex(ValueError,'conversion'):
            datasets.validate_frame(bad,3806,'CW1')
        bad = frame.copy(); bad.loc[0,'delta_t_c'] += 1
        with self.assertRaisesRegex(ValueError,'arithmetic'):
            datasets.validate_frame(bad,3806,'CW1')
        bad = frame.copy(); bad.loc[0,'split']='test'
```

| Строка | Что делает и зачем |
| ---: | --- |
| 73 | Определяет отдельную проверку test_strict_flags_missing_pair_and_units; она запускается только тестовым runner. |
| 74 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 75 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 76 | Продолжает выражение блока «test_strict_flags_missing_pair_and_units»: подготовка/проверка по явным условиям без обучения. |
| 77 | Вычисляет/сохраняет frame для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 78 | Вычисляет/сохраняет bad для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 79 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 80 | Продолжает выражение блока «test_strict_flags_missing_pair_and_units»: подготовка/проверка по явным условиям без обучения. |
| 81 | Вычисляет/сохраняет bad для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 82 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 83 | Продолжает выражение блока «test_strict_flags_missing_pair_and_units»: подготовка/проверка по явным условиям без обучения. |
| 84 | Вычисляет/сохраняет bad для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |

### Строки 85–96

```python
        with self.assertRaisesRegex(ValueError,'split'):
            datasets.validate_frame(bad,3806,'CW1')
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            datasets.validate_frame(pd.concat([frame,frame.iloc[:1]]),3806,'CW1')
        missing=pd.DataFrame({'report_month':['2010-01'],'plant_id_eia':[3806],
            'cooling_id_eia':['CW1'],datasets.F_IN:pd.Series([pd.NA],dtype='Float64'),
            datasets.F_OUT:[60.0],'temperature_method':['Measured continuously with a thermometer']})
        prepared=datasets.from_raw(missing,'Surry')
        self.assertFalse(prepared.pair_available.iloc[0])
        self.assertFalse(prepared.eligible_measured.iloc[0])
        self.assertTrue(pd.isna(prepared.delta_t_c.iloc[0]))

```

| Строка | Что делает и зачем |
| ---: | --- |
| 85 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 86 | Продолжает выражение блока «test_strict_flags_missing_pair_and_units»: подготовка/проверка по явным условиям без обучения. |
| 87 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 88 | Продолжает выражение блока «test_strict_flags_missing_pair_and_units»: подготовка/проверка по явным условиям без обучения. |
| 89 | Заполняет метаданные: точный идентификатор площадки EIA. Это описание данных/будущего пути, а не готовая модель. |
| 90 | Заполняет метаданные: точный ID системы без склейки с другими ID. Это описание данных/будущего пути, а не готовая модель. |
| 91 | Заполняет метаданные: отчётный метод измерения, отдельно от расхода. Это описание данных/будущего пути, а не готовая модель. |
| 92 | Вычисляет/сохраняет prepared для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 93 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 94 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 95 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |

### Строки 97–108

```python
    def test_path_traversal_and_changed_artifact_are_rejected(self):
        for path in ['../secret','C:/secret','/secret','data/../secret',r'data\secret']:
            with self.assertRaises(ValueError):
                registry.project_path(ROOT,path)
        with tempfile.TemporaryDirectory() as directory:
            datasets.write_same_or_new(directory,'data/item.json',{'x':1})
            path=Path(directory)/'data/item.json'
            before=path.read_bytes()
            with self.assertRaisesRegex(ValueError,'refusing overwrite'):
                datasets.write_same_or_new(directory,'data/item.json',{'x':2})
            self.assertEqual(path.read_bytes(),before)

```

| Строка | Что делает и зачем |
| ---: | --- |
| 97 | Определяет отдельную проверку test_path_traversal_and_changed_artifact_are_rejected; она запускается только тестовым runner. |
| 98 | Проверяет/обрабатывает по одному элементу указанной коллекции: for path in ['../secret','C:/secret','/secret','data/../secret',r'data\secret']. Порядок временных рядов не перемешивается. |
| 99 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 100 | Продолжает выражение блока «test_path_traversal_and_changed_artifact_are_rejected»: подготовка/проверка по явным условиям без обучения. |
| 101 | Ограничивает ресурс контекстом; тестовые изменения идут во временный каталог, а новые артефакты создаются без перезаписи. |
| 102 | Продолжает выражение блока «test_path_traversal_and_changed_artifact_are_rejected»: подготовка/проверка по явным условиям без обучения. |
| 103 | Вычисляет/сохраняет path для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 104 | Сравнивает/записывает точные байты; отличающийся уже существующий артефакт не должен быть затёрт. |
| 105 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 106 | Продолжает выражение блока «test_path_traversal_and_changed_artifact_are_rejected»: подготовка/проверка по явным условиям без обучения. |
| 107 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |

### Строки 109–120

```python
    def test_registry_rejects_tampered_selector_and_fake_model_result(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/registry.REGISTRY_PATH
            target.parent.mkdir(parents=True)
            altered=json.loads(json.dumps(self.data))
            altered['datasets'][0]['observations']['selector']['plant_id_eia']=999999
            target.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError,'selector identity'):
                registry.read_registry(directory,verify=False)
            altered=json.loads(json.dumps(self.data))
            entry=next(e for e in altered['datasets'] if e['model_status']=='not_trained')
            entry['results_path']='data/fake.csv'
```

| Строка | Что делает и зачем |
| ---: | --- |
| 109 | Определяет отдельную проверку test_registry_rejects_tampered_selector_and_fake_model_result; она запускается только тестовым runner. |
| 110 | Ограничивает ресурс контекстом; тестовые изменения идут во временный каталог, а новые артефакты создаются без перезаписи. |
| 111 | Вычисляет/сохраняет target для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 112 | Вычисляет/сохраняет target.parent.mkdir(parents для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 113 | Создаёт стабильное JSON-представление; сортировка ключей и запрет NaN нужны для повторяемых байтов и строгого чтения. |
| 114 | Вычисляет/сохраняет altered['datasets'][0]['observations']['selector']['plant_id_eia'] для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 115 | Создаёт стабильное JSON-представление; сортировка ключей и запрет NaN нужны для повторяемых байтов и строгого чтения. |
| 116 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 117 | Вычисляет/сохраняет registry.read_registry(directory,verify для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 118 | Создаёт стабильное JSON-представление; сортировка ключей и запрет NaN нужны для повторяемых байтов и строгого чтения. |
| 119 | Вычисляет/сохраняет entry для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 120 | Вычисляет/сохраняет entry['results_path'] для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |

### Строки 121–132

```python
            target.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError,'Untrained dataset'):
                registry.read_registry(directory,verify=False)

    def test_existing_surry_result_and_hashes_unchanged(self):
        scores=datasets.verify_legacy_result(ROOT,self.surry)
        self.assertAlmostEqual(scores['model_delta_t_c'],1.8493300909090906,places=10)
        self.assertEqual(self.surry['split_counts'],{'train':142,'validation':24,'test':22})
        self.assertEqual(self.surry['results_path'],'data/results.csv')
        self.assertEqual(registry.sha256(ROOT/'data/results.csv'),
                         '428f2546307aae67a29be8c49827faa09e4e3d765b7999a5bdf22426afafd435')
        self.assertEqual(registry.sha256(ROOT/'src/model/model.py'),
```

| Строка | Что делает и зачем |
| ---: | --- |
| 121 | Создаёт стабильное JSON-представление; сортировка ключей и запрет NaN нужны для повторяемых байтов и строгого чтения. |
| 122 | Ожидает отказ для испорченного входа: проверяется защита, а не успешная загрузка плохих данных. |
| 123 | Вычисляет/сохраняет registry.read_registry(directory,verify для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 125 | Определяет отдельную проверку test_existing_surry_result_and_hashes_unchanged; она запускается только тестовым runner. |
| 126 | Вычисляет/сохраняет scores для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 127 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 128 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 129 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 130 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 131 | Продолжает выражение блока «test_existing_surry_result_and_hashes_unchanged»: подготовка/проверка по явным условиям без обучения. |
| 132 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |

### Строки 133–144

```python
                         'b53aec7f6f1870eec9195822e71509c2785e2bf4f92d8c8ec0698378948e9a5a')

    def test_repeated_preparation_has_identical_bytes_and_mtime(self):
        paths=list((ROOT/'data/model_artifacts/multistation').rglob('*.json'))
        before={p:(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns) for p in paths}
        with patch.object(model,'train_model',side_effect=AssertionError('Training forbidden')):
            datasets.prepare_registry(ROOT)
        after={p:(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns) for p in paths}
        self.assertEqual(before,after)


if __name__=='__main__':
```

| Строка | Что делает и зачем |
| ---: | --- |
| 133 | Продолжает выражение блока «test_existing_surry_result_and_hashes_unchanged»: подготовка/проверка по явным условиям без обучения. |
| 135 | Определяет отдельную проверку test_repeated_preparation_has_identical_bytes_and_mtime; она запускается только тестовым runner. |
| 136 | Вычисляет/сохраняет paths для следующего шага блока. Значение используется для воспроизводимой подготовки либо проверки. |
| 137 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 138 | Подменяет указанную функцию исключением: любой случайный вызов обучения немедленно провалит проверку. |
| 139 | Продолжает выражение блока «test_repeated_preparation_has_identical_bytes_and_mtime»: подготовка/проверка по явным условиям без обучения. |
| 140 | Вычисляет, сохраняет либо сравнивает контрольную сумму указанного файла; это привязывает проверку к тем же исходным байтам. |
| 141 | Проверяет указанное ожидаемое свойство/значение; несоответствие даёт провал теста вместо ложного успешного отчёта. |
| 144 | Выбирает ветку по явному условию if __name__=='__main__'. Важно различать отсутствие данных, нерешённую проверку и готовый результат. |

### Строки 145–145

```python
    unittest.main()
```

| Строка | Что делает и зачем |
| ---: | --- |
| 145 | Продолжает выражение блока «уровень модуля»: подготовка/проверка по явным условиям без обучения. |



# Дополнение: обучение и проверка 16 новых моделей

Предыдущий разбор выше сохранён побайтово. В этом дополнении объяснены только новые train_multistation.py и test_trained_multistation.py. model.py, pipeline.py, registry.py, UI и контракт не изменены.

Обучение по-прежнему выполняет model.train_model: StandardScaler+Ridge, четыре заранее заданных alpha, выбор по validation. Адаптер orchestration не содержит второго алгоритма. Calvert выполнена первой; её Ridge хуже baseline, методика оставлена прежней.

В model.export_outputs унаследованы Surry-подпись и проверка 142/24/22. В новых артефактах адаптируются только подпись, identity/contract_version и проверка размеров по реестру. Результаты Surry не открываются на запись.

Статус данных ready_for_model_check не меняется. После проверки нового экспорта model_status становится evaluated_verified, results_path получает реальный путь; evaluation содержит метрики/хеш. Этот статус не обещает преимущество над baseline. Реестр сохраняется через временный соседний файл, flush/fsync и os.replace.

Команды, использованные из корня проекта:

```powershell
python -m src.model.train_multistation --dataset eia_6011_535953303432
python -m src.model.train_multistation --remaining
python -m unittest discover -s tests/model -p test_trained_multistation.py -v
```

Первая команда обрабатывает только Calvert SYS042; выполнена до остальных. Вторая выбирает только ready + not_trained и пропускает Surry/уже оценённые модели. Третья проверяет все сохранённые результаты и отказы, не переобучая их. На этой машине использован bundled Python и PYTHONPATH=D:\workspace\veritas-python, MPLCONFIGDIR=D:\workspace\veritas-mpl.

Не запускать заново prepare_registry ради сброса состояний: он намеренно откажется перезаписывать отличающийся реестр и не удалит проверенные модели. --remaining после успешной партии не обучает их повторно. Ошибки отдельных систем пишутся в failures-<UTC>.json; такая запись не является моделью.

## src/model/train_multistation.py

### Строки 1–12

```python
"""Train isolated ready systems with the existing pipeline; verify before registry update."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
```

| Строка | Что делает и зачем |
| ---: | --- |
| 1 | Объясняет назначение модуля/проверки; вычислений эта строка не запускает. |
| 2 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 3 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 4 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 5 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 6 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 8 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 9 | Продолжает выражение блока уровень модуля: обучение/проверка отдельной системы без смешивания наблюдений. |
| 10 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 11 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 12 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |

### Строки 13–24

```python

from . import model
from .datasets import require
from .pipeline import prepare_job
from .registry import REGISTRY_PATH, find_dataset, project_path, read_registry, sha256

LOCKED_GRID = (0.1, 1.0, 10.0, 100.0)
IDENTITY_FIELDS = ('dataset_id', 'plant_id_eia', 'cooling_id_eia')


def identity(entry):
    return {field: entry[field] for field in IDENTITY_FIELDS}
```

| Строка | Что делает и зачем |
| ---: | --- |
| 14 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 15 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 16 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 17 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 19 | Вычисляет/сохраняет LOCKED_GRID. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 20 | Вычисляет/сохраняет IDENTITY_FIELDS. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 23 | Выделяет точный dataset_id/plant/system, чтобы артефакты нельзя было незаметно приписать другой системе. |
| 24 | Возвращает проверенные данные/метаданные из этого блока. Выделяет точный dataset_id/plant/system, чтобы артефакты нельзя было незаметно приписать другой системе. |

### Строки 25–36

```python


def write_json(path, value, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x' if exclusive else 'w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')


def atomic_registry_update(root, identifier, evaluation):
    path = project_path(root, REGISTRY_PATH)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 27 | Сохраняет собственный JSON с конечными числами; исходные данные и Surry здесь не записываются. |
| 28 | Вычисляет/сохраняет path. Сохраняет собственный JSON с конечными числами; исходные данные и Surry здесь не записываются. |
| 29 | Вычисляет/сохраняет path.parent.mkdir(parents. Сохраняет собственный JSON с конечными числами; исходные данные и Surry здесь не записываются. |
| 30 | Вычисляет/сохраняет with path.open('x' if exclusive else 'w', encoding. Сохраняет собственный JSON с конечными числами; исходные данные и Surry здесь не записываются. |
| 31 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 32 | Записывает собственный новый артефакт/тестовую копию; в рабочем реестре запись выполняется отдельно атомарно. |
| 35 | Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 36 | Вычисляет/сохраняет path. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |

### Строки 37–48

```python
    before = path.read_bytes()
    data = read_registry(root)
    entry = next(e for e in data['datasets'] if e['dataset_id'] == identifier)
    require(entry['model_status'] != 'existing_verified', 'Protected legacy model')
    require(entry['status'] == 'ready_for_model_check', 'Dataset no longer ready')
    entry['model_status'] = 'evaluated_verified'
    entry['results_path'] = entry['artifacts']['future_results_path']
    entry['evaluation'] = evaluation
    payload = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode('utf-8')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='registry-', suffix='.tmp', delete=False) as stream:
```

| Строка | Что делает и зачем |
| ---: | --- |
| 37 | Вычисляет/сохраняет before. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 38 | Вычисляет/сохраняет data. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 39 | Вычисляет/сохраняет entry. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 40 | Проверяет обязательную согласованность: Protected legacy model; при нарушении обработка останавливается, результат не считается проверенным. |
| 41 | Проверяет обязательную согласованность: Dataset no longer ready; при нарушении обработка останавливается, результат не считается проверенным. |
| 42 | Вычисляет/сохраняет entry['model_status']. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 43 | Вычисляет/сохраняет entry['results_path']. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 44 | Вычисляет/сохраняет entry['evaluation']. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 45 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 46 | Вычисляет/сохраняет temporary. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 47 | Ограничивает участок, для которого предусмотрена безопасная обработка ошибок и cleanup. |
| 48 | Создаёт временный файл рядом с реестром, необходимый для атомарного переноса в пределах одного диска. |

### Строки 49–60

```python
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        require(path.read_bytes() == before, 'Concurrent registry change; refusing to replace')
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


```

| Строка | Что делает и зачем |
| ---: | --- |
| 49 | Вычисляет/сохраняет temporary. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 50 | Записывает собственный новый артефакт/тестовую копию; в рабочем реестре запись выполняется отдельно атомарно. |
| 51 | Выводит буфер записи, чтобы реестр заменялся после полной записи файла. |
| 52 | Просит ОС сбросить полностью записанный временный JSON до его атомарной замены. |
| 53 | Проверяет обязательную согласованность: Concurrent registry change; refusing to replace; при нарушении обработка останавливается, результат не считается проверенным. |
| 54 | Атомарно заменяет реестр готовым JSON в той же файловой системе; UI не увидит половину записи. |
| 55 | Вычисляет/сохраняет temporary. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |
| 56 | Гарантирует освобождение временного ресурса или проверку защищённых хешей даже при исключении. |
| 57 | Выбирает ветку по условию if temporary is not None. Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 58 | Вычисляет/сохраняет temporary.unlink(missing_ok. Пишет новый реестр во временный соседний файл, синхронизирует его и заменяет целиком после проверки отсутствия конкурирующей записи. |

### Строки 61–72

```python
def split_record(job):
    return {'identity': identity(job['dataset']),
            'periods': {'train': [2010,2021], 'validation': [2022,2023], 'test': [2024,2025]},
            'months': {name: part.report_month.tolist() for name,part in job['parts'].items()},
            'counts': job['dataset']['split_counts'],
            'excluded_months': job['dataset']['excluded_months'],
            'input_sha256': job['dataset']['observations']['sha256']}


def lock_selection(directory, job, fitted, median, seasonal, candidates):
    scaler, ridge = fitted.steps[0][1], fitted.steps[1][1]
    record = {'identity': identity(job['dataset']), 'locked_before_test': True,
```

| Строка | Что делает и зачем |
| ---: | --- |
| 61 | Фиксирует точные месяцы и размеры хронологических частей без перемешивания. |
| 62 | Возвращает проверенные данные/метаданные из этого блока. Фиксирует точные месяцы и размеры хронологических частей без перемешивания. |
| 63 | Продолжает выражение блока split_record: Фиксирует точные месяцы и размеры хронологических частей без перемешивания. |
| 64 | Продолжает выражение блока split_record: Фиксирует точные месяцы и размеры хронологических частей без перемешивания. |
| 65 | Продолжает выражение блока split_record: Фиксирует точные месяцы и размеры хронологических частей без перемешивания. |
| 66 | Продолжает выражение блока split_record: Фиксирует точные месяцы и размеры хронологических частей без перемешивания. |
| 67 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 70 | Сохраняет выбор alpha, train-параметры и validation до первого вычисления test-оценок. |
| 71 | Вычисляет/сохраняет scaler, ridge. Сохраняет выбор alpha, train-параметры и validation до первого вычисления test-оценок. |
| 72 | Сохраняет точную принадлежность системе, явную отметку порядка выбора до test. Эти поля описывают происхождение и реальный результат, не гарантию качества. |

### Строки 73–84

```python
              'locked_at_utc': datetime.now(timezone.utc).isoformat(),
              'alpha_grid': list(LOCKED_GRID), 'selected_alpha': float(ridge.alpha),
              'validation_candidates': candidates.to_dict(orient='records'),
              'features': model.FEATURES, 'scaler_mean': scaler.mean_.tolist(),
              'scaler_scale': scaler.scale_.tolist(), 'ridge_coef': ridge.coef_.tolist(),
              'ridge_intercept': float(ridge.intercept_), 'train_median_c': median,
              'train_monthly_medians_c': {str(k):float(v) for k,v in seasonal.items()},
              'input_sha256': job['dataset']['observations']['sha256'],
              'pipeline_sha256': sha256(Path(model.__file__))}
    write_json(directory/'selection.json', record, exclusive=True)
    write_json(directory/'splits.json', split_record(job), exclusive=True)
    return sha256(directory/'selection.json')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 73 | Сохраняет фактическое время фиксации. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 74 | Сохраняет заранее заданную сетку, выбранный по validation параметр. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 75 | Сохраняет все результаты validation. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 76 | Сохраняет порядок разрешённых признаков, средние только train. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 77 | Сохраняет масштабы только train, коэффициенты выбранной Ridge. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 78 | Продолжает выражение блока lock_selection: Сохраняет выбор alpha, train-параметры и validation до первого вычисления test-оценок. |
| 79 | Продолжает выражение блока lock_selection: Сохраняет выбор alpha, train-параметры и validation до первого вычисления test-оценок. |
| 80 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 81 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 82 | Вычисляет/сохраняет write_json(directory/'selection.json', record, exclusive. Сохраняет выбор alpha, train-параметры и validation до первого вычисления test-оценок. |
| 83 | Вычисляет/сохраняет write_json(directory/'splits.json', split_record(job), exclusive. Сохраняет выбор alpha, train-параметры и validation до первого вычисления test-оценок. |
| 84 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |

### Строки 85–96

```python


def verify_export(root, identifier, output_dir):
    job = prepare_job(root, identifier)
    entry = job['dataset']
    output_dir = Path(output_dir)
    artifacts = output_dir/'model_artifacts'
    results = pd.read_csv(output_dir/'results.csv')
    require(results.columns.tolist() == model.OUTPUT_FIELDS, 'Results contract mismatch')
    require(results.report_month.is_unique and results.report_month.is_monotonic_increasing, 'Duplicate/unsorted results')
    test = job['parts']['test'].reset_index(drop=True)
    train = job['parts']['train']
```

| Строка | Что делает и зачем |
| ---: | --- |
| 87 | Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 88 | Загружает конкретный dataset_id общим адаптером, повторяя проверки входов и получая прежние split/признаки. |
| 89 | Вычисляет/сохраняет entry. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 90 | Вычисляет/сохраняет output_dir. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 91 | Вычисляет/сохраняет artifacts. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 92 | Читает реальный сохранённый CSV для независимой проверки, а не использует числа из памяти обучения. |
| 93 | Проверяет обязательную согласованность: Results contract mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 94 | Проверяет обязательную согласованность: Duplicate/unsorted results; при нарушении обработка останавливается, результат не считается проверенным. |
| 95 | Вычисляет/сохраняет test. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 96 | Вычисляет/сохраняет train. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |

### Строки 97–108

```python
    require(results.report_month.tolist() == test.report_month.tolist(), 'Wrong system test months')
    require(np.isfinite(results.iloc[:,1:].to_numpy()).all(), 'Missing/nonfinite exported values')
    require(np.allclose(results.intake_temperature_c,test.intake_temperature_c,atol=1.1e-6,rtol=0), 'Export inlet/source mismatch')
    require(np.allclose(results.reported_delta_t_c,test.delta_t_c,atol=1.1e-6,rtol=0), 'Export target/source mismatch')
    median = float(train.delta_t_c.median())
    seasonal = train.groupby(train.date.dt.month).delta_t_c.median()
    require(np.allclose(results.median_baseline_delta_t_c,median,atol=5.1e-7,rtol=0), 'Global baseline is not train-only median')
    require(np.allclose(results.seasonal_baseline_delta_t_c,test.date.dt.month.map(seasonal),atol=5.1e-7,rtol=0), 'Seasonal baseline is not train-only median')
    params = json.loads((artifacts/'parameters.json').read_text(encoding='utf-8'))
    metrics = json.loads((artifacts/'metrics.json').read_text(encoding='utf-8'))
    selection = json.loads((artifacts/'selection.json').read_text(encoding='utf-8'))
    splits = json.loads((artifacts/'splits.json').read_text(encoding='utf-8'))
```

| Строка | Что делает и зачем |
| ---: | --- |
| 97 | Проверяет обязательную согласованность: Wrong system test months; при нарушении обработка останавливается, результат не считается проверенным. |
| 98 | Проверяет обязательную согласованность: Missing/nonfinite exported values; при нарушении обработка останавливается, результат не считается проверенным. |
| 99 | Проверяет обязательную согласованность: Export inlet/source mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 100 | Проверяет обязательную согласованность: Export target/source mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 101 | Пересчитывает baseline только по train, независимо от сохранённого baseline-столбца. |
| 102 | Пересчитывает baseline только по train, независимо от сохранённого baseline-столбца. |
| 103 | Проверяет обязательную согласованность: Global baseline is not train-only median; при нарушении обработка останавливается, результат не считается проверенным. |
| 104 | Проверяет обязательную согласованность: Seasonal baseline is not train-only median; при нарушении обработка останавливается, результат не считается проверенным. |
| 105 | Вычисляет/сохраняет params. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 106 | Вычисляет/сохраняет metrics. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 107 | Вычисляет/сохраняет selection. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 108 | Вычисляет/сохраняет splits. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |

### Строки 109–120

```python
    audit = json.loads((artifacts/'audit.json').read_text(encoding='utf-8'))
    for document in [params,metrics,selection,splits,audit]:
        require(document['identity'] == identity(entry), 'Artifact belongs to another system')
    require(splits == split_record(job), 'Saved splits changed')
    require(selection['locked_before_test'] and selection['alpha_grid'] == list(LOCKED_GRID), 'Selection protocol mismatch')
    require(selection['pipeline_sha256'] == sha256(Path(model.__file__)), 'Pipeline code changed')
    require(selection['input_sha256'] == metrics['input_sha256'] == entry['observations']['sha256'], 'Input provenance mismatch')
    require(metrics['selection_sha256'] == sha256(artifacts/'selection.json'), 'Selection lock changed')
    require(params['features'] == model.FEATURES, 'Unexpected features')
    for field in ['scaler_mean','scaler_scale','ridge_coef','ridge_intercept','train_median_c','train_monthly_medians_c']:
        require(params[field] == selection[field], 'Parameters differ from pre-test selection lock')
    candidates = pd.read_csv(artifacts/'validation_scores.csv')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 109 | Вычисляет/сохраняет audit. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 110 | Обрабатывает каждый указанный файл/признак/набор отдельно: for document in [params,metrics,selection,splits,audit]. Системы не смешиваются. |
| 111 | Проверяет обязательную согласованность: Artifact belongs to another system; при нарушении обработка останавливается, результат не считается проверенным. |
| 112 | Проверяет обязательную согласованность: Saved splits changed; при нарушении обработка останавливается, результат не считается проверенным. |
| 113 | Проверяет обязательную согласованность: Selection protocol mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 114 | Проверяет обязательную согласованность: Pipeline code changed; при нарушении обработка останавливается, результат не считается проверенным. |
| 115 | Проверяет обязательную согласованность: Input provenance mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 116 | Проверяет обязательную согласованность: Selection lock changed; при нарушении обработка останавливается, результат не считается проверенным. |
| 117 | Проверяет обязательную согласованность: Unexpected features; при нарушении обработка останавливается, результат не считается проверенным. |
| 118 | Обрабатывает каждый указанный файл/признак/набор отдельно: for field in ['scaler_mean','scaler_scale','ridge_coef','ridge_intercept','train_median_c','train_monthly_medians_c']. Системы не смешиваются. |
| 119 | Проверяет обязательную согласованность: Parameters differ from pre-test selection lock; при нарушении обработка останавливается, результат не считается проверенным. |
| 120 | Читает реальный сохранённый CSV для независимой проверки, а не использует числа из памяти обучения. |

### Строки 121–132

```python
    require(candidates.alpha.tolist() == list(LOCKED_GRID), 'Candidate grid changed')
    locked_candidates = pd.DataFrame(selection['validation_candidates'])
    require(np.allclose(candidates,locked_candidates,rtol=0,atol=1e-12), 'Validation record mismatch')
    require(candidates.loc[candidates.validation_mae_c.idxmin(),'alpha'] == params['alpha'] == metrics['selected_alpha'] == selection['selected_alpha'], 'Alpha was not selected on validation')
    x_train = job['features']['train'].to_numpy()
    require(np.allclose(params['scaler_mean'],x_train.mean(axis=0),atol=1e-12,rtol=0), 'Scaler mean is not train-only')
    require(np.allclose(params['scaler_scale'],x_train.std(axis=0),atol=1e-12,rtol=0), 'Scaler scale is not train-only')
    require(abs(params['train_median_c']-median)<1e-12, 'Parameter median mismatch')
    require(all(abs(params['train_monthly_medians_c'][str(k)]-v)<1e-12 for k,v in seasonal.items()), 'Parameter seasonal medians mismatch')
    def infer(part):
        x = job['features'][part].to_numpy()
        return ((x-np.array(params['scaler_mean']))/np.array(params['scaler_scale']))@np.array(params['ridge_coef'])+params['ridge_intercept']
```

| Строка | Что делает и зачем |
| ---: | --- |
| 121 | Проверяет обязательную согласованность: Candidate grid changed; при нарушении обработка останавливается, результат не считается проверенным. |
| 122 | Вычисляет/сохраняет locked_candidates. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 123 | Проверяет обязательную согласованность: Validation record mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 124 | Проверяет обязательную согласованность: Alpha was not selected on validation; при нарушении обработка останавливается, результат не считается проверенным. |
| 125 | Вычисляет/сохраняет x_train. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 126 | Проверяет обязательную согласованность: Scaler mean is not train-only; при нарушении обработка останавливается, результат не считается проверенным. |
| 127 | Проверяет обязательную согласованность: Scaler scale is not train-only; при нарушении обработка останавливается, результат не считается проверенным. |
| 128 | Проверяет обязательную согласованность: Parameter median mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 129 | Проверяет обязательную согласованность: Parameter seasonal medians mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 130 | По сохранённым scaler/коэффициентам воспроизводит оценки матричной арифметикой, без fit. |
| 131 | Вычисляет/сохраняет x. По сохранённым scaler/коэффициентам воспроизводит оценки матричной арифметикой, без fit. |
| 132 | Возвращает проверенные данные/метаданные из этого блока. По сохранённым scaler/коэффициентам воспроизводит оценки матричной арифметикой, без fit. |

### Строки 133–144

```python
    require(np.allclose(results.model_delta_t_c,infer('test'),atol=5.1e-7,rtol=0), 'Export differs from saved model parameters')
    val_mae = float(np.abs(infer('validation')-job['parts']['validation'].delta_t_c.to_numpy()).mean())
    require(abs(val_mae-metrics['validation_mae_c']['model_delta_t_c'])<1e-12, 'Validation MAE mismatch')
    scores = {field:float(np.abs(results[field]-results.reported_delta_t_c).mean()) for field in model.OUTPUT_FIELDS[3:]}
    require(all(abs(scores[k]-metrics['test_mae_c'][k])<=1e-6 for k in scores), 'Saved MAE mismatch beyond CSV rounding')
    require(metrics['test_months'] == results.report_month.tolist(), 'Metrics use different test months')
    for name,part in job['parts'].items():
        expected={'n':len(part),'start':part.report_month.min(),'end':part.report_month.max()}
        require(metrics['split'][name]==expected, 'Metric split metadata mismatch')
    errors=pd.read_csv(artifacts/'test_errors.csv')
    require(errors.report_month.tolist()==results.report_month.tolist(), 'Error file uses other months')
    require(np.allclose(errors[model.OUTPUT_FIELDS[1:]],results[model.OUTPUT_FIELDS[1:]],atol=5.1e-7,rtol=0), 'Error table values mismatch')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 133 | Проверяет обязательную согласованность: Export differs from saved model parameters; при нарушении обработка останавливается, результат не считается проверенным. |
| 134 | Независимо считает MAE как среднее абсолютной разности; model.score_table здесь не используется. |
| 135 | Проверяет обязательную согласованность: Validation MAE mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 136 | Независимо считает MAE как среднее абсолютной разности; model.score_table здесь не используется. |
| 137 | Проверяет обязательную согласованность: Saved MAE mismatch beyond CSV rounding; при нарушении обработка останавливается, результат не считается проверенным. |
| 138 | Проверяет обязательную согласованность: Metrics use different test months; при нарушении обработка останавливается, результат не считается проверенным. |
| 139 | Обрабатывает каждый указанный файл/признак/набор отдельно: for name,part in job['parts'].items(). Системы не смешиваются. |
| 140 | Вычисляет/сохраняет expected. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 141 | Проверяет обязательную согласованность: Metric split metadata mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 142 | Читает реальный сохранённый CSV для независимой проверки, а не использует числа из памяти обучения. |
| 143 | Проверяет обязательную согласованность: Error file uses other months; при нарушении обработка останавливается, результат не считается проверенным. |
| 144 | Проверяет обязательную согласованность: Error table values mismatch; при нарушении обработка останавливается, результат не считается проверенным. |

### Строки 145–156

```python
    require(np.allclose(errors.absolute_model_error_c,np.abs(errors.model_delta_t_c-errors.reported_delta_t_c),atol=1e-12,rtol=0), 'Error table arithmetic mismatch')
    report=(artifacts/'evaluation.md').read_text(encoding='utf-8')
    require(report.startswith(f'# {entry["plant_name"]} / {entry["cooling_id_eia"]} evaluation'), 'Wrong station label in report')
    worst_index = np.abs(results.model_delta_t_c-results.reported_delta_t_c).idxmax()
    worst = results.loc[worst_index].to_dict()
    worst['absolute_model_error_c'] = float(abs(worst['model_delta_t_c']-worst['reported_delta_t_c']))
    require(worst['report_month']==metrics['worst_model_error']['report_month'], 'Wrong error example')
    require(abs(worst['absolute_model_error_c']-metrics['worst_model_error']['absolute_model_error_c'])<1e-6, 'Error example mismatch')
    hashes = {p.relative_to(output_dir).as_posix():sha256(p) for p in sorted(output_dir.rglob('*')) if p.is_file() and p.name!='verification.json'}
    best = min(scores[k] for k in model.OUTPUT_FIELDS[3:5])
    return {'identity':identity(entry), 'verified':True, 'independent_csv_mae_c':scores,
            'test_n':len(results), 'split_counts':entry['split_counts'],
```

| Строка | Что делает и зачем |
| ---: | --- |
| 145 | Проверяет обязательную согласованность: Error table arithmetic mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 146 | Вычисляет/сохраняет report. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 147 | Проверяет обязательную согласованность: Wrong station label in report; при нарушении обработка останавливается, результат не считается проверенным. |
| 148 | Вычисляет/сохраняет worst_index. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 149 | Вычисляет/сохраняет worst. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 150 | Вычисляет/сохраняет worst['absolute_model_error_c']. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 151 | Проверяет обязательную согласованность: Wrong error example; при нарушении обработка останавливается, результат не считается проверенным. |
| 152 | Проверяет обязательную согласованность: Error example mismatch; при нарушении обработка останавливается, результат не считается проверенным. |
| 153 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 154 | Вычисляет/сохраняет best. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 155 | Возвращает проверенные данные/метаданные из этого блока. Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 156 | Продолжает выражение блока verify_export: Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |

### Строки 157–168

```python
            'beats_best_baseline':scores['model_delta_t_c']<best,
            'improvement_vs_best_baseline_c':best-scores['model_delta_t_c'],
            'worst_error_from_csv':worst, 'artifact_sha256':hashes}


def register_verified(root, identifier, verification):
    entry = find_dataset(root,identifier)
    base = project_path(root,entry['artifacts']['future_results_path']).parent
    atomic_registry_update(root,identifier,{
        'metrics_path':(base/'model_artifacts/metrics.json').relative_to(root).as_posix(),
        'verification_path':(base/'model_artifacts/verification.json').relative_to(root).as_posix(),
        'results_sha256':sha256(base/'results.csv'), 'test_n':verification['test_n'],
```

| Строка | Что делает и зачем |
| ---: | --- |
| 157 | Сохраняет строгое сравнение с лучшим baseline без обещания улучшения. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 158 | Продолжает выражение блока verify_export: Независимо проверяет сохранённый CSV, принадлежность системе, train-медианы, параметры и MAE; не обучает модель. |
| 159 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 162 | Передаёт атомарному обновлению только уже проверенный результат и его метаданные. |
| 163 | Вычисляет/сохраняет entry. Передаёт атомарному обновлению только уже проверенный результат и его метаданные. |
| 164 | Вычисляет/сохраняет base. Передаёт атомарному обновлению только уже проверенный результат и его метаданные. |
| 165 | Продолжает выражение блока register_verified: Передаёт атомарному обновлению только уже проверенный результат и его метаданные. |
| 166 | Сохраняет точный путь сохранённых метрик. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 167 | Сохраняет путь отдельной независимой проверки. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 168 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |

### Строки 169–180

```python
        'mae_c':verification['independent_csv_mae_c'],
        'beats_best_baseline':verification['beats_best_baseline']})


def train_dataset(root, identifier):
    root = Path(root).resolve()
    job = prepare_job(root,identifier)
    entry = job['dataset']
    require(not job['preserve_existing_result'], 'Surry CW1 is protected; no retraining')
    require(tuple(model.ALPHAS)==LOCKED_GRID, 'Shared Ridge grid differs from predefined protocol')
    final = job['results_path'].parent
    require(final.resolve().is_relative_to(root), 'Output directory escapes project')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 169 | Продолжает выражение блока register_verified: Передаёт атомарному обновлению только уже проверенный результат и его метаданные. |
| 170 | Сохраняет строгое сравнение с лучшим baseline без обещания улучшения. Эти поля описывают происхождение и реальный результат, не гарантию качества. |
| 173 | Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 174 | Вычисляет/сохраняет root. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 175 | Загружает конкретный dataset_id общим адаптером, повторяя проверки входов и получая прежние split/признаки. |
| 176 | Вычисляет/сохраняет entry. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 177 | Проверяет обязательную согласованность: Surry CW1 is protected; no retraining; при нарушении обработка останавливается, результат не считается проверенным. |
| 178 | Проверяет обязательную согласованность: Shared Ridge grid differs from predefined protocol; при нарушении обработка останавливается, результат не считается проверенным. |
| 179 | Вычисляет/сохраняет final. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 180 | Проверяет обязательную согласованность: Output directory escapes project; при нарушении обработка останавливается, результат не считается проверенным. |

### Строки 181–192

```python
    if (final/'results.csv').exists() and (final/'model_artifacts').is_dir():
        verification = verify_export(root,identifier,final)
        write_json(final/'model_artifacts/verification.json',verification)
        register_verified(root,identifier,verification)
        return verification
    require(entry['model_status']=='not_trained', 'Unexpected model state; no retraining')
    require(not (final/'results.csv').exists() and not (final/'model_artifacts').exists(), 'Partial output exists; preserve for inspection')
    final.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.training-',dir=final) as temporary:
        stage = Path(temporary)
        artifacts = stage/'model_artifacts'
        train, validation = job['parts']['train'], job['parts']['validation']
```

| Строка | Что делает и зачем |
| ---: | --- |
| 181 | Выбирает ветку по условию if (final/'results.csv').exists() and (final/'model_artifacts').is_dir(). Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 182 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 183 | Записывает собственный новый артефакт/тестовую копию; в рабочем реестре запись выполняется отдельно атомарно. |
| 184 | Продолжает выражение блока train_dataset: Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 185 | Возвращает проверенные данные/метаданные из этого блока. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 186 | Проверяет обязательную согласованность: Unexpected model state; no retraining; при нарушении обработка останавливается, результат не считается проверенным. |
| 187 | Проверяет обязательную согласованность: Partial output exists; preserve for inspection; при нарушении обработка останавливается, результат не считается проверенным. |
| 188 | Вычисляет/сохраняет final.mkdir(parents. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 189 | Изолирует ещё не проверенный экспорт/тестовую копию в собственном временном каталоге, не трогая исходники. |
| 190 | Вычисляет/сохраняет stage. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 191 | Вычисляет/сохраняет artifacts. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 192 | Вычисляет/сохраняет train, validation. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |

### Строки 193–204

```python
        fitted, median, seasonal, candidates = job['shared_training_function'](train,validation)
        selection_hash = lock_selection(artifacts,job,fitted,median,seasonal,candidates)
        results = job['shared_prediction_function'](job['parts']['test'],fitted,median,seasonal)
        figure = model.plot_results(results)
        figure.axes[0].set_title(f'{entry["plant_name"]} / {entry["cooling_id_eia"]}: retrospective test estimates')
        try:
            audit = {'input_sha256':entry['observations']['sha256'], 'identity':identity(entry),
                     'provenance':entry['provenance'], 'limitations':entry['limitations']}
            model.export_outputs(stage,project_path(root,entry['observations']['path']),audit,
                                 job['parts'],fitted,median,seasonal,candidates,results,figure)
        finally:
            plt.close(figure)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 193 | Вызывает существующий model.train_model только с train и validation; test не передаётся для выбора. |
| 194 | Записывает неизменную запись выбора до финального test и получает её хеш для последующей проверки. |
| 195 | После записи selection.json вычисляет test-оценки выбранной модели прежней predict_table. |
| 196 | Вычисляет/сохраняет figure. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 197 | Продолжает выражение блока train_dataset: Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 198 | Ограничивает участок, для которого предусмотрена безопасная обработка ошибок и cleanup. |
| 199 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 200 | Продолжает выражение блока train_dataset: Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 201 | Переиспользует прежний экспорт CSV/параметров/метрик/графика. Следующие строки адаптируют только идентичность и подписи для новой системы. |
| 202 | Продолжает выражение блока train_dataset: Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 203 | Гарантирует освобождение временного ресурса или проверку защищённых хешей даже при исключении. |
| 204 | Продолжает выражение блока train_dataset: Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |

### Строки 205–216

```python
        for name in ['metrics.json','parameters.json','audit.json']:
            path = artifacts/name
            data = json.loads(path.read_text(encoding='utf-8'))
            data['identity'] = identity(entry)
            if name=='metrics.json':
                data['contract_version']='v2'
                data['selection_sha256']=selection_hash
            if name=='audit.json':
                data.pop('expected_split_counts_match',None)
                data['registry_split_counts_match']=data['split_counts']==entry['split_counts']
            write_json(path,data)
        report_path=artifacts/'evaluation.md'
```

| Строка | Что делает и зачем |
| ---: | --- |
| 205 | Обрабатывает каждый указанный файл/признак/набор отдельно: for name in ['metrics.json','parameters.json','audit.json']. Системы не смешиваются. |
| 206 | Вычисляет/сохраняет path. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 207 | Вычисляет/сохраняет data. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 208 | Вычисляет/сохраняет data['identity']. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 209 | Выбирает ветку по условию if name=='metrics.json'. Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 210 | Вычисляет/сохраняет data['contract_version']. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 211 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 212 | Выбирает ветку по условию if name=='audit.json'. Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 213 | Убирает из нового аудита специфическую для старого Surry проверку 142/24/22; вместо неё сверяются размеры текущего реестра. |
| 214 | Вычисляет/сохраняет data['registry_split_counts_match']. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 215 | Записывает собственный новый артефакт/тестовую копию; в рабочем реестре запись выполняется отдельно атомарно. |
| 216 | Вычисляет/сохраняет report_path. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |

### Строки 217–228

```python
        text=report_path.read_text(encoding='utf-8')
        report_path.write_text(text.replace('# Surry CW1 evaluation',f'# {entry["plant_name"]} / {entry["cooling_id_eia"]} evaluation',1),encoding='utf-8')
        verification=verify_export(root,identifier,stage)
        write_json(artifacts/'verification.json',verification,exclusive=True)
        require(not (final/'results.csv').exists() and not (final/'model_artifacts').exists(),'Concurrent output appeared')
        os.rename(artifacts,final/'model_artifacts')
        os.rename(stage/'results.csv',final/'results.csv')
    verification=verify_export(root,identifier,final)
    register_verified(root,identifier,verification)
    return verification


```

| Строка | Что делает и зачем |
| ---: | --- |
| 217 | Вычисляет/сохраняет text. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 218 | Исправляет лишь унаследованную подпись отчёта на текущую станцию/систему; метод и числовые результаты не меняются. |
| 219 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 220 | Вычисляет/сохраняет write_json(artifacts/'verification.json',verification,exclusive. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 221 | Проверяет обязательную согласованность: Concurrent output appeared; при нарушении обработка останавливается, результат не считается проверенным. |
| 222 | Переносит уже проверенный новый артефакт в отдельный путь этой системы; существующие выходы предварительно запрещены. |
| 223 | Переносит уже проверенный новый артефакт в отдельный путь этой системы; существующие выходы предварительно запрещены. |
| 224 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 225 | Продолжает выражение блока train_dataset: Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |
| 226 | Возвращает проверенные данные/метаданные из этого блока. Для одной допущенной новой системы вызывает существующий pipeline, проверяет экспорт и только затем публикует его в локальном реестре. |

### Строки 229–240

```python
def protection_snapshot(root):
    root=Path(root)
    paths=[*root.joinpath('data/incoming').rglob('*'),*root.joinpath('data/model_artifacts').glob('*'),
           root/'data/results.csv',root/'data/surry_cw1_monthly.csv',root/'src/model/model.py',
           root/'src/model/surry_model.ipynb',*root.joinpath('src/ui').glob('*.py'),root/'docs/work/DATA_CONTRACT.md']
    return {str(p):sha256(p) for p in paths if p.is_file()}


def assert_protected(snapshot):
    require(all(sha256(path)==value for path,value in snapshot.items()),'Protected source/Surry/UI/contract hash changed')


```

| Строка | Что делает и зачем |
| ---: | --- |
| 229 | Собирает хеши неизменяемых исходников, Surry, UI и контракта перед работой. |
| 230 | Вычисляет/сохраняет root. Собирает хеши неизменяемых исходников, Surry, UI и контракта перед работой. |
| 231 | Вычисляет/сохраняет paths. Собирает хеши неизменяемых исходников, Surry, UI и контракта перед работой. |
| 232 | Продолжает выражение блока protection_snapshot: Собирает хеши неизменяемых исходников, Surry, UI и контракта перед работой. |
| 233 | Продолжает выражение блока protection_snapshot: Собирает хеши неизменяемых исходников, Surry, UI и контракта перед работой. |
| 234 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 237 | Останавливает работу, если изменился любой защищённый файл. |
| 238 | Проверяет обязательную согласованность: Protected source/Surry/UI/contract hash changed; при нарушении обработка останавливается, результат не считается проверенным. |

### Строки 241–252

```python
def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--dataset')
    parser.add_argument('--remaining',action='store_true')
    args=parser.parse_args()
    require(bool(args.dataset)!=args.remaining,'Choose exactly --dataset ID or --remaining')
    root=args.root.resolve()
    protected=protection_snapshot(root)
    data=read_registry(root)
    ready=[e for e in data['datasets'] if e['status']=='ready_for_model_check']
```

| Строка | Что делает и зачем |
| ---: | --- |
| 241 | Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 242 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 243 | Вычисляет/сохраняет parser. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 244 | Вычисляет/сохраняет parser.add_argument('--root',type. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 245 | Продолжает выражение блока main: Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 246 | Вычисляет/сохраняет parser.add_argument('--remaining',action. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 247 | Вычисляет/сохраняет args. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 248 | Проверяет обязательную согласованность: Choose exactly --dataset ID or --remaining; при нарушении обработка останавливается, результат не считается проверенным. |
| 249 | Вычисляет/сохраняет root. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 250 | Вычисляет/сохраняет protected. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 251 | Вычисляет/сохраняет data. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 252 | Вычисляет/сохраняет ready. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |

### Строки 253–264

```python
    require(len(ready)==17,'Ready membership changed; review before batch')
    selected=[e for e in ready if e['model_status']=='not_trained'] if args.remaining else [find_dataset(root,args.dataset)]
    failures=[]
    try:
        for entry in selected:
            try:
                check=train_dataset(root,entry['dataset_id'])
                print(json.dumps({'dataset_id':entry['dataset_id'],'verified':True,'mae_c':check['independent_csv_mae_c']},ensure_ascii=False),flush=True)
            except Exception as error:
                failures.append({'dataset_id':entry['dataset_id'],'error_type':type(error).__name__,'reason':str(error)})
                print(json.dumps(failures[-1],ensure_ascii=False),flush=True)
            assert_protected(protected)
```

| Строка | Что делает и зачем |
| ---: | --- |
| 253 | Проверяет обязательную согласованность: Ready membership changed; review before batch; при нарушении обработка останавливается, результат не считается проверенным. |
| 254 | Вычисляет/сохраняет selected. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 255 | Вычисляет/сохраняет failures. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 256 | Ограничивает участок, для которого предусмотрена безопасная обработка ошибок и cleanup. |
| 257 | Обрабатывает каждый указанный файл/признак/набор отдельно: for entry in selected. Системы не смешиваются. |
| 258 | Ограничивает участок, для которого предусмотрена безопасная обработка ошибок и cleanup. |
| 259 | Вычисляет/сохраняет check. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 260 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 261 | Сохраняет причину локального отказа и позволяет обработать независимые наборы; фиктивные значения не создаются. |
| 262 | Продолжает выражение блока main: Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 263 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 264 | Продолжает выражение блока main: Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |

### Строки 265–274

```python
    finally:
        assert_protected(protected)
    if failures:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
        write_json(project_path(root,f'data/model_artifacts/multistation/failures-{stamp}.json'),failures,exclusive=True)
        raise SystemExit(1)


if __name__=='__main__':
    main()
```

| Строка | Что делает и зачем |
| ---: | --- |
| 265 | Гарантирует освобождение временного ресурса или проверку защищённых хешей даже при исключении. |
| 266 | Продолжает выражение блока main: Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 267 | Выбирает ветку по условию if failures. Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 268 | Вычисляет/сохраняет stamp. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 269 | Вычисляет/сохраняет write_json(project_path(root,f'data/model_artifacts/multistation/failures-{stamp}.json'),failures,exclusive. Выбирает одну систему либо оставшиеся неоценённые ready-наборы и продолжает независимые системы после локальной ошибки. |
| 270 | Передаёт ошибку вызывающему коду/командной строке; не выдаёт отказ за успешный расчёт. |
| 273 | Выбирает ветку по условию if __name__=='__main__'. Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 274 | Продолжает выражение блока уровень модуля: обучение/проверка отдельной системы без смешивания наблюдений. |

## tests/model/test_trained_multistation.py

### Строки 1–12

```python
"""Check saved multi-system artifacts and failure paths without fitting models."""
from pathlib import Path
import copy
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

```

| Строка | Что делает и зачем |
| ---: | --- |
| 1 | Объясняет назначение модуля/проверки; вычислений эта строка не запускает. |
| 2 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 3 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 4 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 5 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 6 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 7 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 8 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 9 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 11 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |

### Строки 13–24

```python
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from src.model import model
from src.model.registry import REGISTRY_PATH, read_registry, sha256
from src.model.train_multistation import atomic_registry_update, train_dataset, verify_export


class SavedModelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=read_registry(ROOT)
        cls.calvert=next(e for e in cls.registry['datasets'] if e['plant_id_eia']==6011 and e['cooling_id_eia']=='SYS042')
```

| Строка | Что делает и зачем |
| ---: | --- |
| 13 | Вычисляет/сохраняет ROOT. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 14 | Продолжает выражение блока уровень модуля: обучение/проверка отдельной системы без смешивания наблюдений. |
| 15 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 16 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 17 | Подключает указанный существующий модуль или стандартные средства. Сам импорт не запускает fit; используется общий pipeline, а не второй алгоритм. |
| 20 | Группирует регрессии сохранённых моделей и защитные проверки без повторного обучения. |
| 21 | Разрешает общему setup один раз прочитать реестр для всех тестов. |
| 22 | Один раз читает проверяемый реестр и находит Calvert для тестов сохранённых файлов. |
| 23 | Вычисляет/сохраняет cls.registry. Один раз читает проверяемый реестр и находит Calvert для тестов сохранённых файлов. |
| 24 | Вычисляет/сохраняет cls.calvert. Один раз читает проверяемый реестр и находит Calvert для тестов сохранённых файлов. |

### Строки 25–36

```python
        cls.calvert_dir=(ROOT/cls.calvert['artifacts']['future_results_path']).parent

    def test_all_sixteen_saved_models_verify_without_fit(self):
        evaluated=[e for e in self.registry['datasets'] if e['model_status']=='evaluated_verified']
        self.assertEqual(len(evaluated),16)
        with patch.object(model,'train_model',side_effect=AssertionError('No fitting in verification')):
            for entry in evaluated:
                directory=(ROOT/entry['results_path']).parent
                result=verify_export(ROOT,entry['dataset_id'],directory)
                self.assertTrue(result['verified'])
                self.assertEqual(result['test_n'],entry['split_counts']['test'])
                self.assertEqual(sha256(ROOT/entry['results_path']),entry['evaluation']['results_sha256'])
```

| Строка | Что делает и зачем |
| ---: | --- |
| 25 | Вычисляет/сохраняет cls.calvert_dir. Один раз читает проверяемый реестр и находит Calvert для тестов сохранённых файлов. |
| 27 | Определяет изолированную проверку test_all_sixteen_saved_models_verify_without_fit с безопасными тестовыми входами. |
| 28 | Вычисляет/сохраняет evaluated. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 29 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |
| 30 | Имитирует отказ или запрещает fit в тесте, чтобы проверить защиту без реального изменения моделей. |
| 31 | Обрабатывает каждый указанный файл/признак/набор отдельно: for entry in evaluated. Системы не смешиваются. |
| 32 | Вычисляет/сохраняет directory. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 33 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 34 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |
| 35 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |
| 36 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |

### Строки 37–48

```python

    def test_surry_and_review_dataset_cannot_train(self):
        surry=next(e for e in self.registry['datasets'] if e['plant_id_eia']==3806 and e['cooling_id_eia']=='CW1')
        pending=next(e for e in self.registry['datasets'] if e['status']=='review_required')
        before=sha256(ROOT/'data/results.csv')
        with patch.object(model,'train_model',side_effect=AssertionError('Fit forbidden')):
            with self.assertRaisesRegex(ValueError,'protected'):
                train_dataset(ROOT,surry['dataset_id'])
            with self.assertRaisesRegex(ValueError,'not ready'):
                train_dataset(ROOT,pending['dataset_id'])
        self.assertEqual(sha256(ROOT/'data/results.csv'),before)

```

| Строка | Что делает и зачем |
| ---: | --- |
| 38 | Определяет изолированную проверку test_surry_and_review_dataset_cannot_train с безопасными тестовыми входами. |
| 39 | Вычисляет/сохраняет surry. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 40 | Вычисляет/сохраняет pending. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 41 | Фиксирует/сверяет хеш указанного входа, выбора или результата, связывая оценку с конкретными байтами. |
| 42 | Имитирует отказ или запрещает fit в тесте, чтобы проверить защиту без реального изменения моделей. |
| 43 | Проверяет, что повреждённый вход действительно отвергается с указанной причиной. |
| 44 | Продолжает выражение блока test_surry_and_review_dataset_cannot_train: обучение/проверка отдельной системы без смешивания наблюдений. |
| 45 | Проверяет, что повреждённый вход действительно отвергается с указанной причиной. |
| 46 | Продолжает выражение блока test_surry_and_review_dataset_cannot_train: обучение/проверка отдельной системы без смешивания наблюдений. |
| 47 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |

### Строки 49–60

```python
    def test_corrupted_export_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copied=Path(directory)/'copy'
            shutil.copytree(self.calvert_dir,copied)
            data=pd.read_csv(copied/'results.csv')
            data.loc[0,'reported_delta_t_c']+=1
            data.to_csv(copied/'results.csv',index=False)
            with self.assertRaisesRegex(ValueError,'target/source'):
                verify_export(ROOT,self.calvert['dataset_id'],copied)

    def test_wrong_system_identity_and_changed_selection_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
```

| Строка | Что делает и зачем |
| ---: | --- |
| 49 | Определяет изолированную проверку test_corrupted_export_is_rejected с безопасными тестовыми входами. |
| 50 | Изолирует ещё не проверенный экспорт/тестовую копию в собственном временном каталоге, не трогая исходники. |
| 51 | Вычисляет/сохраняет copied. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 52 | Создаёт/восстанавливает только временную тестовую копию для проверки повреждений; рабочие артефакты не меняются. |
| 53 | Читает реальный сохранённый CSV для независимой проверки, а не использует числа из памяти обучения. |
| 54 | Вычисляет/сохраняет data.loc[0,'reported_delta_t_c']+. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 55 | Вычисляет/сохраняет data.to_csv(copied/'results.csv',index. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 56 | Проверяет, что повреждённый вход действительно отвергается с указанной причиной. |
| 57 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 59 | Определяет изолированную проверку test_wrong_system_identity_and_changed_selection_are_rejected с безопасными тестовыми входами. |
| 60 | Изолирует ещё не проверенный экспорт/тестовую копию в собственном временном каталоге, не трогая исходники. |

### Строки 61–72

```python
            copied=Path(directory)/'copy'
            shutil.copytree(self.calvert_dir,copied)
            path=copied/'model_artifacts/parameters.json'
            parameters=json.loads(path.read_text())
            parameters['identity']['plant_id_eia']=3806
            path.write_text(json.dumps(parameters))
            with self.assertRaisesRegex(ValueError,'another system'):
                verify_export(ROOT,self.calvert['dataset_id'],copied)
            shutil.copyfile(self.calvert_dir/'model_artifacts/parameters.json',path)
            selection=copied/'model_artifacts/selection.json'
            value=json.loads(selection.read_text())
            value['selected_alpha']=123
```

| Строка | Что делает и зачем |
| ---: | --- |
| 61 | Вычисляет/сохраняет copied. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 62 | Создаёт/восстанавливает только временную тестовую копию для проверки повреждений; рабочие артефакты не меняются. |
| 63 | Вычисляет/сохраняет path. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 64 | Вычисляет/сохраняет parameters. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 65 | Вычисляет/сохраняет parameters['identity']['plant_id_eia']. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 66 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 67 | Проверяет, что повреждённый вход действительно отвергается с указанной причиной. |
| 68 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 69 | Создаёт/восстанавливает только временную тестовую копию для проверки повреждений; рабочие артефакты не меняются. |
| 70 | Вычисляет/сохраняет selection. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 71 | Вычисляет/сохраняет value. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 72 | Вычисляет/сохраняет value['selected_alpha']. Значение используется для обучения отдельной системы или проверки сохранённого результата. |

### Строки 73–84

```python
            selection.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError,'Selection lock changed'):
                verify_export(ROOT,self.calvert['dataset_id'],copied)

    def test_atomic_write_failure_keeps_previous_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            path=root/REGISTRY_PATH
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(self.registry))
            before=path.read_bytes()
            with patch('src.model.train_multistation.read_registry',return_value=copy.deepcopy(self.registry)):
```

| Строка | Что делает и зачем |
| ---: | --- |
| 73 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 74 | Проверяет, что повреждённый вход действительно отвергается с указанной причиной. |
| 75 | Проверяет фактические сохранённые файлы независимой формулой MAE и сопоставлением с исходной системой, без fit. |
| 77 | Определяет изолированную проверку test_atomic_write_failure_keeps_previous_registry с безопасными тестовыми входами. |
| 78 | Изолирует ещё не проверенный экспорт/тестовую копию в собственном временном каталоге, не трогая исходники. |
| 79 | Вычисляет/сохраняет root. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 80 | Вычисляет/сохраняет path. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 81 | Вычисляет/сохраняет path.parent.mkdir(parents. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 82 | Сериализует полные JSON-метаданные в стабильном формате; NaN запрещён, частичный JSON в реестр не поступает. |
| 83 | Вычисляет/сохраняет before. Значение используется для обучения отдельной системы или проверки сохранённого результата. |
| 84 | Имитирует отказ или запрещает fit в тесте, чтобы проверить защиту без реального изменения моделей. |

### Строки 85–93

```python
                with patch('src.model.train_multistation.os.replace',side_effect=OSError('simulated failure')):
                    with self.assertRaises(OSError):
                        atomic_registry_update(root,self.calvert['dataset_id'],self.calvert['evaluation'])
            self.assertEqual(path.read_bytes(),before)
            self.assertFalse(list(path.parent.glob('registry-*.tmp')))


if __name__=='__main__':
    unittest.main()
```

| Строка | Что делает и зачем |
| ---: | --- |
| 85 | Атомарно заменяет реестр готовым JSON в той же файловой системе; UI не увидит половину записи. |
| 86 | Проверяет, что повреждённый вход действительно отвергается с указанной причиной. |
| 87 | Продолжает выражение блока test_atomic_write_failure_keeps_previous_registry: обучение/проверка отдельной системы без смешивания наблюдений. |
| 88 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |
| 89 | Сравнивает фактический результат проверки с ожидаемым; отличие должно провалить тест. |
| 92 | Выбирает ветку по условию if __name__=='__main__'. Это защита порядка выполнения, сохранности файлов или допустимости набора. |
| 93 | Продолжает выражение блока уровень модуля: обучение/проверка отдельной системы без смешивания наблюдений. |

