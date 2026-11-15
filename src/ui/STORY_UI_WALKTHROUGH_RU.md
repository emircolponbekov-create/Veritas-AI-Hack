# Интерактивный UI: разбор реализации для защиты

Данные → `SiteSupport` → небольшие функции отображения. Реестр v2, отчёт v1 и story-support v1 остаются раздельными. Нового обучения, платных API и научных выводов здесь нет.

Читать сначала пояснение функции, затем маленькие таблицы строк. Номера относятся к текущим файлам. Пустые строки не выполняют действий и в таблицы не включены. Для существующего UI показаны добавленные/изменённые строки относительно сохранённого снимка до story-интеграции; старые walkthrough сохраняют остальные объяснения.

На защите: показать одну связь statement → source/period/scope, исключённый месяц без карточек и различие recirculating/unknown. Объяснить, почему месячный выбор не пересчитывает экологический отчёт.

## src/ui/exploration_panel.py

Новый тонкий слой отображения над SiteSupport. Здесь нет поиска источников, изменения данных или генератора научных выводов.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | <code>"""Small, read-only views over the MODEL story-support contract."""</code> | Кратко описывает назначение модуля или функции. |
| 2 | <code>import base64</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 3 | <code>import logging</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 4 | <code>from html import escape</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 5 | <code>import pandas as pd</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 6 | <code>import streamlit as st</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 7 | <code>from water_scene import water_chart</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 9 | <code>LOG = logging.getLogger(__name__)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 10 | <code>MONTH_STATUS = {</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 11 | <code>'verified_measurement': 'Verified reported measurement',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 12 | <code>'excluded_method': 'Excluded: reporting method is not an explicit thermometer measurement',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 13 | <code>'missing_temperatures': 'Unavailable: incomplete temperature pair',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 14 | <code>'missing_month': 'Unavailable: no source record for this month',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 15 | <code>'review_required': 'Data review required: values withheld',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 16 | <code>'blocked': 'Unavailable: this dataset is blocked or reference only',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 17 | <code>}</code> | Завершает выражение или структуру данных из предыдущих строк. |

### availability

