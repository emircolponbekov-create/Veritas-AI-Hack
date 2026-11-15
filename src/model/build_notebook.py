"""Build a standalone Colab notebook from model.py without external imports."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def build():
    cells = []

    def add(kind, source):
        cell = {"cell_type": kind, "metadata": {}, "source": source.strip().splitlines(keepends=True)}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        cell["id"] = f"model-{len(cells):02d}"
        cells.append(cell)

    add("markdown", """
# Nuclear Water & Climate Lab — Surry CW1
**Ретроспективная оценка / Retrospective estimation**, не прогноз заранее.

Цель: месячная ΔT = средняя температура сброса − средняя температура входа (°C).
Входы: температура входа того же отчётного месяца и сезон (sin/cos месяца).
Входная средняя известна после окончания месяца; публикация EIA Schedule 8D может запаздывать ещё дольше.

Train: 2010–2021. Validation: 2022–2023 (выбор alpha). Test: 2024–2025.
Используем только `eligible_measured=true`. Все scaler/медианы/коэффициенты обучаются только на train.
Test не используется для выбора. Сравниваем Ridge с общей и сезонной медианами на одинаковых месяцах.

**Запуск:** Runtime → Run all / Среда выполнения → Выполнить все; один раз выберите исходный
`surry_cw1_monthly.csv` при запросе загрузки. GPU не нужен. Результаты — в `model_output`.
Последняя необязательная ячейка скачивает ZIP с результатами.

ΔT охлаждения не равна нагреву водоёма. Нет вывода о вреде/безопасности людей или экосистемы.
Перенос Surry → Akkuyu не проверен. Credits: EIA, Catalyst Cooperative PUDL; Python,
pandas, NumPy, matplotlib, scikit-learn; ChatGPT/Codex помог написать код, команда проверяет и объясняет его.

