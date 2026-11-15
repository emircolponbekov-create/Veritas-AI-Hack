# UI: многосистемный экран — построчный разбор

Область UI, корень `D:\Projects\Veritas AI Hack`. Разбор MODEL не переписан. Реестр и данные только читаются.

Каждая непустая строка нового production-кода и новых тестов приведена дословно. Пустые строки разделяют блоки и ничего не выполняют. Многострочные выражения показаны по физическим строкам. Номера относятся к версии, SHA-256 которой указан перед таблицами.

Существующий `data_loader.py` не изменён. Из `tests/ui/test_ui.py` удалён только прежний ScreenTests, который вызывал старый двухпутевой render: он заменён многосистемными ScreenTests ниже. Пять тестов прежнего CSV-валидатора сохранены. Старый частичный export остаётся проверяемым legacy-сценарием, но новый wrapper не разрешает показывать неполную MAE.

`src/ui/requirements.txt`: добавлена строка `pyarrow==26.0.1` — фиксирует уже установленный Parquet reader, который нужен существующему MODEL-адаптеру. Остальные версии не менялись. `README.md` обновлён как инструкция запуска/ручной проверки, а не исполняемый код.

## Ограничение проверки среды

Обычный Streamlit и обычный AppTest зависли в Windows asyncio `socketpair` до исполнения UI. В изолированных тестах явный `VERITAS_UI_NO_SOCKET_TESTS=1` заменяет только неработающий конструктор неиспользуемого event loop. Widgets, чтение реальных измерений и результатов и расчёт MAE настоящие. Флаг не участвует в production. Это не подтверждает работу HTTP/WebSocket-сервера или визуальную проверку Chrome.

## src/ui/app.py

