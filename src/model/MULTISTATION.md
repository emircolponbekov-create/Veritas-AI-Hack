# Подготовка нескольких систем без обучения

Действующая спецификация — `docs/work/DATA_CONTRACT.md`, v2. Прежний Surry v1 сохранён.
Работать из `D:\Projects\Veritas AI Hack`. Исходные CSV/Parquet в incoming не меняются.

## Что создано

- `registry.py` — лёгкое чтение реестра стандартной библиотекой. Не импортирует pandas/sklearn и не обучает.
- `datasets.py` — проверка входов по хешам инвентаря, приведение температур в памяти, аудит 102 отдельных систем, создание детерминированного реестра.
- `pipeline.py` — задание по dataset_id, которое использует существующие `model.prepare_splits` и `model.make_features`. Возвращает ссылки на прежние функции обучения/оценки, но их не вызывает.
- `data/model_artifacts/multistation/registry.json` — реестр путей, источников, состояний и размеров split для 102 систем 66 площадок.
- `data/model_artifacts/multistation/datasets/<dataset_id>/audit.json` — отдельная проверка системы. Это отчёт данных, не модель и не предсказания.

Оригинальные 7 CSV переиспользуются. Для остальных систем реестр указывает Parquet и точный selector; загрузчик воспроизводимо строит таблицу в памяти. Дополнительные CSV с теми же наблюдениями не создаются.

## Запуск

В обычной Python-среде нужны pandas, numpy, pyarrow. Для задания pipeline и проверок прежнего model.py также нужны matplotlib и scikit-learn. Установка в свою среду:

```powershell
python -m pip install pandas numpy pyarrow matplotlib scikit-learn
python -m src.model.datasets
python -m unittest discover -s tests/model -p test_multistation.py -v
```

На этом ноутбуке фактически использована отдельная рабочая установка:

```powershell
$env:PYTHONPATH = 'D:\workspace\veritas-python'
$env:MPLCONFIGDIR = 'D:\workspace\veritas-mpl'
& 'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -m src.model.datasets
& 'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -m unittest discover -s tests/model -p test_multistation.py -v
```

Повторная подготовка проверяет совпадение байтов созданных JSON и не меняет их время записи. Если новый результат подготовки отличается, команда откажется перезаписывать файлы: нужно отдельно разобрать изменение входов/правил. Не удаляйте исходники для обхода проверки.

Не запускать `run_notebook.py`, `model.py` как CLI и весь старый `test_model.py` на этапе без обучения: они могут вызывать fit. Новый тестовый файл проверяет задания с блокировкой train_model/Ridge.fit.

## Доступ для следующего UI Work

```python
from pathlib import Path
from src.model.registry import read_registry

root = Path(r'D:\Projects\Veritas AI Hack')
entries = read_registry(root)['datasets']
```

Первая строка даёт удобную работу с путями. Вторая импортирует только чтение метаданных. Третья задаёт корень локальной копии. Четвёртая читает и проверяет реестр; обучение не вызывается. В UI показывать имя станции и системы раздельно. `ready_for_model_check` означает проверенные входы для следующего этапа, не готовые оценки. Только прежний Surry CW1 имеет `results_path`; у остальных `model_status=not_trained`, `results_path=null`.

## Подготовка одного задания

```python
from src.model.pipeline import prepare_job
from src.model.registry import dataset_id

identifier = dataset_id(6011, 'SYS042')
job = prepare_job(root, identifier)
```

Первая строка импортирует адаптер существующего pipeline. Вторая — безопасный способ сформировать ID. Третья выбирает конкретную систему Calvert Cliffs. Четвёртая возвращает проверенные `parts`, `features`, пути будущих результатов и ссылки на общие функции. Ни одна строка не вызывает fit. Для `review_required`, `measurements_only`, `blocked` и `reference_only` подготовка задания остановится с причиной.

Hex-суффикс ID обратим: разные `CW1`, `CW-1`, `1`, `cw1` не объединятся и не создадут опасный путь. Для человека используйте `plant_name` и `cooling_id_eia` из записи, а не hex.

## Почему готовых наборов меньше, чем кандидатов

Инвентарь определил 21 площадку/30 систем по консервативному скринингу. Этот скрининг исключал нулевые/отрицательные и необычные measured-значения. Подготовка не превращает его в молчаливую чистку: исходный measured-флаг сохраняется, а весь набор получает `review_required`, пока сомнительные месяцы не разобраны отдельно. Причину нуля/отрицательного значения не угадываем и не связываем с ошибкой будущей модели.

Итог: 17 систем готовы к структурной проверке модели; 41 требуют предметного разбора; 21 доступны только как измерения; 15 заблокированы; 8 без полных пар. Это категории систем, не площадок. У одной площадки системы могут иметь разный статус.

Surry CW1: 142/24/22, прежние файлы и результаты сохранены. North Anna и Millstone остаются доступными для просмотра измерений, но их нулевые measured-значения не удалены ради допуска к новому обучению. Неполный поздний ряд Donald C Cook даёт по 12 test-месяцев, не 24; границы лет не сдвигаются.

Полный построчный разбор нового кода находится в `MULTISTATION_WALKTHROUGH.md`. Подробные причины по системе — в её audit.json и реестре.