Источники: [PUDL cooling definitions](https://data.catalyst.coop/preview/pudl/_core_eia923__monthly_cooling_system_information),
[EIA-923 instructions](https://www.eia.gov/survey/form/eia_923/instructions.pdf),
[EIA public data](https://www.eia.gov/electricity/data/eia923/).
    """)
    chunks = (HERE / "model.py").read_text(encoding="utf-8").split("# %% ")[1:]
    sections = {chunk.split("\n", 1)[0]: chunk.split("\n", 1)[1] for chunk in chunks}
    add("markdown", "## 1. Библиотеки\nВ обычном Colab они уже установлены. Если импорт не сработал, выполните `%pip install pandas matplotlib scikit-learn` в отдельной ячейке и перезапустите среду.")
    add("code", sections["imports"])
    add("markdown", "## 2. Загрузка CSV\nColab не видит папку ноутбука на Windows. Выберите файл один раз. Локально путь определяется автоматически из папки проекта.")
    add("code", '''
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    uploaded = files.upload()
    if len(uploaded) != 1:
        raise ValueError("Choose exactly one original surry_cw1_monthly.csv")
    CSV_PATH = Path(next(iter(uploaded)))
    OUTPUT_DIR = Path("model_output")
else:
    candidates = [Path.cwd(), *Path.cwd().parents]
    ROOT = next((p for p in candidates if (p / "data/surry_cw1_monthly.csv").is_file()), None)
    if ROOT is None:
        raise FileNotFoundError("Run from the project root or src/model folder")
    CSV_PATH = ROOT / "data/surry_cw1_monthly.csv"
    OUTPUT_DIR = ROOT / "data"
print("Input:", CSV_PATH, "| Output:", OUTPUT_DIR)
    ''')
    add("markdown", "## 3. Проверка данных\nПроверяем станцию, месяцы, флаги, методы, конечность температур и перевод °F → °C. При противоречии обучение останавливается. Данные не исправляются молча.")
    add("code", sections["audit helpers"])
    add("code", '''
frame, audit = audit_data(CSV_PATH)
print(json.dumps(audit, indent=2, ensure_ascii=False))
display(frame.head())
    ''')
    add("markdown", "## 4. Признаки и разделение по времени\nКалендарь известен заранее. Средняя температура входа — только после отчётного месяца. Температура сброса и ΔT используются исключительно как цель и для аудита. Cooling hours, выработка, потоки и лаги не входят в признаки. Поэтому baseline «прошлый месяц» не предполагает недоказанную оперативную доступность отчётов EIA.")
    add("code", sections["feature preparation"])
    add("code", '''
parts = prepare_splits(frame)
for name, part in parts.items():
    print(name, len(part), part.report_month.min(), "to", part.report_month.max())
print("Features:", FEATURES)
display(make_features(parts["train"]).head())
    ''')
    add("markdown", "## 5. Обучение и выбор на validation\nRidge — линейная регрессия со штрафом за большие коэффициенты. Проверяем заранее заданные alpha 0.1, 1, 10, 100. StandardScaler учится только на train. Обе медианы также только из train; после выбора модель не переобучаем на validation.")
    add("code", sections["training (does not accept test)"])
    add("code", '''
model, median, seasonal, validation_scores = train_model(parts["train"], parts["validation"])
display(validation_scores)
print("Locked alpha:", model.named_steps["ridge"].alpha)
print("Train median delta T (°C):", median)
    ''')
    add("markdown", "## 6. Финальная проверка\nТолько теперь рассчитываем ошибки на test. MAE — средняя абсолютная ошибка в °C; меньше лучше. Все методы сравниваются на одних строках. После просмотра test не менять модель ради улучшения этой метрики.")
    add("code", sections["evaluation (after selection is locked)"])
    add("code", '''
results = predict_table(parts["test"], model, median, seasonal)
test_scores = score_table(results)
display(pd.DataFrame.from_dict(test_scores, orient="index", columns=["MAE (°C)"]))
print("Test:", results.report_month.min(), "to", results.report_month.max(), "N =", len(results))
if test_scores["model_delta_t_c"] < min(test_scores[k] for k in OUTPUT_FIELDS[3:5]):
    print("Ridge has lower test MAE than both baselines on this historical holdout.")
else:
    print("Ridge does NOT beat both baselines. Report this result honestly.")
worst = results.assign(absolute_error_c=(results.model_delta_t_c-results.reported_delta_t_c).abs())
display(worst.nlargest(1, "absolute_error_c"))
    ''')
    add("markdown", "## 7. График\nПропуски на графике — месяцы с неподтверждённым методом измерения; они исключены у всех методов. Синие точки — отчётные значения, остальные линии — оценки.")
    add("code", "figure = plot_results(results)\nplt.show()")
    add("markdown", "## 8. Экспорт для UI\nКонтракт v1: один месяц на строку, только test. Колонки: `report_month`, `intake_temperature_c`, `reported_delta_t_c`, `median_baseline_delta_t_c`, `seasonal_baseline_delta_t_c`, `model_delta_t_c`. Все числовые поля в °C. UI соединяет таблицы по месяцу, не по номеру строки. JSON и отчёт содержат аудит, метрики, версии и параметры модели.")
    add("code", sections["export"])
    add("code", '''
metrics = export_outputs(OUTPUT_DIR, CSV_PATH, audit, parts, model, median,
                         seasonal, validation_scores, results, figure)
print("Saved:", OUTPUT_DIR / "results.csv")
print("Reports:", OUTPUT_DIR / "model_artifacts")
print("Input SHA-256:", metrics["input_sha256"])
    ''')
    add("markdown", "## 9. Ограничения и объяснение жюри\nМодель получает температуру воды на входе и время года и оценивает разность температур сброса и входа за уже завершившийся месяц. Проверяем её на поздних годах и сравниваем с простыми правилами. Один объект и небольшой зависимый по времени ряд не доказывают переносимость; месячные средние скрывают пики и режимы работы. Ошибка отдельного месяца может быть большой. Нет биологических данных, карты теплового шлейфа, вывода о безопасности или прогноза Аккую. Точность записи °C не означает точность измерений: источник округляет °F.")
    add("markdown", "## 10. Скачать результаты (необязательно)\nПоменяйте `DOWNLOAD_RESULTS` на `True` и выполните эту ячейку в Colab. Передайте другу results.csv, model_artifacts и этот ноутбук; исходный CSV сверяйте по SHA-256. В ZIP исходный CSV не дублируется.")
    add("code", '''
DOWNLOAD_RESULTS = False
if IN_COLAB and DOWNLOAD_RESULTS:
    from zipfile import ZipFile, ZIP_DEFLATED
    archive = Path("surry_model_results.zip")
    with ZipFile(archive, "w", ZIP_DEFLATED) as zipped:
        zipped.write(OUTPUT_DIR / "results.csv", "data/results.csv")
        for path in sorted((OUTPUT_DIR / "model_artifacts").glob("*")):
            if path.is_file():
                zipped.write(path, "data/model_artifacts/" + path.name)
    files.download(str(archive))
    ''')
    notebook = {"nbformat": 4, "nbformat_minor": 5,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "language_info": {"name": "python"}, "colab": {"provenance": []}},
                "cells": cells}
    target = HERE / "surry_model.ipynb"
    target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    build()