Собирает независимые признаки наличия материалов. Несколько признаков могут сосуществовать; они не оценивают экологичность.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 20 | <code>def availability(record):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 21 | <code>"""Independent availability flags; no score or quality ranking."""</code> | Кратко описывает назначение модуля или функции. |
| 22 | <code>if record is None:</code> | Выбирает ветку только при выполнении указанного условия. |
| 23 | <code>return 'Availability could not be verified'</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |
| 24 | <code>flags = []</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 25 | <code>if record.get('report_state') == 'missing':</code> | Выбирает ветку только при выполнении указанного условия. |
| 26 | <code>flags.append('No ecological report')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 27 | <code>if record.get('has_substantive_environment_report'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 28 | <code>flags.append('Environmental report')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 29 | <code>if record.get('has_insufficient_evidence_report'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 30 | <code>flags.append('Insufficient ecological evidence')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 31 | <code>if record.get('any_system_has_verified_measurements', record.get('has_verified_measurements')):</code> | Выбирает ветку только при выполнении указанного условия. |
| 32 | <code>flags.append('Measurements')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 33 | <code>if record.get('any_system_has_verified_model_results', record.get('has_verified_model_results')):</code> | Выбирает ветку только при выполнении указанного условия. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 34 | <code>flags.append('Saved model')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 35 | <code>if record.get('any_system_requires_review', record.get('requires_review')) or record.get('report_state') in {'review_required', 'evidence_unavailable'}:</code> | Выбирает ветку только при выполнении указанного условия. |
| 36 | <code>flags.append('Review needed')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 37 | <code>if record.get('data_blocked') or record.get('no_temperature_pairs'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 38 | <code>flags.append('No confirmed temperature pairs')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 39 | <code>return ' · '.join(flags) or 'No verified materials yet'</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### support_call

Изолирует сбой необязательного story API, чтобы прежние измерения и результаты оставались доступны.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 42 | <code>def support_call(provider, method, *args):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 43 | <code>"""A failed story feature must not prevent the legacy explorer from loading."""</code> | Кратко описывает назначение модуля или функции. |
| 44 | <code>if provider is None:</code> | Выбирает ветку только при выполнении указанного условия. |
| 45 | <code>return None</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |
| 46 | <code>try:</code> | Начинает операцию, для которой ниже предусмотрена обработка ошибок. |
| 47 | <code>return getattr(provider, method)(*args)</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |
| 48 | <code>except (OSError, ValueError, KeyError, TypeError, ImportError):</code> | Перехватывает перечисленные ошибки и переходит к честному состоянию недоступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 49 | <code>LOG.warning('Story support unavailable: %s', method)</code> | Сохраняет безопасную диагностическую метку, без пользовательского traceback. |
| 50 | <code>return None</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### journey_panel

Берёт готовое описание MODEL, переключает три этапа штатным виджетом и показывает учебный SVG. Семейство охлаждения определяет подпись и петлю повторного использования.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 53 | <code>def journey_panel(payload, identifier):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 54 | <code>st.header('Follow a drop', anchor='drop-journey')</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |
| 55 | <code>if payload is None:</code> | Выбирает ветку только при выполнении указанного условия. |
| 56 | <code>st.info('The cooling explanation is temporarily unavailable. Measurements can still be explored below.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 57 | <code>return</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 58 | <code>family = payload['cooling_family']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 59 | <code>family_label = {'once_through': 'Once-through cooling', 'recirculating': 'Recirculating cooling', 'unknown': 'General educational scheme — cooling type unconfirmed'}[family]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 60 | <code>st.caption(family_label + ' · Historical metadata, not a current engineering map.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 61 | <code>steps = payload['steps']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 62 | <code>stage_ids = [step['id'] for step in steps]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 63 | <code>selected = st.segmented_control('Choose a stage', stage_ids, default=stage_ids[0], required=True,</code> | Создаёт штатный переключатель трёх этапов, доступный с клавиатуры. |
| 64 | <code>format_func=lambda value: str(stage_ids.index(value) + 1) + ' / ' + next(step['title'] for step in steps if step['id'] == value),</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 65 | <code>key='journey_' + identifier, wrap=True)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 66 | <code>step = next(step for step in steps if step['id'] == selected)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 67 | <code># A local illustration uses no spatial data, plume geometry or station imagery.</code> | Комментарий поясняет границу или причину реализации; сам не выполняется. |
| 68 | <code>loop = '&lt;path d="M340 135 C340 178 230 178 230 135 L230 105 L255 105" fill="none" stroke="#aed7d4" stroke-width="3"/&gt;&lt;text x="325" y="184" text-anchor="middle"&gt;cool &amp; reuse&lt;/text&gt;' if family == 'recirculating' else ''</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 69 | <code>labels = ['Intake', 'Heat exchange', 'Conditional release' if family == 'recirculating' else 'Discharge & mixing']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 70 | <code>shapes = [</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 71 | <code>'&lt;path d="M55 112q15-16 30 0t30 0t30 0M70 96q15-16 30 0t30 0"/&gt;',</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 72 | <code>'&lt;path d="M290 75v55m15-55v55m15-55v55m15-55v55M275 88h80m-80 30h80"/&gt;',</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 73 | <code>'&lt;path d="M500 96q15-16 30 0t30 0t30 0M500 118q15-16 30 0t30 0t30 0"/&gt;',</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 74 | <code>]</code> | Завершает выражение или структуру данных из предыдущих строк. |
| 75 | <code>nodes = ''.join(f'&lt;g stroke="{("#d0f56f" if i == stage_ids.index(selected) else "#72eee4")}" stroke-width="3" fill="none"&gt;{shape}&lt;/g&gt;&lt;text x="{100+i*220}" y="55" text-anchor="middle"&gt;{escape(labels[i])}&lt;/text&gt;' for i, shape in enumerate(shapes))</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 76 | <code>release_dash = ' stroke-dasharray="5 6"' if family == 'recirculating' else ''</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 77 | <code>svg = '&lt;svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 200"&gt;&lt;g fill="#e7f6f2" font-family="Segoe UI, sans-serif" font-size="16"&gt;' + nodes + '&lt;path d="M155 105h100m-10-8 10 8-10 8" fill="none" stroke="#72eee4" stroke-width="2"/&gt;&lt;path d="M375 105h100m-10-8 10 8-10 8" fill="none" stroke="#72eee4" stroke-width="2"' + release_dash + '/&gt;' + loop + '&lt;/g&gt;&lt;/svg&gt;'</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 78 | <code>image = base64.b64encode(svg.encode()).decode('ascii')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 79 | <code>st.html('&lt;div class="journey-art"&gt;&lt;img alt="' + escape('Educational sequence: ' + ' to '.join(labels)) + '" src="data:image/svg+xml;base64,' + image + '"/&gt;&lt;/div&gt;')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 80 | <code>st.subheader(step['title'])</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 81 | <code>st.write(step['general_explanation'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 82 | <code>st.caption('Educational illustration, not a traced water particle, thermal map or assessment of harm or safety.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 83 | <code>with st.expander('Stage sources and what remains unknown'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 84 | <code>st.write(step['confirmed_for_system'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 85 | <code>for reference in step['sources']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 86 | <code>st.link_button(reference['title'], reference['url'], wrap=True)</code> | Даёт ссылку именно на указанный проверенный источник. |
| 87 | <code>st.caption(reference['role'].replace('_', ' ') + ' · ' + reference['locator'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 88 | <code>if step.get('site_context'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 89 | <code>context = step['site_context']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 90 | <code>st.write(context['text'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 91 | <code>st.link_button(context['source']['title'], context['source']['url'], wrap=True)</code> | Даёт ссылку именно на указанный проверенный источник. |
| 92 | <code>st.caption('Operator account · ' + context['source']['locator'] + ' · ' + context['source']['period'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 93 | <code>st.caption(context['limitation'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 94 | <code>st.caption('Metadata period: ' + ' to '.join(payload['period']))</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 95 | <code>for unknown in step['unknowns'] + payload['limitations']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 96 | <code>st.write(unknown)</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

### month_panel

Создаёт единственный выбор месяца по полному календарю. Только verified_measurement получает числовые карточки; пропуски сохраняются в графике.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 99 | <code>def month_panel(payload, identifier):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 100 | <code>"""One month widget includes every historical calendar slot, including gaps."""</code> | Кратко описывает назначение модуля или функции. |
| 101 | <code>st.header('A ribbon of months', anchor='month-ribbon')</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |
| 102 | <code>st.write('Explore the reported water temperature before and after cooling, one historical month at a time.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 103 | <code>if not payload or payload['state'] != 'available' or not payload['rows']:</code> | Выбирает ветку только при выполнении указанного условия. |
| 104 | <code>st.info('The monthly record is temporarily unavailable. No replacement temperatures are shown.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 105 | <code>return None</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 106 | <code>rows = {row['report_month']: row for row in payload['rows']}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 107 | <code>months = list(rows)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 108 | <code>verified = [month for month, row in rows.items() if row['status'] == 'verified_measurement']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 109 | <code>month = st.select_slider('Historical reporting month', months, value=verified[-1] if verified else months[-1],</code> | Создаёт единственную ленту месяцев с реальными календарными вариантами. |
| 110 | <code>key='month_' + identifier, persist_state='session', help='Arrow keys move by one month. Excluded and missing months remain selectable. No autoplay.')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 111 | <code>row = rows[month]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 112 | <code>st.subheader(pd.Timestamp(month).strftime('%B %Y'))</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 113 | <code>st.caption(MONTH_STATUS[row['status']])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 114 | <code>if row['status'] == 'verified_measurement':</code> | Выбирает ветку только при выполнении указанного условия. |
| 115 | <code>for column, label, field in zip(st.columns(3), ['Intake temperature, °C', 'Discharge temperature, °C', 'Reported ΔT, °C'],</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 116 | <code>['intake_temperature_c', 'discharge_temperature_c', 'delta_t_c']):</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 117 | <code>column.metric(label, f'{row[field]:.2f}')</code> | Показывает проверенное значение месяца и подписанную единицу. |
| 118 | <code>difference = row['delta_t_c']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 119 | <code>direction = 'warmer' if difference &gt; 0 else 'cooler' if difference &lt; 0 else 'the same temperature'</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 120 | <code>comparison = f'{abs(difference):.2f} °C {direction}' if difference else direction</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 121 | <code>st.write(f'In {pd.Timestamp(month).strftime("%B %Y")}, water leaving this system was {comparison} compared with water entering it, based on reported monthly averages.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 122 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 123 | <code>st.info(MONTH_STATUS[row['status']] + '. This month has no confirmed temperature cards or substituted values.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 124 | <code>st.caption('This difference is across the cooling system, not warming of the whole water body. The ecological report has its own evidence periods and does not change with this month.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 125 | <code>frame = pd.DataFrame(payload['rows']).set_index('report_month')[['intake_temperature_c', 'discharge_temperature_c']]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 126 | <code>frame.index = pd.to_datetime(frame.index)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 127 | <code>if verified:</code> | Выбирает ветку только при выполнении указанного условия. |
| 128 | <code>water_chart(frame.rename(columns={'intake_temperature_c': 'Measured intake', 'discharge_temperature_c': 'Measured discharge'}),</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 129 | <code>x_label='Reporting month', y_label='Temperature (°C)', height=260, color=['#70eee4', '#ffc86b'], selected_month=month)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 130 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 131 | <code>st.info('No confirmed temperature series for this system. An empty chart would not represent a measurement.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 132 | <code>st.caption(f'{len(verified)} verified measured months / {len(months)} calendar months · {months[0]} to {months[-1]}. Gaps are unavailable, never zero or interpolated. Rounding is not sensor precision.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 133 | <code>with st.expander('Missing, excluded and review-blocked months'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 134 | <code>unavailable = [dict(Month=key, Status=MONTH_STATUS[value['status']]) for key, value in rows.items() if value['status'] != 'verified_measurement']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 135 | <code>if unavailable:</code> | Выбирает ветку только при выполнении указанного условия. |
| 136 | <code>st.table(unavailable)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 137 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 138 | <code>st.write('Every month in this period has a verified reported measurement.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 139 | <code>return month</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

## src/ui/app.py

Изменения относительно сохранённого UI перед story-интеграцией. Перенесённый без изменения смысловой код не нужно переучивать как новый алгоритм.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 3 | <code>import logging</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 15 | <code>from exploration_panel import availability, support_call, journey_panel, month_panel</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 17 | <code>LOG = logging.getLogger(__name__)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

### model_panel

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 62 | <code>LOG.warning('Saved comparison unavailable: %s', type(exc).__name__)</code> | Сохраняет безопасную диагностическую метку, без пользовательского traceback. |
| 63 | <code>st.warning('Saved results are temporarily unavailable or need review. Refresh data to retry.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

### render_technical

Сохраняет прежние графики, Ridge, baseline, сценарии и методику. Получает тот же выбранный месяц, отдельного переключателя не создаёт.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 96 | <code>def render_technical(entry, identifier, plant_id, token, root, publication, month):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 111 | <code>LOG.warning('Technical measurements unavailable: %s', type(exc).__name__)</code> | Сохраняет безопасную диагностическую метку, без пользовательского traceback. |
| 112 | <code>st.warning('Measured data are temporarily unavailable or need review. Refresh data to retry.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

### select_surry

Callback переключает площадку до следующего рендера виджетов.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 167 | <code>def select_surry():</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 168 | <code>st.session_state['plant'] = 3806</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

### story_support

Создаёт новый provider на каждый запрос, проверяет версии зависимостей каталога и пересчитывает только устаревший каталог без обучения.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 171 | <code>def story_support(root):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 172 | <code>"""Revalidate the MODEL snapshot; never cache a provider across reruns."""</code> | Кратко описывает назначение модуля или функции. |
| 173 | <code>try:</code> | Начинает операцию, для которой ниже предусмотрена обработка ошибок. |
| 174 | <code>from src.model.site_support import SiteSupport, read_catalog</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 175 | <code>provider = SiteSupport(root)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 176 | <code>try:</code> | Начинает операцию, для которой ниже предусмотрена обработка ошибок. |
| 177 | <code>catalog = read_catalog(root)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 178 | <code>except (OSError, ValueError, KeyError, TypeError):</code> | Перехватывает перечисленные ошибки и переходит к честному состоянию недоступности. |
| 179 | <code>catalog = provider.catalog()</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 180 | <code>return provider, catalog</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |
| 181 | <code>except (OSError, ValueError, KeyError, TypeError, ImportError):</code> | Перехватывает перечисленные ошибки и переходит к честному состоянию недоступности. |
| 182 | <code>LOG.warning('Story-support catalog unavailable')</code> | Сохраняет безопасную диагностическую метку, без пользовательского traceback. |
| 183 | <code>return None, None</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### render

Сначала выбирает площадку и показывает краткий экологический отчёт, затем учебный процесс и календарь. Технический исследователь открывается отдельно.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 187 | <code>st.set_page_config(page_title='Nuclear Water & Climate Lab', page_icon='🌊', layout='wide')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 189 | <code>reduced = st.session_state.get('reduce_motion', False)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 190 | <code>st.html(hero_html(reduced))</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 193 | <code>except (OSError, ValueError, KeyError, TypeError):</code> | Перехватывает перечисленные ошибки и переходит к честному состоянию недоступности. |
| 194 | <code>st.error('The station catalog is temporarily unavailable. Refresh the page to retry.')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 195 | <code>install_motion(reduced)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 202 | <code>install_motion(reduced)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 204 | <code>provider, catalog = story_support(root)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 205 | <code>plant_flags = {row['plant_id_eia']: row for row in catalog['plants']} if catalog else {}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 206 | <code>system_flags = {row['dataset_id']: row for row in catalog['systems']} if catalog else {}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 207 | <code>st.markdown('&lt;div id="explore-water" class="lab-eyebrow"&gt;01 / Start with a station&lt;/div&gt;', unsafe_allow_html=True)</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 208 | <code>st.subheader('What does the evidence tell us?')</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |
| 209 | <code>st.write('Start with Surry: explore a source-based environmental report, follow the cooling process, then browse historical water measurements. Other sites have different evidence coverage.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 210 | <code>site_column, settings = st.columns([3, 1], vertical_alignment='bottom')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 211 | <code>plant_id = site_column.selectbox('Plant site — available materials', ids, index=ids.index(3806) if 3806 in ids else 0,</code> | Создаёт выбор площадки/системы из проверенного каталога. |
| 212 | <code>format_func=lambda plant: plants[plant] + ' · ' + availability(plant_flags.get(plant)), key='plant')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 213 | <code>with settings:</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 214 | <code>reduced = st.toggle('Reduce decorative motion', key='reduce_motion', help='Turns off decorative movement and fades. Your operating system’s reduced-motion setting is always respected.')</code> | Создаёт явный пользовательский переключатель режима. |
| 215 | <code>st.button('Refresh data', help='Reread verified files. No training or external source search.', width='stretch')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 216 | <code>st.caption(availability(plant_flags.get(plant_id)) + '. Availability flags may coexist; they are not an environmental rating.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 217 | <code>if catalog:</code> | Выбирает ветку только при выполнении указанного условия. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 218 | <code>coverage = plant_flags[plant_id]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 219 | <code>st.caption(f"Measurements: {coverage['verified_measurement_systems']}/{coverage['system_count']} registered systems; saved models: {coverage['verified_model_systems']}/{coverage['system_count']}. This is coverage, not a safety score.")</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 220 | <code>if not catalog:</code> | Выбирает ветку только при выполнении указанного условия. |
| 221 | <code>st.info('Material availability could not be verified. Individual measurement and report readers remain available.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 222 | <code>if plant_id != 3806:</code> | Выбирает ветку только при выполнении указанного условия. |
| 223 | <code>st.button('Explore the Surry example', on_click=select_surry)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 227 | <code>with st.expander('Cooling system and measurement coverage'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 228 | <code>identifier = st.selectbox('Cooling system', system_ids, index=default,</code> | Создаёт выбор площадки/системы из проверенного каталога. |
| 229 | <code>format_func=lambda value: next(e['cooling_id_eia'] for e in systems if e['dataset_id'] == value) + ' · ' + availability(system_flags.get(value)),</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 230 | <code>key=f'system_{plant_id}')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 231 | <code>st.caption('Each system has its own measurements and review status. Site reports and system findings have different scopes.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 233 | <code>st.caption(plants[plant_id] + ' · Selected cooling system ' + str(entry['cooling_id_eia']))</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 234 | <code>details = support_call(provider, 'claim_details', plant_id, entry['cooling_id_eia'])</code> | Читает соответствующий готовый payload MODEL через безопасный адаптер. |
| 235 | <code>publication = environment_panel(plant_id, entry['cooling_id_eia'], root, details)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 236 | <code>journey_panel(support_call(provider, 'journey', identifier), identifier)</code> | Читает соответствующий готовый payload MODEL через безопасный адаптер. |
| 237 | <code>timeline = support_call(provider, 'timeline', identifier)</code> | Читает соответствующий готовый payload MODEL через безопасный адаптер. |
| 238 | <code>month = month_panel(timeline, identifier)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 239 | <code>st.markdown('&lt;div class="lab-note"&gt;&lt;b&gt;The role of AI.&lt;/b&gt; Ridge estimates a completed month’s cooling-system temperature difference. '</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 240 | <code>'Environmental reports use reviewed sources and rules, not a trained environmental-safety model. No overall safety or environmental score is calculated.&lt;/div&gt;', unsafe_allow_html=True)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 242 | <code>st.caption('Saved model comparisons, original measurements, assumptions and explicit user-entered scenarios. Model estimates stay separate from measured temperatures.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 245 | <code>render_technical(entry, identifier, plant_id, token, root, publication, month)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 246 | <code>st.markdown('&lt;div class="lab-footer"&gt;Nuclear Water &amp; Climate Lab / Historical data. Transparent estimates. '</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 247 | <code>'No environmental safety ranking.&lt;br&gt;Data: EIA · Catalyst Cooperative PUDL &#124; Built with Streamlit&lt;/div&gt;', unsafe_allow_html=True)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 248 | <code>install_motion(reduced)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

## src/ui/environment_panel.py

Проверенные атомарные утверждения и периоды идут из backend, а исходная публикация остаётся неизменной.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 2 | <code>from pathlib import Path</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 19 | <code>'missing': 'No environmental report has been published for this station. Explore the cooling explanation and check measurement availability below.',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

### statement_evidence

Показывает конкретное утверждение с его областью и ограничением; раскрытие использует только проверенные связи MODEL с источниками.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 26 | <code>def statement_evidence(card, root):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 27 | <code>"""Display only the reviewed links for this exact statement."""</code> | Кратко описывает назначение модуля или функции. |
| 28 | <code>scope = card['scope']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 29 | <code>label = ('System ' + str(scope.get('cooling_id_eia')) if scope['level'] == 'system'</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 30 | <code>else 'General context' if scope['level'] == 'general' else 'Site context')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 31 | <code>st.caption(label + ' · ' + card['period']['label'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 32 | <code>st.text(card['statement'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 33 | <code># The boundary belongs beside the claim, even when its citations are closed.</code> | Комментарий поясняет границу или причину реализации; сам не выполняется. |
| 34 | <code>st.caption('Limit: ' + card['limitation'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 35 | <code>with st.expander('Why this conclusion?', key='proof_' + card['statement_id']):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 36 | <code>st.caption('Exact reviewed wording: ' + card['display_span'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 37 | <code>if not card['sources']:</code> | Выбирает ветку только при выполнении указанного условия. |
| 38 | <code>st.write('Review boundary / evidence gap, not a new field observation.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 39 | <code>review = Path(root) / 'src/model/environment_evidence/CAPABILITY_AUDIT_RU.md'</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 40 | <code>if review.is_file():</code> | Выбирает ветку только при выполнении указанного условия. |
| 41 | <code>st.download_button('Download review notes', review.read_bytes(), file_name='evidence-review.md', mime='text/markdown', key='review_' + card['statement_id'], on_click='ignore')</code> | Предлагает локальные заметки проверки, не выдавая их за полевое наблюдение. |
| 42 | <code>for reference in card['sources']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 43 | <code>st.link_button(reference['title'], reference['url'], wrap=True, width='stretch')</code> | Даёт ссылку именно на указанный проверенный источник. |
| 44 | <code>st.caption('Source role: ' + SOURCE_ROLES.get(reference['role'], reference['role'].replace('_', ' ')))</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 45 | <code>st.caption(reference['locator'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 46 | <code>st.caption('Observation period: ' + card['period']['label'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 47 | <code>st.caption('Geography: ' + card['geography'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 48 | <code>if card['counterevidence']:</code> | Выбирает ветку только при выполнении указанного условия. |
| 49 | <code>st.write('Related evidence addresses a different endpoint; it is not a direct contradiction.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 50 | <code>for item in card['counterevidence']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 51 | <code>st.caption(item['source_id'] + ' · ' + item['locator'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 52 | <code>st.caption('Review basis: ' + card['review_basis'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

### environment_panel

Сохраняет реальные периоды и состояния отчёта, открывает короткие тематические вкладки и фильтрует только системные утверждения.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 55 | <code>def environment_panel(plant_id, system, root, details=None):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 60 | <code>(st.warning if snapshot.state == 'review_required' else st.info)(message)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 61 | <code>st.markdown('[Explore available measurements](#month-ribbon) · [Try the Surry example](#explore-water)')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 62 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 63 | <code>report = snapshot.report</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 64 | <code>st.caption('Evidence period: ' + report['period_label'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 65 | <code>st.caption('The report does not change with the historical month selector. Specialist review has not been performed.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 66 | <code>cards = details.get('statements', []) if details and details['report_state'] == 'ready' else []</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 67 | <code>with st.container(border=True, key='environment_summary'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 68 | <code>st.subheader('At a glance')</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |
| 69 | <code>if cards:</code> | Выбирает ветку только при выполнении указанного условия. |
| 70 | <code>summary_cards = [card for card in cards if card['target'] == 'summary']</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 71 | <code>if not details.get('omitted_system_statement_ids'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 72 | <code>st.text(report['summary'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 73 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 74 | <code>for card in summary_cards:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 75 | <code>st.text(card['statement'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 76 | <code>with st.expander('Evidence behind this summary'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 77 | <code>for card in summary_cards:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 78 | <code>statement_evidence(card, root)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 79 | <code>elif system == 'CW1' or snapshot.state == 'insufficient_evidence':</code> | Выбирает ветку только при выполнении указанного условия. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 80 | <code>st.text(report['summary'])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 81 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 82 | <code>st.write('Site report available. System-specific statement links need review before they can be displayed here.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 83 | <code>if details and details.get('omitted_system_statement_ids'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 84 | <code>st.info('CW1 findings are omitted for your selected system. The remaining findings are site or general context, not effects attributed to ' + str(system) + '.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 85 | <code>if snapshot.state == 'insufficient_evidence':</code> | Выбирает ветку только при выполнении указанного условия. |
| 86 | <code>st.info('Not enough reviewed evidence for site-specific environmental conclusions. This is not a favourable or unfavourable assessment.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 87 | <code>elif not cards:</code> | Выбирает ветку только при выполнении указанного условия. |
| 88 | <code>st.warning('Statement-level source links need review. No substitute citations are assigned.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 89 | <code>titles = {'water': 'Water', 'animals_plants': 'Animals & plants', 'people': 'People', 'climate': 'Climate', 'unknowns': 'What is unknown'}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 90 | <code>with st.container(key='environment_sections'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 91 | <code>tabs = st.tabs([titles[section['id']] for section in report['sections']])</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 92 | <code>for tab, section in zip(tabs, report['sections']):</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 93 | <code>with tab:</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 94 | <code>st.subheader(section['title'])</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |
| 95 | <code>st.caption(STATUS_LABELS[section['status']])</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 96 | <code>section_cards = [card for card in cards if card['target'] == section['id']]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 97 | <code>if section_cards:</code> | Выбирает ветку только при выполнении указанного условия. |
| 98 | <code># Keep a short entry; the entire reviewed text stays available.</code> | Комментарий поясняет границу или причину реализации; сам не выполняется. |
| 99 | <code>for card in section_cards[:1]:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 100 | <code>statement_evidence(card, root)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 101 | <code>with st.expander('Read the full finding: ' + titles[section['id']]):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 102 | <code>for card in section_cards[1:]:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 103 | <code>statement_evidence(card, root)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 104 | <code>if not details.get('omitted_system_statement_ids'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 105 | <code>with st.expander('Original reviewed wording'):</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 106 | <code>for paragraph in section['paragraphs']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 107 | <code>st.text(paragraph)</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 108 | <code>elif snapshot.state == 'insufficient_evidence':</code> | Выбирает ветку только при выполнении указанного условия. |
| 109 | <code>for paragraph in section['paragraphs']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 110 | <code>st.text(paragraph)</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 111 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 112 | <code>st.info('No reviewed statement links apply to this selection.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 113 | <code>if section['periods']:</code> | Выбирает ветку только при выполнении указанного условия. |
| 114 | <code>st.caption('Period: ' + '; '.join(period['label'] for period in section['periods']))</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 115 | <code># This navigation destination exists even for a missing or damaged report.</code> | Комментарий поясняет границу или причину реализации; сам не выполняется. |
| 116 | <code>st.subheader('Sources and limitations', anchor='evidence-methods')</code> | Добавляет понятный заголовок и, где задано, реальную цель навигационной ссылки. |
| 117 | <code>if snapshot.report is None:</code> | Выбирает ветку только при выполнении указанного условия. |
| 120 | <code>st.caption('Historical sources have different periods. An operator account is distinct from monitoring and general literature.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 121 | <code>st.caption('Compiled ' + snapshot.report['as_of'] + '; this is not an observation date.')</code> | Показывает указанный текст/статус, сохраняя различие фактов, границ и доступности. |
| 122 | <code>for section in snapshot.report['sections']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |

## src/ui/water_scene.py

Изменены навигационные адреса, объяснение первого экрана и передача режима движения.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | <code>"""Coastal presentation: local imagery, optional motion and measured charts."""</code> | Кратко описывает назначение модуля или функции. |

### hero_html

Меняет навигацию и короткое объяснение первого экрана; изображение и SVG остаются декоративными локальными ресурсами.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 42 | <code>def hero_html(reduced=False):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 62 | <code>&lt;nav aria-label="Page sections"&gt;&lt;a href="#explore-water"&gt;Explore&lt;/a&gt;&lt;a href="#environment-report"&gt;Environment&lt;/a&gt;&lt;a href="#drop-journey"&gt;Follow a drop&lt;/a&gt;&lt;a href="#month-ribbon"&gt;Months&lt;/a&gt;&lt;a href="#evidence-methods"&gt;Methodology&lt;/a&gt;&lt;/nav&gt;</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 77 | <code>&lt;p&gt;Explore the link between nuclear energy,&lt;br&gt;cooling water and living ecosystems.&lt;/p&gt;&lt;p class="hero-start"&gt;Historical measurements. Reviewed sources.&lt;br&gt;Start with the Surry example below.&lt;/p&gt;</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 84 | <code>html = html.replace('scene-paused"', 'scene-paused" data-reduced="' + str(reduced).lower() + '"')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

### install_motion

Передаёт ручной режим уменьшения движения локальному скрипту. Данные источников не превращаются в исполняемый код.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 88 | <code>def install_motion(reduced=False):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 91 | <code>setting = 'document.documentElement.classList.toggle("lab-motion-off", ' + str(reduced).lower() + ');'</code> | Создаёт явный пользовательский переключатель режима. |
| 92 | <code>st.html('&lt;script&gt;' + setting + script + '&lt;/script&gt;', unsafe_allow_javascript=True)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

## src/ui/motion.js

Существующий анимационный runtime теперь проверяет как системное предпочтение, так и ручной выключатель.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 9 | <code>const reduced = () =&gt; reduce.matches &#124;&#124; document.documentElement.classList.contains('lab-motion-off');</code> | Добавляет проверку ручного/системного режима уменьшения движения в существующий runtime; фон и значения данных не пересчитывает. |
| 14 | <code>const active = inView && !document.hidden && !reduced();</code> | Добавляет проверку ручного/системного режима уменьшения движения в существующий runtime; фон и значения данных не пересчитывает. |
| 33 | <code>if (!mouse.matches &#124;&#124; reduced() &#124;&#124; !inView &#124;&#124; document.hidden) return;</code> | Добавляет проверку ручного/системного режима уменьшения движения в существующий runtime; фон и значения данных не пересчитывает. |
| 75 | <code>if (state.seen.has(key) &#124;&#124; reduced()) node.classList.add('is-revealed');</code> | Добавляет проверку ручного/системного режима уменьшения движения в существующий runtime; фон и значения данных не пересчитывает. |

## src/ui/style.css

Дополнительные правила читаемости, фокуса, мобильных кнопок и полного отключения эффектов. data-testid относится к Streamlit 1.67 и требует повторной проверки при обновлении.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 133 | <code>/* Readable evidence and native, keyboard-operable story controls. */</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 134 | <code>:root { --lab-muted:#c2d9d9; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 135 | <code>[data-testid="stCaptionContainer"] { color:#c2d9d9 !important; font-size:.9rem !important; line-height:1.6; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 136 | <code>[data-testid="stText"], [data-testid="stMarkdownContainer"] p { line-height:1.65; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 137 | <code>.st-key-environment_summary, .st-key-environment_sections { max-width:920px; }</code> | Ограничивает ширину строки или иллюстрации для удобного чтения. |
| 138 | <code>.st-key-environment_summary [data-testid="stText"], .st-key-environment_sections [data-testid="stText"] { max-width:76ch; }</code> | Ограничивает ширину строки или иллюстрации для удобного чтения. |
| 139 | <code>[data-testid="stExpander"] summary { min-height:48px; padding-block:.7rem; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 140 | <code>[data-testid="stExpander"] [data-testid="stCaptionContainer"] { overflow-wrap:anywhere; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 141 | <code>[data-testid="stLinkButton"] a { white-space:normal; min-height:44px; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |
| 142 | <code>[data-testid="stSegmentedControl"] button { min-height:48px; padding:.65rem 1rem; border-color:#638e93; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |
| 143 | <code>[data-testid="stSegmentedControl"] button[aria-checked="true"] { background:#234c43; color:#e4ffad; border-color:#c9f272; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 144 | <code>[data-testid="stSlider"] { padding:1rem .4rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 145 | <code>[data-testid="stSlider"] [role="slider"] { outline-offset:6px; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 146 | <code>:where(input,select,textarea,[role="slider"],[role="tab"],[role="switch"],[tabindex]):focus-visible { outline:3px solid #83f7ef !important; outline-offset:4px; }</code> | Рисует заметный контур при клавиатурном фокусе. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 147 | <code>.journey-art { max-width:820px; border:1px solid var(--lab-line); border-radius:20px; background:linear-gradient(110deg,#123f48,#072d36); }</code> | Ограничивает ширину строки или иллюстрации для удобного чтения. |
| 148 | <code>.journey-art img { display:block; width:100%; height:auto; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 149 | <code>.hero-copy .hero-start { font-size:.9rem; line-height:1.5; color:#cce7e2; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 150 | <code>.lab-topline nav { flex-wrap:wrap; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 151 | <code>[id] { scroll-margin-top:85px; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 152 | <code>.lab-motion-off *, .lab-motion-off *::before, .lab-motion-off *::after { animation:none !important; transition:none !important; scroll-behavior:auto !important; }</code> | Выключает соответствующее движение/переход; статичное содержание остаётся видимым. |
| 153 | <code>.lab-motion-off .reveal-ready { opacity:1 !important; transform:none !important; }</code> | Выключает соответствующее движение/переход; статичное содержание остаётся видимым. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 154 | <code>.lab-motion-off .water-scene svg { transform:none !important; }</code> | Выключает соответствующее движение/переход; статичное содержание остаётся видимым. |
| 155 | <code>@media(max-width:760px) {</code> | Начинает правила узкого мобильного экрана. |
| 156 | <code>.lab-topline nav { overflow:visible; gap:.35rem .9rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 157 | <code>.lab-topline nav a { min-height:44px; display:inline-flex; align-items:center; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |
| 158 | <code>.lab-hero { min-height:560px; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |
| 159 | <code>.scene-caption { font-size:.75rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 160 | <code>.hero-copy { padding-bottom:5rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 161 | <code>[data-testid="stMetric"] { min-height:105px; padding:1rem; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |
| 162 | <code>[data-testid="stMetricValue"] { font-size:2rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 163 | <code>.lab-footer { font-size:.85rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 164 | <code>[role="tablist"] { gap:.65rem; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 165 | <code>[role="tab"] { min-height:44px; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |
| 166 | <code>}</code> | Заканчивает группу мобильных правил. |
| 168 | <code>button[data-variant="segmented_control"] { min-height:48px; padding:.65rem 1rem; background:#0b323b !important; color:#e8f7f3 !important; border-color:#638e93 !important; }</code> | Задаёт удобную высоту элемента/зоны нажатия; остальные свойства сохраняют океаническую тему. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 169 | <code>button[data-variant="segmented_control"][aria-checked="true"] { background:#284e43 !important; color:#e4ffad !important; border-color:#c9f272 !important; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 170 | <code>button[data-variant="segmented_control"]:hover { border-color:#83f7ef !important; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 171 | <code>[role="switch"][aria-checked="true"], [role="slider"] { accent-color:#d0f56f; }</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 173 | <code>/* Avoid showing previous-site content while Streamlit replaces a stale block. */</code> | Настраивает указанные цвет, интервал или перенос для читаемости выбранного элемента. |
| 174 | <code>[data-stale="true"] { visibility:hidden; }</code> | Скрывает старый блок при его замене Streamlit, чтобы не показывать данные другой станции. |

## submission/package_release.py

Продолжает прежний явный отбор путей; добавляет вложенные UI-ресурсы, сценарии, evidence/story-поддержку и версионирование.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | <code>"""Versioned local ZIP, extending the original explicit-allowlist packaging method."""</code> | Кратко описывает назначение модуля или функции. |
| 2 | <code>import argparse</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 3 | <code>import hashlib</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 4 | <code>import json</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 5 | <code>from datetime import datetime, timezone</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 6 | <code>from pathlib import Path</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 7 | <code>from zipfile import ZipFile, ZIP_DEFLATED</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 9 | <code>ROOT = Path(__file__).resolve().parents[1]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 10 | <code>ALLOWED = {'.py', '.md', '.ipynb', '.css', '.js', '.json', '.csv', '.parquet', '.png', '.svg', '.toml'}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 11 | <code>EXCLUDED = {'.venv', '__pycache__', '.git', '.codex', '.agents', 'node_modules', '.aws', '.ssh', '.pytest_cache'}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

### digest

Получает SHA-256 переданных байтов.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 14 | <code>def digest(data):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 15 | <code>return hashlib.sha256(data).hexdigest()</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### collect

Собирает разрешённые файлы, заранее обходит окружения/кэши и отклоняет секретные конфигурации, логи и вложенные ZIP.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 18 | <code>def collect():</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 19 | <code>files = {Path('AGENTS.md'), Path('README.md')}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 20 | <code>for area in ['src/model', 'src/ui', 'src/fuel', 'tests/model', 'tests/ui', 'tests/fuel', 'data', 'docs']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 21 | <code># Prune environment/cache directories before descending, not after reading them.</code> | Комментарий поясняет границу или причину реализации; сам не выполняется. |
| 22 | <code>pending = [ROOT / area]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 23 | <code>while pending:</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 24 | <code>directory = pending.pop()</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 25 | <code>for path in directory.iterdir():</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 26 | <code>assert not path.is_symlink(), 'Package inputs must be ordinary local files'</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 27 | <code>if path.name in EXCLUDED:</code> | Выбирает ветку только при выполнении указанного условия. |
| 28 | <code>continue</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 29 | <code>if path.is_dir():</code> | Выбирает ветку только при выполнении указанного условия. |
| 30 | <code>pending.append(path)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 31 | <code>elif path.suffix in ALLOWED or path.name == 'requirements.txt':</code> | Выбирает ветку только при выполнении указанного условия. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 32 | <code>files.add(path.relative_to(ROOT))</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 33 | <code>for path in (ROOT / 'submission').iterdir():</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 34 | <code>if path.is_file() and path.suffix in {'.md', '.json', '.ipynb', '.py'}:</code> | Выбирает ветку только при выполнении указанного условия. |
| 35 | <code>files.add(path.relative_to(ROOT))</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 36 | <code>files = {path for path in files if '.local.' not in path.name and 'protected_snapshot' not in path.name}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 37 | <code>for path in files:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 38 | <code>assert not set(path.parts) & EXCLUDED</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 39 | <code>assert not path.name.startswith('.env') and path.name not in {'credentials.json', 'secrets.toml'}</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 40 | <code>assert path.suffix not in {'.log', '.zip', '.pem', '.key'}</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 41 | <code>assert (b'-----BEGIN ' + b'PRIVATE KEY-----') not in (ROOT / path).read_bytes()</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 42 | <code>return files</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### verify

Проверяет CRC, полный список, хеши и размеры файлов архива, UI-зависимости и все входы/результаты, на которые ссылается реестр.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 45 | <code>def verify(archive):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 46 | <code>with ZipFile(archive) as bundle:</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 47 | <code>assert bundle.testzip() is None, 'ZIP CRC failure'</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 48 | <code>records = json.loads(bundle.read('submission/RELEASE_FILES.json'))</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 49 | <code>expected = set(records) &#124; {'submission/RELEASE_FILES.json', 'submission/RELEASE_MANIFEST.md'}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 50 | <code>assert set(bundle.namelist()) == expected, 'Unexpected or missing ZIP member'</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 51 | <code>for name, record in records.items():</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 52 | <code>data = bundle.read(name)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 53 | <code>assert len(data) == record['bytes'] and digest(data) == record['sha256'], name</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 54 | <code>for name in bundle.namelist():</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 55 | <code>path = Path(name)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 56 | <code>assert not path.is_absolute() and '..' not in path.parts</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 57 | <code>assert not set(path.parts) & EXCLUDED</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 58 | <code>for name in ['src/ui/exploration_panel.py', 'src/ui/style.css', 'src/ui/motion.js',</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 59 | <code>'src/ui/app.py', 'src/ui/environment_panel.py', 'src/ui/environment_loader.py',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 60 | <code>'src/ui/data_loader.py', 'src/ui/multistation_loader.py', 'src/ui/water_scene.py',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 61 | <code>'src/model/site_support.py', 'src/model/environment_report.py',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 62 | <code>'src/model/site_support_data/review.json',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 63 | <code>'src/ui/assets/coastline.png', 'src/model/site_support_data/claim_links.json',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 64 | <code>'src/model/site_support_data/journey.json', 'src/model/environment_evidence/claims.json',</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 65 | <code>'src/fuel/scenarios.py', 'src/ui/requirements.txt', 'data/environment_reports/v1/eia_3806/ready.json']:</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 66 | <code>assert name in expected, name</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 67 | <code>registry = json.loads(bundle.read('data/model_artifacts/multistation/registry.json'))</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 68 | <code>for entry in registry['datasets']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 69 | <code>assert entry['observations']['path'] in expected, 'Missing registered observation input'</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 70 | <code>if entry.get('results_path'):</code> | Выбирает ветку только при выполнении указанного условия. |
| 71 | <code>assert entry['results_path'] in expected, 'Missing registered saved result'</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 72 | <code>return len(expected)</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### build

Создаёт новую версию архива без перезаписи старой, обновляет точный манифест, проверяет готовый ZIP и пишет внешний SHA-256.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 75 | <code>def build(name):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 76 | <code>assert Path(name).name == name and name.endswith('.zip')</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 77 | <code>archive = ROOT / 'submission' / name</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 78 | <code>assert not archive.exists(), 'Use a new version name; previous releases are preserved'</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 79 | <code>files = collect()</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 80 | <code>manifest = ROOT / 'submission/RELEASE_MANIFEST.md'</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 81 | <code>records_path = ROOT / 'submission/RELEASE_FILES.json'</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 82 | <code>files.update([manifest.relative_to(ROOT), records_path.relative_to(ROOT)])</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 83 | <code>manifest.write_text('# Local release manifest\n\n'</code> | Записывает только документ/манифест/архив сдачи, не исходные измерения или модель. |
| 84 | <code>+ f'Archive: &#96;{name}&#96;. Built {datetime.now(timezone.utc).isoformat()}. Not published or submitted.\n\n'</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 85 | <code>+ 'Registry v2 + evidence-report v1 + story-support v1. Run instructions: README.md and src/ui/README.md. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 86 | <code>+ 'Current UI capabilities and remaining team actions: submission/UI_CAPABILITIES.md. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 87 | <code>+ 'Previous nuclear-water-release.zip is preserved unchanged and predates these extensions.\n\n'</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 88 | <code>+ 'Includes all UI readers, styles, motion script, coastal image; MODEL story/evidence sources, publications, '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 89 | <code>+ 'frozen observations, saved results and FUEL scenario implementation. No training binary is invented. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 90 | <code>+ 'The UI uses the pinned Python dependencies in src/ui/requirements.txt; scenario math uses the standard library.\n\n'</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 91 | <code>+ 'Run from the extracted root: &#96;.\\src\\ui\\.venv\\Scripts\\python.exe -m streamlit run src/ui/app.py '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 92 | <code>+ '--server.address 127.0.0.1 --server.port 8503 --browser.gatherUsageStats false&#96;. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 93 | <code>+ 'Create the environment and install src/ui/requirements.txt first if absent. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 94 | <code>+ 'Notebook review additionally needs matplotlib; the saved-model developer tests need matplotlib/scikit-learn and their dependencies. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 95 | <code>+ 'These developer dependencies are not required to view saved results in the UI.\n\n'</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 96 | <code>+ 'No virtual environments, caches, credentials, logs or ZIPs are members. '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 97 | <code>+ 'RELEASE_FILES.json contains byte counts and SHA-256 for every member except itself and this manifest; '</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 98 | <code>+ 'the outer ZIP checksum protects those two files. PACKAGE_CHECKS.json distinguishes actual checks from pending actions.\n\n'</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 99 | <code>+ '## Exact project-relative paths\n\n' + '\n'.join('- &#96;' + path.as_posix() + '&#96;' for path in sorted(files)) + '\n', encoding='utf-8')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 100 | <code>records = {path.as_posix(): {'sha256': digest((ROOT / path).read_bytes()), 'bytes': (ROOT / path).stat().st_size}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 101 | <code>for path in sorted(files) if path not in {manifest.relative_to(ROOT), records_path.relative_to(ROOT)}}</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 102 | <code>records_path.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')</code> | Записывает только документ/манифест/архив сдачи, не исходные измерения или модель. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 103 | <code>with ZipFile(archive, 'w', ZIP_DEFLATED, compresslevel=6) as bundle:</code> | Ограничивает контекст блока: UI-контейнер, архив или тестовую подмену. |
| 104 | <code>for path in sorted(files):</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 105 | <code>bundle.write(ROOT / path, path.as_posix())</code> | Записывает только документ/манифест/архив сдачи, не исходные измерения или модель. |
| 106 | <code>count = verify(archive)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 107 | <code>archive.with_suffix('.zip.sha256').write_text(digest(archive.read_bytes()) + '  ' + archive.name + '\n', encoding='ascii')</code> | Записывает только документ/манифест/архив сдачи, не исходные измерения или модель. |
| 108 | <code>print(f'Checked {count} files: {archive}')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 111 | <code>if __name__ == '__main__':</code> | Выбирает ветку только при выполнении указанного условия. |
| 112 | <code>parser = argparse.ArgumentParser(description=__doc__)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 113 | <code>parser.add_argument('--name', default='nuclear-water-release-20261115-interactive.zip')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 114 | <code>parser.add_argument('--verify', type=Path)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 115 | <code>arguments = parser.parse_args()</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 116 | <code>if arguments.verify:</code> | Выбирает ветку только при выполнении указанного условия. |
| 117 | <code>print('Verified files:', verify(arguments.verify))</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 118 | <code>else:</code> | Обрабатывает оставшийся случай, не подставляя готовый результат другой станции. |
| 119 | <code>build(arguments.name)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

## tests/ui/test_story.py

Проверяет поведение настоящих виджетов и контракт навигации. Статическая проверка CSS/JS не доказывает визуальный эффект.

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 1 | <code>"""Regression coverage for the read-only story-support UI."""</code> | Кратко описывает назначение модуля или функции. |
| 2 | <code>import asyncio</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 3 | <code>import base64</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 4 | <code>import json</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 5 | <code>import os</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 6 | <code>from pathlib import Path</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 7 | <code>import re</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 8 | <code>import sys</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 9 | <code>import unittest</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 10 | <code>from unittest.mock import MagicMock, patch</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 12 | <code>ROOT = Path(__file__).resolve().parents[2]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 13 | <code>sys.path.insert(0, str(ROOT / 'src/ui'))</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 14 | <code>from exploration_panel import availability</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 15 | <code>from water_scene import hero_html</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 18 | <code>class StoryTests(unittest.TestCase):</code> | Объединяет связанные проверки в тестовый класс. |

### setUp

Подготавливает существующий изолированный обход Windows event loop только для AppTest; продуктовые функции не подменяет.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 19 | <code>def setUp(self):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 20 | <code>if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':</code> | Выбирает ветку только при выполнении указанного условия. |

### loop

Создаёт неисполняемый event loop для ограниченной тестовой среды.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 21 | <code>def loop():</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 22 | <code>result = MagicMock(spec=asyncio.AbstractEventLoop)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 23 | <code>result.is_closed.return_value = False</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 24 | <code>return result</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### setUp

Подготавливает существующий изолированный обход Windows event loop только для AppTest; продуктовые функции не подменяет.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 25 | <code>factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop', side_effect=loop)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 26 | <code>factory.start()</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 27 | <code>self.addCleanup(factory.stop)</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

### screen

Запускает настоящий app.py в AppTest и проверяет отсутствие исключений.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 29 | <code>def screen(self):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 30 | <code>from streamlit.testing.v1 import AppTest</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 31 | <code>screen = AppTest.from_file(str(ROOT / 'src/ui/app.py')).run(timeout=40)</code> | В тесте воспроизводит указанное действие виджета и следующий запуск приложения. |
| 32 | <code>self.assertFalse(screen.exception, str(screen.exception))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 33 | <code>return screen</code> | Возвращает вычисленное значение вызывающему коду; не записывает исходные данные. |

### test_surry_journey_exclusion_and_motion_control

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 35 | <code>def test_surry_journey_exclusion_and_motion_control(self):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 36 | <code>screen = self.screen()</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 37 | <code>self.assertEqual(screen.select_slider[0].value, '2025-12')</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 38 | <code>self.assertEqual([node.value for node in screen.metric], ['6.11', '12.78', '6.67'])</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 39 | <code>self.assertTrue(any('Why this conclusion?' == node.label for node in screen.expander))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 40 | <code>screen.segmented_control[0].set_value('heat_transfer').run(timeout=40)</code> | В тесте воспроизводит указанное действие виджета и следующий запуск приложения. |
| 41 | <code>self.assertFalse(screen.exception)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 42 | <code>self.assertEqual(screen.segmented_control[0].value, 'heat_transfer')</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 43 | <code>self.assertTrue(any('heat' in node.value.lower() for node in screen.markdown))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 44 | <code>screen.select_slider[0].set_value('2024-08').run(timeout=40)</code> | В тесте воспроизводит указанное действие виджета и следующий запуск приложения. |
| 45 | <code>self.assertFalse(screen.exception)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 46 | <code>self.assertEqual(len(screen.metric), 0)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 47 | <code>self.assertTrue(any('Excluded' in node.value for node in screen.info))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 48 | <code>self.assertTrue(any('James River' in node.value for node in screen.text))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 49 | <code>screen.toggle(key='reduce_motion').set_value(True).run(timeout=40)</code> | В тесте воспроизводит указанное действие виджета и следующий запуск приложения. |
| 50 | <code>self.assertFalse(screen.exception)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 51 | <code>self.assertTrue(screen.toggle(key='reduce_motion').value)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 52 | <code>self.assertEqual(screen.select_slider[0].value, '2024-08')</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 53 | <code>screen.selectbox(key='system_3806').select('eia_3806_435732').run(timeout=40)</code> | Создаёт выбор площадки/системы из проверенного каталога. |
| 54 | <code>self.assertEqual(len(screen.metric), 0)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 55 | <code>self.assertFalse(any('warmer cooling-water discharge from CW1' in node.value for node in screen.text))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 56 | <code>self.assertTrue(any('CW1 findings are omitted' in node.value for node in screen.info))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

### test_brunswick_switch_and_absent_report

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 58 | <code>def test_brunswick_switch_and_absent_report(self):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 59 | <code>screen = self.screen()</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 60 | <code>screen.selectbox(key='plant').select(6014).run(timeout=40)</code> | Создаёт выбор площадки/системы из проверенного каталога. |
| 61 | <code>registry = json.loads((ROOT / 'data/model_artifacts/multistation/registry.json').read_text())</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 62 | <code>systems = [entry for entry in registry['datasets'] if entry['plant_id_eia'] == 6014 and entry['cooling_id_eia'] in {'1', '2'}]</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 63 | <code>self.assertEqual(len(systems), 2)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 64 | <code>for entry in systems:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 65 | <code>screen.selectbox(key='system_6014').select(entry['dataset_id']).run(timeout=40)</code> | Создаёт выбор площадки/системы из проверенного каталога. |
| 66 | <code>self.assertFalse(screen.exception)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 67 | <code>self.assertEqual(len(screen.metric), 3)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 68 | <code>self.assertTrue(any('No environmental report' in node.value for node in screen.info))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 69 | <code>self.assertFalse(any('James River' in node.value for node in screen.text))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 70 | <code>self.assertIn('month_' + entry['dataset_id'], screen.session_state)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 71 | <code>self.assertEqual(len(screen.select_slider), 1)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

### test_explicit_gaps_never_have_temperature_cards

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 73 | <code>def test_explicit_gaps_never_have_temperature_cards(self):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 74 | <code>from streamlit.testing.v1 import AppTest</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 75 | <code>script = f"""</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 76 | <code>import sys</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 77 | <code>sys.path.insert(0, {str(ROOT / 'src/ui')!r})</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 78 | <code>from exploration_panel import month_panel</code> | Подключает указанную библиотеку или существующий модуль; не создаёт второй алгоритм. |
| 79 | <code>payload = {{'state':'available','rows':[{{'report_month': month, 'status':status, 'intake_temperature_c':None,'discharge_temperature_c':None,'delta_t_c':None}} for month,status in [('2025-01','missing_month'),('2025-02','missing_temperatures')]]}}</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 80 | <code>month_panel(payload, 'gap_fixture')</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |
| 81 | <code>"""</code> | Кратко описывает назначение модуля или функции. |
| 82 | <code>screen = AppTest.from_string(script).run(timeout=20)</code> | В тесте воспроизводит указанное действие виджета и следующий запуск приложения. |
| 83 | <code>self.assertFalse(screen.exception)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 84 | <code>self.assertEqual(len(screen.metric), 0)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 85 | <code>self.assertTrue(any('incomplete temperature pair' in node.value for node in screen.info))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 86 | <code>screen.select_slider[0].set_value('2025-01').run(timeout=20)</code> | В тесте воспроизводит указанное действие виджета и следующий запуск приложения. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 87 | <code>self.assertEqual(len(screen.metric), 0)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 88 | <code>self.assertTrue(any('no source record' in node.value for node in screen.info))</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

### test_navigation_flags_and_motion_contract

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 90 | <code>def test_navigation_flags_and_motion_contract(self):</code> | Объявляет функцию с указанными входами; её роль описана над блоком. |
| 91 | <code>html = hero_html(True)</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 92 | <code>anchors = set(re.findall(r'href="#([^" ]+)"', html))</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 93 | <code>self.assertEqual(anchors, {'lab-home','explore-water','environment-report','drop-journey','month-ribbon','evidence-methods'})</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 94 | <code>self.assertIn('data-reduced="true"', html)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 95 | <code># Sections exist before their availability branches in their respective views.</code> | Комментарий поясняет границу или причину реализации; сам не выполняется. |
| 96 | <code>source = (ROOT / 'src/ui/environment_panel.py').read_text(encoding='utf-8') + (ROOT / 'src/ui/exploration_panel.py').read_text(encoding='utf-8')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 97 | <code>for target in ['environment-report', 'evidence-methods', 'drop-journey', 'month-ribbon']:</code> | Перебирает указанные элементы, сохраняя их собственные идентификаторы/значения. |
| 98 | <code>self.assertIn("anchor='" + target + "'", source)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 99 | <code>css = (ROOT / 'src/ui/style.css').read_text(encoding='utf-8')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 100 | <code>js = (ROOT / 'src/ui/motion.js').read_text(encoding='utf-8')</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 101 | <code>self.assertIn('.lab-motion-off', css)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 102 | <code>self.assertIn('prefers-reduced-motion', js)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 103 | <code>self.assertIn('document.hidden', js)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 104 | <code>self.assertIn('!reduced()', js)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 105 | <code>flags = availability({'has_insufficient_evidence_report':True,'any_system_has_verified_measurements':True,'any_system_has_verified_model_results':True})</code> | Задаёт показанное значение, параметр или локальную структуру для текущего этапа функции. |
| 106 | <code>self.assertIn('Insufficient ecological evidence', flags)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 107 | <code>self.assertIn('Measurements', flags)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |
| 108 | <code>self.assertIn('Saved model', flags)</code> | Проверяет указанное условие и останавливает проверку при несоответствии. |

### Настройка модуля

Проверка названного поведения: входные данные и ожидания указаны непосредственно в строках ниже.

| Строка | Код | Простое объяснение |
| --- | --- | --- |
| 111 | <code>if __name__ == '__main__':</code> | Выбирает ветку только при выполнении указанного условия. |
| 112 | <code>unittest.main()</code> | Продолжает выражение/шаблон предыдущей строки с показанным текстом или параметром. |

## Остальные регрессионные проверки

В test_environment.py и test_multistation.py ожидания управления месяцем используют `select_slider` вместо прежнего `selectbox`; технический раздел больше не создаёт второй месячный виджет. Существующие проверки чужой идентичности, испорченных файлов, обновлений и MAE сохранены. Подробный разбор этих загрузчиков остаётся в прежних walkthrough.

Изменённые README/описания объясняют интерфейс, а не алгоритмы. PACKAGE_CHECKS.json хранит только действительно наблюдавшиеся исходы. Новая версия архива сохраняет старый ZIP неизменным.
