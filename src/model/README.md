# Модель Surry CW1

Готовый самостоятельный ноутбук: `surry_model.ipynb`. Он включает код из `model.py` и не требует загружать Python-модуль в Colab. Исходный CSV не встроен и не продублирован.

## Запуск в Colab

1. Откройте https://colab.research.google.com/ . Выберите **File → Upload notebook / Файл → Загрузить блокнот**, затем локальный `D:\Projects\Veritas AI Hack\src\model\surry_model.ipynb`.
2. Выберите **Runtime → Run all / Среда выполнения → Выполнить все**. Обычного CPU достаточно, GPU не нужен.
3. В ячейке загрузки выберите `D:\Projects\Veritas AI Hack\data\surry_cw1_monthly.csv`. Файл выбирается один раз; остальные ячейки используют `CSV_PATH`.
4. Дождитесь метрик, графика и сообщения `Saved: model_output/results.csv`.
5. Для скачивания экспорта поменяйте в последней ячейке `DOWNLOAD_RESULTS = False` на `True` и выполните её. ZIP содержит `data/results.csv` и `data/model_artifacts/`.
6. Для переноса в общий ноутбук откройте загруженный ноутбук, выберите ячейки через **Edit → Select all cells**, скопируйте их, откройте общий Colab и вставьте после существующих ячеек. Если пункт меню отличается, выделите первую ячейку, затем последнюю с Shift и скопируйте выбранные ячейки. Сохраните Ctrl+S. Не заменяйте чужие ячейки.

Общий Colab: https://colab.research.google.com/drive/1K4F60eedk1SRdhFQFpuC0IRkaMGe3qyy . Он был прочитан (одна пустая ячейка), но не изменён: управление браузером остановилось из-за невозможности надёжно определить URL. Запуск в Colab не подтверждён.

Если библиотек нет, выполните отдельную ячейку `%pip install pandas matplotlib scikit-learn`, затем перезапустите среду и **Run all**. Ноутбук проверяет схему и остановится при противоречиях вместо подстановки значений.

## Метод

Цель — `delta_t_c`: среднемесячный сброс минус среднемесячный вход системы охлаждения. Это не температура контрольной точки ниже по течению. Подтверждение определений — [PUDL](https://data.catalyst.coop/preview/pudl/_core_eia923__monthly_cooling_system_information) и [EIA Schedule 8D](https://www.eia.gov/survey/form/eia_923/instructions.pdf). Исходные средние в °F, конверсия `(F−32)*5/9`; разность — `(F_out−F_in)*5/9`. Шесть знаков в CSV не означают такую точность измерения.

| Признак | Единица | Когда известен |
| --- | --- | --- |
| intake_temperature_c | °C | По завершении отчётного месяца, в публичном EIA позже; Schedule 8D собирается ежегодно |
| month_sin | безразмерный | Заранее, из календарного месяца |
| month_cos | безразмерный | Заранее, из календарного месяца |

`sin(2πm/12)` и `cos(2πm/12)` задают сезон. Текущие ΔT, сброс и их производные запрещены во входах. Выработка, cooling_hours, расходы и лаги не используются. Baseline «прошлый месяц» не включён, поскольку своевременный доступ к предыдущему EIA-отчёту не установлен. Вместо него используются обязательные train-медианы: общая и по календарному месяцу.

Фильтр `eligible_measured=true` дополнительно сверяется с методом измерения. Train 2010–2021, validation 2022–2023, test 2024–2025. StandardScaler и Ridge учатся только на train. Alpha выбирается из фиксированного списка 0.1, 1, 10, 100 по MAE validation. После выбора нет переобучения на validation/test. Все три метода сравниваются на одинаковых test-месяцах, без перемешивания и заполнения целей.

## Экспорт для друга / UI

Схема неизменна: `docs/work/DATA_CONTRACT.md`, v1. Локально ноутбук пишет в `data/`, в Colab — в `model_output/`.

| Поле results.csv | Смысл | Единица |
| --- | --- | --- |
| report_month | Уникальный отчётный месяц test | YYYY-MM |
| intake_temperature_c | Отчётная температура на входе | °C |
| reported_delta_t_c | Отчётная разность сброс − вход, цель | °C |
| median_baseline_delta_t_c | Общая медиана ΔT по train | °C |
| seasonal_baseline_delta_t_c | Медиана ΔT этого календарного месяца по train | °C |
| model_delta_t_c | Оценка Ridge | °C |

Соединять по `report_month`; не по позиции строки. Для исключённых месяцев оценки нет. Отчётные измерения и оценки должны иметь разные подписи. UI не обучает модель.

В `model_artifacts/`: `audit.json`, `metrics.json`, `parameters.json`, `validation_scores.csv`, `test_errors.csv`, `evaluation.md`, `test_predictions.png`. JSON параметров сохраняет scaler и коэффициенты без небезопасного pickle: `prediction = ((X - scaler_mean) / scaler_scale) @ ridge_coef + ridge_intercept`, порядок X задан `features`. Это для воспроизведения; текущий UI читает results.csv.

## Локальное воспроизведение

В обычной среде Python с установленными зависимостями, из корня проекта:

```powershell
python -m pip install pandas numpy matplotlib scikit-learn
python src/model/run_notebook.py
python -m unittest discover -s tests/model -v
```

`run_notebook.py` выполняет все code-ячейки по порядку в одном новом пространстве имён, сохраняет реальные текстовые/графические выходы в `.ipynb`. Это Python-прогон без Jupyter kernel; он не проверяет виджет загрузки Colab. Для отдельного CLI: `python src/model/model.py --csv data/surry_cw1_monthly.csv --output-dir data`.

При изменении `model.py` пересоберите ноутбук `python src/model/build_notebook.py` (его старые выходы сбросятся), затем снова выполните `run_notebook.py`. Не редактируйте логику в двух местах независимо.

## Границы доверия

Одна система, 16 лет месячных отчётов, небольшой временно зависимый test. Нет внешней проверки на другой станции, доверительных интервалов и доказательства причин. Средние скрывают пики, остановки и пространственные различия. Не использовать для медицинских, экологических или регуляторных решений; не переносить на Аккую. ΔT системы не равно нагреву всего водоёма.

Credits: EIA → Catalyst Cooperative PUDL, pandas, NumPy, matplotlib, scikit-learn; ChatGPT/Codex — помощь с кодом и проверкой. Происхождение локального снимка и результаты проверки зафиксированы в MODEL-handoff; общие SOURCES.md/LOG.md не перезаписаны.