SHA-256: `a23b9e4651032dac663c98385a84e1c75670dca2dcf7cdc39564a6edf6586f3c`.

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 1 | <code>"""Read-only Streamlit UI for one registered cooling system at a time."""</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 2 | <code>import sys</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 3 | <code>from pathlib import Path</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 4 | <code>import pandas as pd</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 5 | <code>import streamlit as st</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 7 | <code>sys.path.insert(0, str(Path(__file__).resolve().parent))</code> | Добавляет локальную область импорта: Streamlit запускает файл, а MODEL расположен в соседнем пакете. |
| 8 | <code>from data_loader import history_chart, METHOD_LABELS</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 9 | <code>from multistation_loader import ROOT, registry_snapshot, measurements_snapshot, verified_results</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 11 | <code>REASONS = {</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 12 | <code>    'mixed_site_nuclear_attribution_unconfirmed': 'Mixed-site attribution to nuclear generation is unconfirmed.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 13 | <code>    'no_complete_pairs': 'No complete intake/discharge temperature pairs are available.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 14 | <code>    'no_explicit_measured_pairs': 'No pairs have an explicitly measured source method.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 15 | <code>    'suspect_measured_rows_retained_no_automatic_exclusion': 'Suspect reported measurements were retained and require review.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 16 | <code>    'cooling_scheme_semantics_require_review': 'Intake/discharge meaning for this cooling scheme requires review.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 17 | <code>    'fixed_time_coverage_insufficient': 'Insufficient coverage of the fixed train/validation/test periods.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 18 | <code>    'recirculating_mixed_or_unknown_cooling_codes': 'Recirculating, mixed or unknown cooling metadata limits interpretation.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 19 | <code>    'missing_temperatures_retained_and_ineligible': 'Missing temperatures were retained and are ineligible.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 20 | <code>    'reported_measurement_not_independent_sensor_validation': 'Source-reported measurements; no independent sensor validation.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 21 | <code>    'historical_monthly_retrospective_only_no_ecosystem_inference': 'Historical monthly records; no ecosystem conclusions.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 22 | <code>    'historical_cooling_metadata_incomplete_or_changed': 'Historical cooling metadata may be incomplete or changed.',</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 23 | <code>}</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 26 | <code>def source_panel(entry):</code> | Показывает provenance и ограничения именно выбранной системы. Даже когда температуры скрыты, причина остаётся видимой. |
| 27 | <code>    with st.expander('Source, identifiers and limitations', expanded=entry['status'] != 'ready_for_model_check'):</code> | Оформляет следующий блок экрана в отдельной области; данные остаются выбранной системы. |
| 28 | <code>        st.write(f"Dataset: {entry['dataset_id']} &#124; Data: {entry['status']} &#124; Model: {entry['model_status']}")</code> | Выводит указанный текст или метаданные выбранного набора. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 29 | <code>        st.write(f"Local observations: {entry['observations']['path']}")</code> | Выводит указанный текст или метаданные выбранного набора. |
| 30 | <code>        source = entry['provenance']</code> | Берёт источник и единицы из provenance выбранной записи. |
| 31 | <code>        st.write(f"Source table: {source['table']}")</code> | Выводит указанный текст или метаданные выбранного набора. |
| 32 | <code>        st.markdown(f"[Source snapshot URL]({source['source_url']})")</code> | Оформляет указанную подпись или ссылку на источник. |
| 33 | <code>        st.write(f"Original units: {source['source_units']}; display: {source['units']}. Celsius = (Fahrenheit - 32) × 5/9.")</code> | Выводит указанный текст или метаданные выбранного набора. |
| 34 | <code>        st.write(f"Reuse: {source['license']}")</code> | Выводит указанный текст или метаданные выбранного набора. |
| 35 | <code>        st.caption(f"Frozen source SHA-256: {source['raw_sha256']}. The nightly URL may serve a newer snapshot.")</code> | Подписывает происхождение, доступность, единицы или покрытие, чтобы числа не трактовались шире данных. |
| 36 | <code>        for reason in entry['limitations']:</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 37 | <code>            st.write('- ' + REASONS.get(reason, reason.replace('_', ' ')))</code> | Выводит указанный текст или метаданные выбранного набора. |
| 38 | <code>        if entry['review_months']:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 39 | <code>            st.write('Months requiring review (not silently removed):')</code> | Выводит указанный текст или метаданные выбранного набора. |
| 40 | <code>            st.json(entry['review_months'], expanded=False)</code> | Показывает конкретные спорные месяцы и причины из реестра. |
| 43 | <code>def model_panel(entry, measurements, month, token, root):</code> | Читает только сохранённые результаты выбранной системы. Ошибки публикации не мешают показу доступных измерений. MAE не пересекает границы систем. |
| 44 | <code>    st.subheader('Model estimate')</code> | Отделяет следующий смысловой блок экрана. |
| 45 | <code>    st.caption('Retrospective estimate, not an advance forecast. Same-month intake is known after the month; publication can lag. No training runs here.')</code> | Подписывает происхождение, доступность, единицы или покрытие, чтобы числа не трактовались шире данных. |
| 46 | <code>    if measurements is None or entry['status'] != 'ready_for_model_check' or entry['model_status'] == 'not_trained':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 47 | <code>        st.info('Model not ready')</code> | Показывает научное ограничение либо Model not ready вместо придуманной оценки. |
| 48 | <code>        return</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 49 | <code>    try:</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 50 | <code>        results, scores = verified_results(entry, measurements, token, root)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 51 | <code>    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:</code> | Перехватывает перечисленные ошибки чтения/проверки и переводит экран в явное недоступное состояние. |
| 52 | <code>        st.info('Model not ready')</code> | Показывает научное ограничение либо Model not ready вместо придуманной оценки. |
| 53 | <code>        st.warning(f'Saved results temporarily unavailable or need review: {exc}. Refresh data to retry.')</code> | Показывает понятную причину ограничения/временной недоступности. |
| 54 | <code>        return</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 55 | <code>    if month in results.index:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 56 | <code>        row = results.loc[month]</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 57 | <code>        cols = st.columns(2)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 58 | <code>        cols[0].metric('Model estimate of ΔT, °C', f'{row.model_delta_t_c:.2f}')</code> | Показывает проверенное значение текущего месяца с единицей °C и округлением для экрана. |
| 59 | <code>        cols[1].metric('Absolute error for this month, °C', f'{abs(row.model_delta_t_c - row.reported_delta_t_c):.2f}')</code> | Показывает проверенное значение текущего месяца с единицей °C и округлением для экрана. |
| 60 | <code>    else:</code> | Обрабатывает оставшийся вариант предыдущего условия; отдельный блок не подменяет другие состояния. |
| 61 | <code>        st.info('No model estimate for this month')</code> | Показывает научное ограничение либо Model not ready вместо придуманной оценки. |
| 62 | <code>    st.markdown('**Held-out test comparison for this system**')</code> | Оформляет указанную подпись или ссылку на источник. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 63 | <code>    st.caption(f'{len(results)} identical eligible test months: {results.index.min()} to {results.index.max()}. MAE recalculated from CSV; lower is better. Baselines: train 2010–2021 only. Model selection: validation 2022–2023.')</code> | Подписывает происхождение, доступность, единицы или покрытие, чтобы числа не трактовались шире данных. |
| 64 | <code>    st.dataframe(pd.DataFrame({'Method': list(METHOD_LABELS.values()),</code> | Показывает три пересчитанные MAE с числом одинаковых тестовых месяцев. |
| 65 | <code>                              'MAE (°C)': [scores[field] for field in METHOD_LABELS],</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 66 | <code>                              'Test months': len(results)}), hide_index=True, width='stretch',</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 67 | <code>                 column_config={'MAE (°C)': st.column_config.NumberColumn(format='%.3f')})</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 68 | <code>    difference = scores['model_delta_t_c'] - min(scores['median_baseline_delta_t_c'], scores['seasonal_baseline_delta_t_c'])</code> | Сравнивает MAE модели с минимумом двух baseline этой же системы. |
| 69 | <code>    comparison = 'worse' if difference &gt; 0 else 'better'</code> | Выбирает честную подпись лучше/хуже, не обещая улучшения. |
| 70 | <code>    st.write(f'Model MAE is {comparison} than the best simple baseline by {abs(difference):.3f} °C.' if difference else 'Model MAE equals the best simple baseline.')</code> | Выводит указанный текст или метаданные выбранного набора. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 71 | <code>    chart = results[['reported_delta_t_c', *METHOD_LABELS]].copy()</code> | Готовит график для одной системы и оставляет отсутствующие месяцы разрывами. |
| 72 | <code>    chart.index = pd.to_datetime(chart.index)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 73 | <code>    chart = chart.reindex(pd.date_range(chart.index.min(), chart.index.max(), freq='MS'))</code> | Готовит график для одной системы и оставляет отсутствующие месяцы разрывами. |
| 74 | <code>    st.line_chart(chart.rename(columns={'reported_delta_t_c': 'Reported measurement', **METHOD_LABELS}),</code> | Строит график выбранной системы, без интерполяции отсутствующих месяцев. |
| 75 | <code>                  x_label='Test month', y_label='Cooling-system ΔT (°C)', height=260)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 78 | <code>def render(root=ROOT):</code> | Собирает экран, перечитывает реестр и хранит выбор месяца отдельно для каждого dataset_id. Функция не вызывает fit или подготовку файлов. |
| 79 | <code>    st.set_page_config(page_title='Nuclear Water & Climate Lab', page_icon='💧', layout='wide')</code> | Задаёт английское название страницы и широкую компоновку. |
| 80 | <code>    st.title('Nuclear Water & Climate Lab')</code> | Выводит название проекта. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 81 | <code>    st.write('Explore historical cooling-water measurements and saved retrospective estimates for one cooling system at a time.')</code> | Выводит указанный текст или метаданные выбранного набора. |
| 82 | <code>    st.info('ΔT = discharge temperature − intake temperature across the cooling system. It is not the heating of the whole water body.')</code> | Показывает научное ограничение либо Model not ready вместо придуманной оценки. |
| 83 | <code>    st.button('Refresh data', help='Reread registry, observations and saved results. No training is performed.')</code> | Создаёт Refresh data: нажатие вызывает обычный rerun, без обучения и кэшированных данных. |
| 84 | <code>    try:</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 85 | <code>        registry, token = registry_snapshot(root)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 86 | <code>    except (OSError, ValueError, KeyError, TypeError) as exc:</code> | Перехватывает перечисленные ошибки чтения/проверки и переводит экран в явное недоступное состояние. |
| 87 | <code>        st.error(f'Registry temporarily unavailable: {exc}. Refresh data to retry.')</code> | Заметно выделяет необходимость проверки данных или недоступность реестра. |
| 88 | <code>        return</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 89 | <code>    entries = registry['datasets']</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 90 | <code>    plants = {e['plant_id_eia']: e['plant_name'] for e in entries}</code> | Берёт названия площадок и EIA ID из реестра без угадывания по имени CSV. |
| 91 | <code>    ids = sorted(plants, key=lambda plant: (plants[plant], plant))</code> | Упорядочивает площадки для устойчивого выбора, сохраняя идентификаторы. |
| 92 | <code>    if not ids:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 93 | <code>        st.warning('No registered systems are available.')</code> | Показывает понятную причину ограничения/временной недоступности. |
| 94 | <code>        return</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 95 | <code>    plant_id = st.selectbox('Plant site', ids, index=ids.index(3806) if 3806 in ids else 0,</code> | Создаёт выбор площадки; при первом открытии выбирает EIA 3806. |
| 96 | <code>                            format_func=lambda plant: f'{plants[plant]} — EIA {plant}', key='plant')</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 97 | <code>    systems = sorted([e for e in entries if e['plant_id_eia'] == plant_id], key=lambda e: e['cooling_id_eia'])</code> | Оставляет в выборе системы только выбранной площадки. |
| 98 | <code>    system_ids = [e['dataset_id'] for e in systems]</code> | Передаёт виджету уникальные dataset_id вместо неоднозначных названий. |
| 99 | <code>    default = next((i for i, e in enumerate(systems) if plant_id == 3806 and e['cooling_id_eia'] == 'CW1'), 0)</code> | Для Surry явно предпочитает CW1, иначе первую существующую систему. |
| 100 | <code>    identifier = st.selectbox('Cooling system', system_ids, index=default,</code> | Выбирает систему с отдельным ключом состояния для каждой площадки. |
| 101 | <code>                              format_func=lambda value: next(e['cooling_id_eia'] for e in systems if e['dataset_id'] == value),</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 102 | <code>                              key=f'system_{plant_id}')</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 103 | <code>    entry = next(e for e in systems if e['dataset_id'] == identifier)</code> | Находит запись строго выбранного dataset_id, чтобы источник и модель не смешались. |
| 104 | <code>    st.caption(f"WATER IMPACT · {entry['plant_name']} · EIA {plant_id} / {entry['cooling_id_eia']}")</code> | Подписывает происхождение, доступность, единицы или покрытие, чтобы числа не трактовались шире данных. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 105 | <code>    source_panel(entry)</code> | Вызывает соответствующую область экрана с записью и измерениями именно выбранной системы. |
| 106 | <code>    measurements = None</code> | Хранит только текущую таблицу; при ошибке остаётся None и модель скрыта. |
| 107 | <code>    month = None</code> | Выбирает исторический месяц; ключ виджета включает dataset_id. |
| 108 | <code>    if entry['status'] in {'blocked', 'reference_only'}:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 109 | <code>        st.warning('Temperature data unavailable for confirmed measurement display. See reasons above; no numbers are substituted.')</code> | Показывает понятную причину ограничения/временной недоступности. |
| 110 | <code>    elif entry['status'] == 'review_required':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 111 | <code>        st.error('Data review required. Unresolved suspect measurements: temperature cards and model comparisons are withheld pending review.')</code> | Заметно выделяет необходимость проверки данных или недоступность реестра. |
| 112 | <code>    else:</code> | Обрабатывает оставшийся вариант предыдущего условия; отдельный блок не подменяет другие состояния. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 113 | <code>        try:</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 114 | <code>            measurements, audit = measurements_snapshot(entry, token, root)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 115 | <code>        except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:</code> | Перехватывает перечисленные ошибки чтения/проверки и переводит экран в явное недоступное состояние. |
| 116 | <code>            st.warning(f'Measured data temporarily unavailable or need review: {exc}. Refresh data to retry.')</code> | Показывает понятную причину ограничения/временной недоступности. |
| 117 | <code>        else:</code> | Обрабатывает оставшийся вариант предыдущего условия; отдельный блок не подменяет другие состояния. |
| 118 | <code>            if measurements.empty:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 119 | <code>                st.warning('No eligible measured temperature pairs are available.')</code> | Показывает понятную причину ограничения/временной недоступности. |
| 120 | <code>            else:</code> | Обрабатывает оставшийся вариант предыдущего условия; отдельный блок не подменяет другие состояния. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 121 | <code>                months = measurements.report_month.tolist()</code> | Берёт доступные месяцы из измерений именно текущей системы. |
| 122 | <code>                month = st.selectbox('Historical reporting month', months, index=len(months) - 1, key=f'month_{identifier}')</code> | Выбирает исторический месяц; ключ виджета включает dataset_id. |
| 123 | <code>                row = measurements.set_index('report_month').loc[month]</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 124 | <code>                st.caption('Source-reported measured monthly averages · °C')</code> | Подписывает происхождение, доступность, единицы или покрытие, чтобы числа не трактовались шире данных. |
| 125 | <code>                for col, label, field in zip(st.columns(3), ['Intake temperature, °C', 'Discharge temperature, °C', 'Reported ΔT, °C'],</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 126 | <code>                                            ['intake_temperature_c', 'discharge_temperature_c', 'reported_delta_t_c']):</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 127 | <code>                    col.metric(label, f'{row[field]:.2f}')</code> | Показывает проверенное значение текущего месяца с единицей °C и округлением для экрана. |
| 128 | <code>                st.subheader('Historical reported ΔT')</code> | Отделяет следующий смысловой блок экрана. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 129 | <code>                st.line_chart(history_chart(measurements).rename(columns={'reported_delta_t_c': 'Reported measurement'}),</code> | Строит график выбранной системы, без интерполяции отсутствующих месяцев. |
| 130 | <code>                              x_label='Reporting month', y_label='Cooling-system ΔT (°C)', height=280)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 131 | <code>                st.caption(f"{audit['eligible']} eligible months out of {audit['total']} rows. Gaps are unavailable/excluded months, not zero. Rounding does not imply sensor precision.")</code> | Подписывает происхождение, доступность, единицы или покрытие, чтобы числа не трактовались шире данных. |
| 132 | <code>                with st.expander('Excluded months and split coverage'):</code> | Оформляет следующий блок экрана в отдельной области; данные остаются выбранной системы. |
| 133 | <code>                    st.write(', '.join(audit['excluded']) or 'None')</code> | Выводит указанный текст или метаданные выбранного набора. |
| 134 | <code>                    st.write(entry['split_counts'])</code> | Выводит указанный текст или метаданные выбранного набора. |
| 135 | <code>    model_panel(entry, measurements, month, token, root)</code> | Вызывает соответствующую область экрана с записью и измерениями именно выбранной системы. |
| 136 | <code>    left, right = st.columns(2)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 137 | <code>    with left:</code> | Ограничивает область действия указанного контекста или тестовой подмены. |
| 138 | <code>        st.subheader('What we know')</code> | Отделяет следующий смысловой блок экрана. |
| 139 | <code>        st.write('Eligible records describe source-reported monthly intake and discharge temperatures for the selected system. Saved estimates are checked against that system and its test months.')</code> | Выводит указанный текст или метаданные выбранного набора. |
| 140 | <code>    with right:</code> | Ограничивает область действия указанного контекста или тестовой подмены. |
| 141 | <code>        st.subheader("What we don't know")</code> | Отделяет следующий смысловой блок экрана. |
| 142 | <code>        st.write('These records cannot establish harm or safety for people, animals or plants. Monthly averages do not describe local peaks, mixing or downstream temperatures. Results do not automatically apply to Akkuyu or another system. This is not an environmental safety ranking.')</code> | Выводит указанный текст или метаданные выбранного набора. |
| 145 | <code>if __name__ == '__main__':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 146 | <code>    render()</code> | Запускает сборку экрана; обучения в этой функции нет. |

## src/ui/multistation_loader.py

SHA-256: `df45f3a8316d9cb9f68a0082937d28436b8cad80d2b8fa5dc7a9ed8476156881`.

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 1 | <code>"""Read-only UI snapshots using the MODEL registry reader and observation adapter."""</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 2 | <code>import json</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 3 | <code>from pathlib import Path</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 4 | <code>import sys</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 6 | <code>import numpy as np</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 8 | <code>ROOT = Path(__file__).resolve().parents[2]</code> | Определяет абсолютный корень по расположению файла, чтобы команда работала независимо от текущей папки. |
| 9 | <code>sys.path.insert(0, str(ROOT))</code> | Добавляет локальную область импорта: Streamlit запускает файл, а MODEL расположен в соседнем пакете. |
| 10 | <code>from src.model.registry import REGISTRY_PATH, project_path, read_registry, sha256</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 11 | <code>from src.model.datasets import load_observations</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 12 | <code>from data_loader import DataError, load_results, require</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 15 | <code>def registry_snapshot(root=ROOT):</code> | Через существующий reader получает одну версию реестра. Проверка полного набора файлов отключена здесь: выбранный адаптер проверяет собственные входы, поэтому чужая недоступная система не блокирует весь UI. |
| 16 | <code>    """No UI cache: each rerun observes an atomic registry version."""</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 17 | <code>    path = project_path(root, REGISTRY_PATH)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 18 | <code>    token = sha256(path)</code> | Сохраняет SHA-256 версии реестра для проверки согласованности последующих чтений. |
| 19 | <code>    registry = read_registry(root, verify=False)</code> | Читает структуру реестра существующим MODEL reader без обучения. |
| 20 | <code>    require(sha256(path) == token, "Registry changed while reading. Refresh data.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 21 | <code>    return registry, token</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 24 | <code>def current(root, token):</code> | Проверяет, что MODEL не заменил реестр во время операции чтения. При смене версии прекращает показ модели до следующего Refresh. |
| 25 | <code>    require(sha256(project_path(root, REGISTRY_PATH)) == token,</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 26 | <code>            "Registry updated during this read. Refresh data to use the new version.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 29 | <code>def measurements_snapshot(entry, token, root=ROOT):</code> | Вызывает существующий MODEL-адаптер: единицы, исходный Parquet, идентификаторы и eligibility проверяет он. UI сверяет размеры с реестром и отбирает только eligible-строки в памяти. |
| 30 | <code>    """Delegate units, eligibility, raw provenance and identity checks to MODEL."""</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 31 | <code>    current(root, token)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 32 | <code>    frame = load_observations(root, entry)</code> | Получает канонические измерения через существующий адаптер; подготовка Parquet не дублируется. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 33 | <code>    current(root, token)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 34 | <code>    require(len(frame) == entry['rows'], "Observation count disagrees with registry.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 35 | <code>    selected = frame.loc[frame.eligible_measured].copy()</code> | Создаёт отдельную таблицу только eligible-измерений, исходные строки не меняются. |
| 36 | <code>    require(len(selected) == entry['eligible_rows'], "Eligibility count disagrees with registry.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 37 | <code>    counts = {name: int(selected.split.eq(name).sum()) for name in entry['split_counts']}</code> | Считает фактические размеры временных частей для сверки с реестром. |
| 38 | <code>    require(counts == entry['split_counts'], "Split counts disagree with registry.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 39 | <code>    selected['reported_delta_t_c'] = selected.delta_t_c</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 40 | <code>    return selected, {'total': len(frame), 'eligible': len(selected),</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 41 | <code>                      'excluded': frame.loc[~frame.eligible_measured, 'report_month'].tolist()}</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 44 | <code>def verified_results(entry, measurements, token, root=ROOT):</code> | Проверяет статус, принадлежность, полное покрытие test, train-only медианы, SHA-256 и три сохранённых MAE. Ничего не обучает и не записывает. |
| 45 | <code>    """Verify a complete per-system export, train baselines and saved metrics."""</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 46 | <code>    require(entry['status'] == 'ready_for_model_check', "Dataset is not cleared for model display.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 47 | <code>    require(entry['model_status'] in {'existing_verified', 'evaluated_verified'}</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 48 | <code>            and entry['results_path'], "No verified model export is registered.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 49 | <code>    current(root, token)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 50 | <code>    require(entry['results_path'] == entry['artifacts']['future_results_path'],</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 51 | <code>            "Registered result destination disagrees with this system.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 52 | <code>    result_path = project_path(root, entry['results_path'])</code> | Разрешает зарегистрированный путь результата безопасно внутри корня проекта. |
| 53 | <code>    artifact_dir = entry['artifacts']['future_artifacts_dir']</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 54 | <code>    metrics_path = project_path(root, artifact_dir + '/metrics.json')</code> | Определяет отдельный файл метрик выбранной системы. |
| 55 | <code>    paths = [result_path, metrics_path]</code> | Собирает файлы одной публикации для проверки до и после чтения. |
| 56 | <code>    evaluation = entry.get('evaluation')</code> | Берёт из реестра метаданные завершённой оценки; отсутствие не подменяется числами. |
| 57 | <code>    if entry['model_status'] == 'evaluated_verified':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 58 | <code>        require(bool(evaluation), "Verified evaluation metadata is missing.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 59 | <code>        require(evaluation['metrics_path'] == artifact_dir + '/metrics.json', "Metrics path mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 60 | <code>        require(evaluation['verification_path'] == artifact_dir + '/verification.json', "Verification path mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 61 | <code>        paths.append(project_path(root, evaluation['verification_path']))</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 62 | <code>    hashes = {path: sha256(path) for path in paths}</code> | Фиксирует содержимое файлов до чтения, чтобы обнаружить одновременную замену. |
| 63 | <code>    results, missing = load_results(measurements, result_path)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 64 | <code>    require(not missing, "Incomplete export: some eligible test months are missing.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 65 | <code>    metrics = json.loads(metrics_path.read_text(encoding='utf-8'))</code> | Читает сохранённые метрики; это не запуск модели. |
| 66 | <code>    require(metrics['input_sha256'] == entry['observations']['sha256'], "Metrics source hash mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 67 | <code>    require(metrics['test_months'] == results.index.tolist(), "Metrics test months mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 68 | <code>    require(metrics['split']['test']['n'] == len(results), "Metrics test count mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 69 | <code>    train = measurements.loc[measurements.split.eq('train')]</code> | Отбирает только 2010–2021 для независимой проверки медиан. |
| 70 | <code>    seasonal = train.groupby(train.date.dt.month).reported_delta_t_c.median()</code> | Считает медиану каждого календарного месяца только на train. |
| 71 | <code>    expected = {'median_baseline_delta_t_c': np.repeat(train.reported_delta_t_c.median(), len(results)),</code> | Строит ожидаемые оценки двух простых методов из train для тех же test-месяцев. |
| 72 | <code>                'seasonal_baseline_delta_t_c': [seasonal.loc[int(month[-2:])] for month in results.index]}</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 73 | <code>    for field, values in expected.items():</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 74 | <code>        require(np.allclose(results[field], values, atol=1.1e-6, rtol=0), "Train-only baseline mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 75 | <code>    scores = {field: float((results[field] - results.reported_delta_t_c).abs().mean())</code> | Пересчитывает среднюю абсолютную ошибку по одинаковым строкам результатов. |
| 76 | <code>              for field in [*expected, 'model_delta_t_c']}</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 77 | <code>    for field, value in scores.items():</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 78 | <code>        require(np.isclose(value, metrics['test_mae_c'][field], atol=1.1e-6, rtol=0), "Saved MAE mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 79 | <code>    if evaluation:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 80 | <code>        identity = {field: entry[field] for field in ['dataset_id', 'plant_id_eia', 'cooling_id_eia']}</code> | Формирует точный dataset_id и пару plant/system для проверки принадлежности артефактов. |
| 81 | <code>        verification = json.loads(paths[-1].read_text(encoding='utf-8'))</code> | Читает сохранённое независимое подтверждение экспорта выбранной системы. |
| 82 | <code>        require(metrics['identity'] == identity and verification['identity'] == identity,</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 83 | <code>                "Model artifacts belong to another system.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 84 | <code>        require(verification['verified'] is True, "Independent verification is not successful.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 85 | <code>        require(verification['test_n'] == len(results), "Verification test count mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 86 | <code>        require(hashes[result_path] == evaluation['results_sha256'], "Result hash mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 87 | <code>        require(hashes[metrics_path] == verification['artifact_sha256']['model_artifacts/metrics.json'],</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 88 | <code>                "Verified metrics hash mismatch.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 89 | <code>        require(hashes[result_path] == verification['artifact_sha256']['results.csv'],</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 90 | <code>                "Verified result hash mismatch.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 91 | <code>        require(evaluation['test_n'] == len(results), "Registry test count mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 92 | <code>        for field, value in scores.items():</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 93 | <code>            require(np.isclose(value, evaluation['mae_c'][field], atol=1.1e-6, rtol=0), "Registry MAE mismatch.")</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 94 | <code>            require(np.isclose(value, verification['independent_csv_mae_c'][field], atol=1.1e-6, rtol=0),</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 95 | <code>                    "Independent verification MAE mismatch.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 96 | <code>    else:</code> | Обрабатывает оставшийся вариант предыдущего условия; отдельный блок не подменяет другие состояния. |
| 97 | <code>        require(entry['plant_id_eia'] == 3806 and entry['cooling_id_eia'] == 'CW1'</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 98 | <code>                and entry['results_path'] == 'data/results.csv', "Unrecognized legacy model identity.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 99 | <code>    require(all(sha256(path) == digest for path, digest in hashes.items()),</code> | Проверяет явно записанное условие; при несоответствии останавливает показ неподтверждённого результата с объяснением. |
| 100 | <code>            "Model files changed during this read. Refresh data.")</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 101 | <code>    current(root, token)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 102 | <code>    return results, scores</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |

## tests/ui/test_multistation.py

SHA-256: `137333eefc18599a62fb861ca1d267a231ad6ac98a1ef0852627ffacaec24f67`.

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 1 | <code>"""Read-only integration, artifact races and Streamlit selection regressions."""</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 2 | <code>from copy import deepcopy</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 3 | <code>import asyncio</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 4 | <code>import os</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 5 | <code>from pathlib import Path</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 6 | <code>import sys</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 7 | <code>import tempfile</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 8 | <code>import unittest</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 9 | <code>from unittest.mock import MagicMock, patch</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 11 | <code>ROOT = Path(__file__).resolve().parents[2]</code> | Определяет абсолютный корень по расположению файла, чтобы команда работала независимо от текущей папки. |
| 12 | <code>sys.path.insert(0, str(ROOT / 'src/ui'))</code> | Добавляет локальную область импорта: Streamlit запускает файл, а MODEL расположен в соседнем пакете. |
| 13 | <code>from multistation_loader import registry_snapshot, measurements_snapshot, verified_results</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 14 | <code>from data_loader import DataError</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 17 | <code>class SnapshotTests(unittest.TestCase):</code> | Группирует автоматические проверки, отделяя проверку данных от проверки экрана. |
| 18 | <code>    @classmethod</code> | Запускает общую подготовку тестовых ссылок один раз на класс. |
| 19 | <code>    def setUpClass(cls):</code> | Один раз читает фактический реестр и находит Surry/Calvert по внутренним идентификаторам для независимых проверок. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 20 | <code>        cls.registry, cls.token = registry_snapshot()</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 21 | <code>        cls.surry = next(e for e in cls.registry['datasets'] if e['plant_id_eia'] == 3806 and e['cooling_id_eia'] == 'CW1')</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 22 | <code>        cls.calvert = next(e for e in cls.registry['datasets'] if e['plant_id_eia'] == 6011)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 24 | <code>    def test_all_seventeen_saved_models(self):</code> | Проверяет все 17 допущенных систем на настоящих локальных измерениях и сохранённых результатах; обучения нет. |
| 25 | <code>        entries = [e for e in self.registry['datasets'] if e['status'] == 'ready_for_model_check']</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 26 | <code>        self.assertEqual(len(entries), 17)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 27 | <code>        for entry in entries:</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 28 | <code>            with self.subTest(dataset=entry['dataset_id']):</code> | Ограничивает область действия указанного контекста или тестовой подмены. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 29 | <code>                measurements, _ = measurements_snapshot(entry, self.token)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 30 | <code>                result, scores = verified_results(entry, measurements, self.token)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 31 | <code>                self.assertEqual(len(result), entry['split_counts']['test'])</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 32 | <code>                self.assertGreaterEqual(scores['model_delta_t_c'], 0)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 34 | <code>    def test_registry_changed_mid_read(self):</code> | Проверяет отказ при устаревшем токене реестра. |
| 35 | <code>        with self.assertRaisesRegex(DataError, 'Registry updated'):</code> | Требует именно ожидаемую ошибку в негативном сценарии, а не молчаливое принятие данных. |
| 36 | <code>            measurements_snapshot(self.surry, 'stale')</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 38 | <code>    def test_missing_corrupt_and_foreign_export(self):</code> | Проверяет неверный хеш, путь другой системы и временно отсутствующий файл, не меняя настоящих артефактов. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 39 | <code>        measured, _ = measurements_snapshot(self.calvert, self.token)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 40 | <code>        entry = deepcopy(self.calvert)</code> | Находит запись строго выбранного dataset_id, чтобы источник и модель не смешались. |
| 41 | <code>        entry['evaluation']['results_sha256'] = 'wrong'</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 42 | <code>        with self.assertRaisesRegex(DataError, 'Result hash'):</code> | Требует именно ожидаемую ошибку в негативном сценарии, а не молчаливое принятие данных. |
| 43 | <code>            verified_results(entry, measured, self.token)</code> | Запускает независимую проверку сохранённого экспорта, не обучение. |
| 44 | <code>        entry = deepcopy(self.calvert)</code> | Находит запись строго выбранного dataset_id, чтобы источник и модель не смешались. |
| 45 | <code>        entry['results_path'] = 'data/results.csv'</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 46 | <code>        with self.assertRaisesRegex(DataError, 'destination'):</code> | Требует именно ожидаемую ошибку в негативном сценарии, а не молчаливое принятие данных. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 47 | <code>            verified_results(entry, measured, self.token)</code> | Запускает независимую проверку сохранённого экспорта, не обучение. |
| 48 | <code>        with patch('multistation_loader.sha256', side_effect=FileNotFoundError('temporarily missing')):</code> | Временно подменяет только указанную зависимость теста; после блока восстанавливает её, настоящие файлы не меняет. |
| 49 | <code>            with self.assertRaises(FileNotFoundError):</code> | Требует именно ожидаемую ошибку в негативном сценарии, а не молчаливое принятие данных. |
| 50 | <code>                verified_results(self.calvert, measured, self.token)</code> | Запускает независимую проверку сохранённого экспорта, не обучение. |
| 52 | <code>    def test_result_replaced_during_read(self):</code> | Имитирует смену хеша файла между двумя чтениями и требует остановки сравнения. |
| 53 | <code>        measured, _ = measurements_snapshot(self.calvert, self.token)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 54 | <code>        from multistation_loader import sha256</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 55 | <code>        counts = {}</code> | Считает фактические размеры временных частей для сверки с реестром. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 56 | <code>        def changing_hash(path):</code> | Возвращает правильный хеш при первом чтении и другой при повторном, воспроизводя гонку файлов. |
| 57 | <code>            text = str(path)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 58 | <code>            counts[text] = counts.get(text, 0) + 1</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 59 | <code>            return 'changed' if text.endswith('results.csv') and counts[text] &gt; 1 else sha256(path)</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 60 | <code>        with patch('multistation_loader.sha256', side_effect=changing_hash):</code> | Временно подменяет только указанную зависимость теста; после блока восстанавливает её, настоящие файлы не меняет. |
| 61 | <code>            with self.assertRaisesRegex(DataError, 'changed during'):</code> | Требует именно ожидаемую ошибку в негативном сценарии, а не молчаливое принятие данных. |
| 62 | <code>                verified_results(self.calvert, measured, self.token)</code> | Запускает независимую проверку сохранённого экспорта, не обучение. |
| 64 | <code>    def test_incomplete_export_withholds_comparison(self):</code> | Проверяет, что отсутствующий подходящий test-месяц блокирует MAE вместо сравнения неполного экспорта. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 65 | <code>        measured, _ = measurements_snapshot(self.calvert, self.token)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 66 | <code>        with patch('multistation_loader.load_results', return_value=(None, ['2024-01'])):</code> | Временно подменяет только указанную зависимость теста; после блока восстанавливает её, настоящие файлы не меняет. |
| 67 | <code>            with self.assertRaisesRegex(DataError, 'Incomplete export'):</code> | Требует именно ожидаемую ошибку в негативном сценарии, а не молчаливое принятие данных. |
| 68 | <code>                verified_results(self.calvert, measured, self.token)</code> | Запускает независимую проверку сохранённого экспорта, не обучение. |
| 71 | <code>class ScreenTests(unittest.TestCase):</code> | Группирует автоматические проверки, отделяя проверку данных от проверки экрана. |
| 72 | <code>    def setUp(self):</code> | Только тесты: явный флаг среды позволяет заменить неработающий в текущем исполнителе socketpair на неиспользуемый event loop. При обычном запуске подмены нет. |
| 73 | <code>        if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 74 | <code>            def nonrunning_loop():</code> | Создаёт только тестовую заглушку интерфейса AbstractEventLoop, не меняя production-код. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 75 | <code>                loop = MagicMock(spec=asyncio.AbstractEventLoop)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 76 | <code>                loop.is_closed.return_value = False</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 77 | <code>                return loop</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 78 | <code>            factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop',</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 79 | <code>                            side_effect=nonrunning_loop)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 80 | <code>            factory.start()</code> | Включает тестовую подмену или гарантирует её отмену после проверки. |
| 81 | <code>            self.addCleanup(factory.stop)</code> | Включает тестовую подмену или гарантирует её отмену после проверки. |
| 83 | <code>    def screen(self, overrides=None):</code> | Создаёт настоящий Streamlit AppTest, подменяя только отдельные поля копии реестра для сценария отсутствующего результата. Источники на диске остаются прежними. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 84 | <code>        from streamlit.testing.v1 import AppTest</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 85 | <code>        script = f'''</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 86 | <code>import sys</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 87 | <code>sys.path.insert(0, {str(ROOT / 'src/ui')!r})</code> | Добавляет локальную область импорта: Streamlit запускает файл, а MODEL расположен в соседнем пакете. |
| 88 | <code>import app</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 89 | <code>from unittest.mock import patch</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 90 | <code>real = app.registry_snapshot</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 91 | <code>def snapshot(root):</code> | Определяет отдельную функцию для указанного шага; вызов расположен ниже. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 92 | <code>    registry, token = real(root)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 93 | <code>    for entry in registry['datasets']:</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 94 | <code>        if entry['plant_id_eia'] == 6011:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 95 | <code>            entry.update({overrides or {}!r})</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 96 | <code>    return registry, token</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 97 | <code>with patch.object(app, 'registry_snapshot', snapshot):</code> | Временно подменяет только указанную зависимость теста; после блока восстанавливает её, настоящие файлы не меняет. |
| 98 | <code>    app.render()</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 99 | <code>'''</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 100 | <code>        screen = AppTest.from_string(script).run(timeout=30)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 101 | <code>        self.assertFalse(screen.exception, str(screen.exception))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 102 | <code>        return screen</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 104 | <code>    def switch(self, screen, plant):</code> | Выбирает площадку через реальный виджет AppTest, выполняет rerun и требует отсутствия исключения. |
| 105 | <code>        screen.selectbox[0].select(plant).run(timeout=30)</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |
| 106 | <code>        self.assertFalse(screen.exception, str(screen.exception))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 107 | <code>        return screen</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 109 | <code>    def test_surry_default_switch_system_and_refresh(self):</code> | Проверяет Surry по умолчанию, Calvert, Refresh, ограниченную CW2 и возврат к CW1 без чужих чисел. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 110 | <code>        screen = self.screen()</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 111 | <code>        self.assertEqual(screen.selectbox[0].value, 3806)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 112 | <code>        self.assertEqual(screen.selectbox[1].value, 'eia_3806_435731')</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 113 | <code>        self.assertEqual(screen.metric[2].value, '6.67')</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 114 | <code>        self.assertEqual(screen.metric[3].value, '11.03')</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 115 | <code>        self.switch(screen, 6011)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 116 | <code>        self.assertEqual(screen.selectbox[1].value, 'eia_6011_535953303432')</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 117 | <code>        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [24]*3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 118 | <code>        self.assertTrue(any('worse' in x.value for x in screen.markdown))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 119 | <code>        screen.button[0].click().run(timeout=30)</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |
| 120 | <code>        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [24]*3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 121 | <code>        self.switch(screen, 3806)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 122 | <code>        screen.selectbox[1].select('eia_3806_435732').run(timeout=30)</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |
| 123 | <code>        self.assertFalse(screen.exception)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 124 | <code>        self.assertEqual(len(screen.metric), 0)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 125 | <code>        self.assertTrue(any(x.value == 'Model not ready' for x in screen.info))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 126 | <code>        screen.selectbox[1].select('eia_3806_435731').run(timeout=30)</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |
| 127 | <code>        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [22]*3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 129 | <code>    def test_valid_measurements_without_model(self):</code> | Проверяет отдельное состояние пригодных измерений при ещё не опубликованной модели. |
| 130 | <code>        screen = self.switch(self.screen({'model_status': 'not_trained', 'results_path': None}), 6011)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 131 | <code>        self.assertEqual(len(screen.metric), 3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 132 | <code>        self.assertTrue(any(x.value == 'Model not ready' for x in screen.info))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 133 | <code>        self.assertEqual(len(screen.dataframe), 0)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 135 | <code>    def test_refresh_observes_newly_published_model(self):</code> | В рамках одного сеанса имитирует публикацию модели между rerun: сначала три карточки измерений, затем пять карточек и MAE на 24 месяцах. Доказывает, что отсутствие модели не застревает в кэше. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 136 | <code>        from streamlit.testing.v1 import AppTest</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 137 | <code>        script = f'''</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 138 | <code>import sys</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 139 | <code>sys.path.insert(0, {str(ROOT / 'src/ui')!r})</code> | Добавляет локальную область импорта: Streamlit запускает файл, а MODEL расположен в соседнем пакете. |
| 140 | <code>import app</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 141 | <code>import streamlit as st</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 142 | <code>from unittest.mock import patch</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 143 | <code>real = app.registry_snapshot</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 144 | <code>def snapshot(root):</code> | Определяет отдельную функцию для указанного шага; вызов расположен ниже. |
| 145 | <code>    registry, token = real(root)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 146 | <code>    if not st.session_state.get('fixture_published', False):</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 147 | <code>        for entry in registry['datasets']:</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 148 | <code>            if entry['plant_id_eia'] == 6011:</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 149 | <code>                entry.update(model_status='not_trained', results_path=None)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 150 | <code>    return registry, token</code> | Возвращает явно указанный результат либо завершает ветку без дальнейшего отображения. |
| 151 | <code>with patch.object(app, 'registry_snapshot', snapshot):</code> | Временно подменяет только указанную зависимость теста; после блока восстанавливает её, настоящие файлы не меняет. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 152 | <code>    app.render()</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 153 | <code>'''</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 154 | <code>        screen = AppTest.from_string(script).run(timeout=30)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 155 | <code>        self.switch(screen, 6011)</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 156 | <code>        self.assertEqual(len(screen.metric), 3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 157 | <code>        self.assertEqual(len(screen.dataframe), 0)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 158 | <code>        screen.session_state['fixture_published'] = True</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |
| 159 | <code>        screen.button[0].click().run(timeout=30)</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 160 | <code>        self.assertFalse(screen.exception)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 161 | <code>        self.assertEqual(len(screen.metric), 5)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 162 | <code>        self.assertEqual(screen.dataframe[0].value['Test months'].tolist(), [24]*3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 164 | <code>    def test_each_restricted_status(self):</code> | На реальных записях проверяет все четыре ограниченных статуса и отсутствие неподтверждённых чисел. |
| 165 | <code>        registry, _ = registry_snapshot()</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 166 | <code>        for status in ['review_required', 'blocked', 'reference_only', 'measurements_only']:</code> | Повторяет проверку или вывод только для перечисленных элементов текущего набора. |
| 167 | <code>            entry = next(e for e in registry['datasets'] if e['status'] == status)</code> | Находит запись строго выбранного dataset_id, чтобы источник и модель не смешались. |
| 168 | <code>            with self.subTest(status=status):</code> | Ограничивает область действия указанного контекста или тестовой подмены. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 169 | <code>                screen = self.switch(self.screen(), entry['plant_id_eia'])</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 170 | <code>                screen.selectbox[1].select(entry['dataset_id']).run(timeout=30)</code> | Сохраняет/переключает указанное тестовое состояние или проверяет реальную таблицу виджетов. |
| 171 | <code>                self.assertFalse(screen.exception, str(screen.exception))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 172 | <code>                self.assertTrue(any(x.value == 'Model not ready' for x in screen.info))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 173 | <code>                if status != 'measurements_only':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 174 | <code>                    self.assertEqual(len(screen.metric), 0)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 175 | <code>                if status == 'review_required':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |
| 176 | <code>                    self.assertTrue(any('Data review required' in x.value for x in screen.error))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 178 | <code>    def test_corrupt_model_graceful(self):</code> | Имитирует FileNotFoundError в чтении модели: измерения остаются, модель получает понятное сообщение, экран не падает. |
| 179 | <code>        screen = self.screen()</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 180 | <code>        from streamlit.testing.v1 import AppTest</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 181 | <code>        script = f'''</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 182 | <code>import sys</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 183 | <code>sys.path.insert(0, {str(ROOT / 'src/ui')!r})</code> | Добавляет локальную область импорта: Streamlit запускает файл, а MODEL расположен в соседнем пакете. |
| 184 | <code>from unittest.mock import patch</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |
| 185 | <code>import app</code> | Подключает указанные библиотеки/общие функции, чтобы переиспользовать проверенную реализацию. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 186 | <code>with patch.object(app, 'verified_results', side_effect=FileNotFoundError('updating')):</code> | Временно подменяет только указанную зависимость теста; после блока восстанавливает её, настоящие файлы не меняет. |
| 187 | <code>    app.render()</code> | Продолжает непосредственно предшествующее выражение: перечисляет его точные аргументы, поля или ограничивающие условия. |
| 188 | <code>'''</code> | Документирует назначение блока; не выполняет вычислений и не меняет данные. |
| 189 | <code>        screen = AppTest.from_string(script).run(timeout=30)</code> | Сохраняет указанное локальное значение для текущего блока; не записывает MODEL или исходные данные. |
| 190 | <code>        self.assertFalse(screen.exception)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 191 | <code>        self.assertEqual(len(screen.metric), 3)</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 192 | <code>        self.assertTrue(any('temporarily unavailable' in x.value for x in screen.warning))</code> | Утверждает указанный ожидаемый результат сценария; несоответствие делает тест неуспешным. |
| 195 | <code>if __name__ == '__main__':</code> | Проверяет указанное условие перед следующим действием: неподходящее состояние не получает числовую оценку. |

| Строка | Код | Что делает и зачем |
| --- | --- | --- |
| 196 | <code>    unittest.main()</code> | Разрешает отдельный запуск файла тестов стандартным unittest. |

