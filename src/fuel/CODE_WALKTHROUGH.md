# Построчный разбор сценарных модулей

Формулы, числа и интерфейс разделены. Это расчётные сценарии, не AI и не заключение о реальном вреде. Отступ определяет принадлежность строки блоку.

## src/fuel/scenarios.py

| Строка | Код | Объяснение |
| --- | --- | --- |
| 1 | <code>"""Transparent scenario arithmetic, independent of retrospective ML artifacts."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 2 | <code>from math import isfinite</code> | Подключает указанные функции или модуль; само подключение не запускает обучение. |
| 4 | <code>IPCC_URL = 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'</code> | Сохраняет результат выражения в IPCC_URL. |
| 5 | <code>IPCC_NUCLEAR_G_PER_KWH = (3.7, 12.0, 110.0)</code> | Проверенные литературные минимум, медиана и максимум IPCC AR5; не параметры выбранной АЭС. |
| 8 | <code>def finite(value, name, *, minimum=None, positive=False):</code> | Проверяет число: оно должно быть конечным и удовлетворять ограничениям. |
| 9 | <code>    """Reject missing, nonnumeric, nonfinite and out-of-domain inputs."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 10 | <code>    if isinstance(value, bool):</code> | Выполняет следующий блок только при условии isinstance(value, bool). |
| 11 | <code>        raise ValueError(f'{name} must be a number.')</code> | Останавливает расчёт с понятной ошибкой ввода. |
| 12 | <code>    try:</code> | Начинает операцию, ошибки которой будут обработаны ниже. |
| 13 | <code>        value = float(value)</code> | Сохраняет результат выражения в value. |
| 14 | <code>    except (TypeError, ValueError):</code> | Перехватывает указанную ошибку; приложение сообщает о проблеме вместо неверного результата. |
| 15 | <code>        raise ValueError(f'{name} must be a finite number.') from None</code> | Останавливает расчёт с понятной ошибкой ввода. |
| 16 | <code>    if not isfinite(value):</code> | Выполняет следующий блок только при условии not isfinite(value). |
| 17 | <code>        raise ValueError(f'{name} must be finite.')</code> | Останавливает расчёт с понятной ошибкой ввода. |
| 18 | <code>    if minimum is not None and value &lt; minimum:</code> | Выполняет следующий блок только при условии minimum is not None and value < minimum. |
| 19 | <code>        raise ValueError(f'{name} must be at least {minimum}.')</code> | Останавливает расчёт с понятной ошибкой ввода. |
| 20 | <code>    if positive and value &lt;= 0:</code> | Выполняет следующий блок только при условии positive and value <= 0. |
| 21 | <code>        raise ValueError(f'{name} must be greater than zero.')</code> | Останавливает расчёт с понятной ошибкой ввода. |
| 22 | <code>    return value</code> | Возвращает результат вызывающему коду; исходные данные не изменяются. |
| 25 | <code>def mixed_stream(ambient_c, discharge_c, bypass_m3_s, discharge_m3_s):</code> | Рассчитывает идеальную температуру после смешения двух отдельных потоков. |
| 26 | <code>    """Ideal steady complete mixing of TWO separate equal-density water streams."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 27 | <code>    ambient = finite(ambient_c, 'Ambient temperature', minimum=-273.15)</code> | Сохраняет результат выражения в ambient. |
| 28 | <code>    discharge = finite(discharge_c, 'Discharge temperature', minimum=-273.15)</code> | Сохраняет результат выражения в discharge. |
| 29 | <code>    bypass = finite(bypass_m3_s, 'Bypass flow', minimum=0)</code> | Сохраняет результат выражения в bypass. |
| 30 | <code>    flow = finite(discharge_m3_s, 'Discharge flow', positive=True)</code> | Сохраняет результат выражения в flow. |
| 31 | <code>    fraction = 1 / (1 + bypass / flow)</code> | Находит долю расхода сброса. Запись через отношение защищает от переполнения суммы больших расходов. |
| 32 | <code>    temperature = finite(ambient + fraction * (discharge - ambient), 'Mixed temperature')</code> | Прибавляет к фоновой температуре долю разницы температур потоков и проверяет конечность результата. |
| 33 | <code>    return {'mixed_c': temperature, 'rise_c': temperature - ambient,</code> | Возвращает результат вызывающему коду; исходные данные не изменяются. |
| 34 | <code>            'discharge_fraction': fraction}</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 37 | <code>def closed_volume_rise(volume_m3, recirculation_m3_s, system_delta_c, hours):</code> | Рассчитывает изменение средней температуры замкнутого перемешанного объёма. |
| 38 | <code>    """Adiabatic fixed-volume recirculation box, constant heat input, no added water."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 39 | <code>    volume = finite(volume_m3, 'Water volume', positive=True)</code> | Сохраняет результат выражения в volume. |
| 40 | <code>    flow = finite(recirculation_m3_s, 'Recirculation flow', minimum=0)</code> | Сохраняет результат выражения в flow. |
| 41 | <code>    delta = finite(system_delta_c, 'Cooling-system temperature rise')</code> | Сохраняет результат выражения в delta. |
| 42 | <code>    duration = finite(hours, 'Duration', minimum=0)</code> | Сохраняет результат выражения в duration. |
| 43 | <code>    # Equal constant water density and heat capacity cancel in the heat balance.</code> | Комментарий объясняет допущение; Python его не выполняет. |
| 44 | <code>    return finite(flow * delta * duration * 3600 / volume, 'Volume-average change')</code> | Умножает расход на постоянную ΔT и время в секундах, делит на объём; плотность и теплоёмкость сокращаются. |
| 47 | <code>def lifecycle_tonnes(generation_twh, factor_g_per_kwh):</code> | Переводит выработку и удельный коэффициент жизненного цикла в тонны CO2e. |
| 48 | <code>    """Electricity × literature intensity; TWh→kWh (1e9), grams→tonnes (1e-6)."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 49 | <code>    generation = finite(generation_twh, 'Electricity generation', minimum=0)</code> | Сохраняет результат выражения в generation. |
| 50 | <code>    factor = finite(factor_g_per_kwh, 'Lifecycle intensity', minimum=0)</code> | Сохраняет результат выражения в factor. |
| 51 | <code>    return finite(generation * factor * 1000, 'Lifecycle scenario total')</code> | Учитывает 10^9 кВт·ч в ТВт·ч и 10^6 граммов в тонне: общий множитель 1000. |
| 54 | <code>def reference_difference(temperature_c, reference_c):</code> | Сравнивает число с введённым ориентиром без вывода о безопасности. |
| 55 | <code>    """Arithmetic relative to a user-supplied reference, never a safety verdict."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 56 | <code>    return finite(finite(temperature_c, 'Temperature', minimum=-273.15) - finite(</code> | Возвращает результат вызывающему коду; исходные данные не изменяются. |
| 57 | <code>        reference_c, 'Reference temperature', minimum=-273.15), 'Reference difference')</code> | Продолжает аргументы или выражение предыдущей команды. |

## src/ui/impact_panel.py

| Строка | Код | Объяснение |
| --- | --- | --- |
| 1 | <code>"""Optional impact scenarios: explicit inputs, assumptions and evidence gaps."""</code> | Описание назначения модуля или функции; не вычислительная команда. |
| 2 | <code>import streamlit as st</code> | Подключает указанные функции или модуль; само подключение не запускает обучение. |
| 4 | <code>from src.fuel.scenarios import (</code> | Подключает указанные функции или модуль; само подключение не запускает обучение. |
| 5 | <code>    IPCC_URL, IPCC_NUCLEAR_G_PER_KWH, mixed_stream,</code> | Продолжает аргументы или выражение предыдущей команды. |
| 6 | <code>    closed_volume_rise, lifecycle_tonnes, reference_difference,</code> | Продолжает аргументы или выражение предыдущей команды. |
| 7 | <code>)</code> | Закрывает многострочное выражение выше. |
| 9 | <code>EPA_THERMAL = 'https://www.epa.gov/system/files/documents/2023-07/Thermal-Discharges-Report.pdf'</code> | Сохраняет результат выражения в EPA_THERMAL. |
| 10 | <code>EPA_ECOLOGY = 'https://www.epa.gov/caddis/temperature'</code> | Сохраняет результат выражения в EPA_ECOLOGY. |
| 13 | <code>def blank_number(label, key, *, minimum=None, help=None):</code> | Создаёт числовое поле без выдуманного начального значения. |
| 14 | <code>    return st.number_input(label, value=None, min_value=minimum, key=key,</code> | Возвращает введённое пользователем число или None: value=None оставляет поле пустым. |
| 15 | <code>                           placeholder='Enter a scenario input', help=help)</code> | Продолжает аргументы или выражение предыдущей команды. |
| 18 | <code>def impact_panel():</code> | Строит четыре раздела сценариев в интерфейсе. |
| 19 | <code>    st.subheader('Explore possible impacts — with explicit assumptions')</code> | Выводит заголовок раздела. |
| 20 | <code>    st.warning('Scenario calculations, not measured impacts or a safety assessment. '</code> | Показывает ограничение или предупреждение; это не результат оценки безопасности. |
| 21 | <code>               'These inputs are independent of the selected station. No saved ML result is changed.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 22 | <code>    mixing, volume, climate, ecology = st.tabs([</code> | Сохраняет результат выражения в (mixing, volume, climate, ecology). |
| 23 | <code>        'Mixing', 'Water-body heat balance', 'Lifecycle emissions', 'Ecological evidence'])</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 24 | <code>    with mixing:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 25 | <code>        st.markdown('**Two-stream mixing scenario**')</code> | Выводит подпись, список или ссылку на источник. |
| 26 | <code>        st.write('Estimate the temperature after complete mixing of a discharge and a separate ambient stream. '</code> | Выводит пояснение или вычисленный результат. |
| 27 | <code>                 'This is neither a spatial plume model nor the temperature of an entire sea or lake.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 28 | <code>        left, right = st.columns(2)</code> | Сохраняет результат выражения в (left, right). |
| 29 | <code>        with left:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 30 | <code>            ambient = blank_number('Ambient water temperature, °C', 'mix_ambient', minimum=-273.15)</code> | Сохраняет результат выражения в ambient. |
| 31 | <code>            bypass = blank_number('Ambient bypass flow, m³/s', 'mix_bypass', minimum=0.0,</code> | Сохраняет результат выражения в bypass. |
| 32 | <code>                                  help='Flow reaching the mixing point EXCLUDING the discharged water. Do not double-count a withdrawal/return.')</code> | Продолжает аргументы или выражение предыдущей команды. |
| 33 | <code>        with right:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 34 | <code>            discharge = blank_number('Discharge temperature, °C', 'mix_discharge', minimum=-273.15)</code> | Сохраняет результат выражения в discharge. |
| 35 | <code>            flow = blank_number('Discharge flow, m³/s', 'mix_flow', minimum=0.0)</code> | Сохраняет результат выражения в flow. |
| 36 | <code>        if all(x is not None for x in (ambient, discharge, bypass, flow)):</code> | Выполняет следующий блок только при условии all((x is not None for x in (ambient, discharge, bypass, flow))). |
| 37 | <code>            try:</code> | Начинает операцию, ошибки которой будут обработаны ниже. |
| 38 | <code>                result = mixed_stream(ambient, discharge, bypass, flow)</code> | Сохраняет результат выражения в result. |
| 39 | <code>            except ValueError as exc:</code> | Перехватывает указанную ошибку; приложение сообщает о проблеме вместо неверного результата. |
| 40 | <code>                st.error(str(exc))</code> | Показывает ошибку ввода. |
| 41 | <code>            else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 42 | <code>                st.success(f"Scenario mixed temperature: {result['mixed_c']:.2f} °C; "</code> | Показывает успешно рассчитанное число, а не безопасность объекта. |
| 43 | <code>                           f"change from ambient: {result['rise_c']:+.2f} °C.")</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 44 | <code>        else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 45 | <code>            st.info('Enter all four inputs to calculate. Missing site flow is not inferred from ΔT.')</code> | Показывает нейтральное пояснение или запрос недостающих данных. |
| 46 | <code>        st.latex(r'T_{mix}=\frac{Q_aT_a+Q_dT_d}{Q_a+Q_d}')</code> | Показывает формулу; сам расчёт выполняется в scenarios.py. |
| 47 | <code>        st.caption('Assumes synchronous steady flows, complete mixing, equal constant density/heat capacity, '</code> | Показывает дополнительные допущения мелким текстом. |
| 48 | <code>                   'no atmospheric heat exchange, evaporation, stratification, tides or recirculation. '</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 49 | <code>                   'Monthly average flow × monthly average temperature does not generally equal mean heat flux.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 50 | <code>        st.markdown(f'[EPA: thermal discharge modelling and mixing]({EPA_THERMAL})')</code> | Выводит подпись, список или ссылку на источник. |
| 51 | <code>    with volume:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 52 | <code>        st.markdown('**Idealized average heating of a closed water volume**')</code> | Выводит подпись, список или ссылку на источник. |
| 53 | <code>        st.write('A fixed, perfectly mixed freshwater volume is circulated through a cooler that adds a constant ΔT. '</code> | Выводит пояснение или вычисленный результат. |
| 54 | <code>                 'All circulated water returns; this is not a model with an additional incoming discharge volume.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 55 | <code>        left, right = st.columns(2)</code> | Сохраняет результат выражения в (left, right). |
| 56 | <code>        with left:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 57 | <code>            amount = blank_number('Water volume, m³', 'box_volume', minimum=0.0)</code> | Сохраняет результат выражения в amount. |
| 58 | <code>            circulation = blank_number('Recirculated cooling flow, m³/s', 'box_flow', minimum=0.0)</code> | Сохраняет результат выражения в circulation. |
| 59 | <code>        with right:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 60 | <code>            delta = blank_number('Constant system ΔT, °C', 'box_delta')</code> | Сохраняет результат выражения в delta. |
| 61 | <code>            hours = blank_number('Duration, hours', 'box_hours', minimum=0.0)</code> | Сохраняет результат выражения в hours. |
| 62 | <code>        if all(x is not None for x in (amount, circulation, delta, hours)):</code> | Выполняет следующий блок только при условии all((x is not None for x in (amount, circulation, delta, hours))). |
| 63 | <code>            try:</code> | Начинает операцию, ошибки которой будут обработаны ниже. |
| 64 | <code>                rise = closed_volume_rise(amount, circulation, delta, hours)</code> | Сохраняет результат выражения в rise. |
| 65 | <code>            except ValueError as exc:</code> | Перехватывает указанную ошибку; приложение сообщает о проблеме вместо неверного результата. |
| 66 | <code>                st.error(str(exc))</code> | Показывает ошибку ввода. |
| 67 | <code>            else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 68 | <code>                st.success(f'Idealized volume-average temperature change: {rise:+.3f} °C.')</code> | Показывает успешно рассчитанное число, а не безопасность объекта. |
| 69 | <code>        else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 70 | <code>            st.info('Enter volume, circulation, system ΔT and duration. No site volume or circulation is assumed.')</code> | Показывает нейтральное пояснение или запрос недостающих данных. |
| 71 | <code>        st.latex(r'\Delta T_{body}=\frac{Q_c\,\Delta T_{system}\,t}{V},\quad t\text{ in seconds}')</code> | Показывает формулу; сам расчёт выполняется в scenarios.py. |
| 72 | <code>        st.warning('No heat losses or natural inflows/outflows, constant water properties and heat input. '</code> | Показывает ограничение или предупреждение; это не результат оценки безопасности. |
| 73 | <code>                   'Long-duration results may be physically unrealistic. This is not a validated prediction '</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 74 | <code>                   'or a general upper bound for a real water body; other heat inputs also exist.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 75 | <code>    with climate:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 76 | <code>        st.markdown('**Electricity-generation lifecycle scenario**')</code> | Выводит подпись, список или ссылку на источник. |
| 77 | <code>        generation = blank_number('Electricity generation over your chosen period, TWh', 'lca_generation', minimum=0.0)</code> | Сохраняет результат выражения в generation. |
| 78 | <code>        st.write('IPCC AR5 (2014), Annex III, Table A.III.2 reports nuclear lifecycle intensities '</code> | Выводит пояснение или вычисленный результат. |
| 79 | <code>                 'of 3.7 / 12 / 110 g CO₂e per kWh (literature minimum / median / maximum).')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 80 | <code>        st.caption('A dated cross-study literature range, not a confidence interval, a station-specific factor '</code> | Показывает дополнительные допущения мелким текстом. |
| 81 | <code>                   'or direct measured stack emissions. It includes the lifecycle, not only mining/milling. '</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 82 | <code>                   'Do not add a separate mining estimate to this total.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 83 | <code>        if generation is not None:</code> | Выполняет следующий блок только при условии generation is not None. |
| 84 | <code>            try:</code> | Начинает операцию, ошибки которой будут обработаны ниже. |
| 85 | <code>                values = [lifecycle_tonnes(generation, factor) for factor in IPCC_NUCLEAR_G_PER_KWH]</code> | Сохраняет результат выражения в values. |
| 86 | <code>            except ValueError as exc:</code> | Перехватывает указанную ошибку; приложение сообщает о проблеме вместо неверного результата. |
| 87 | <code>                st.error(str(exc))</code> | Показывает ошибку ввода. |
| 88 | <code>            else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 89 | <code>                st.write(f'Scenario total for the entered period: **{values[1]:,.1f} t CO₂e** at the literature median; '</code> | Выводит пояснение или вычисленный результат. |
| 90 | <code>                         f'**{values[0]:,.1f}–{values[2]:,.1f} t CO₂e** using the literature endpoints.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 91 | <code>        else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 92 | <code>            st.info('Enter generation to calculate. Plant generation is not inferred from cooling-system temperature.')</code> | Показывает нейтральное пояснение или запрос недостающих данных. |
| 93 | <code>        st.latex(r'E_{tCO_2e}=G_{TWh}\times I_{gCO_2e/kWh}\times 1000')</code> | Показывает формулу; сам расчёт выполняется в scenarios.py. |
| 94 | <code>        st.markdown(f'[IPCC AR5 final Annex III, Table A.III.2]({IPCC_URL})')</code> | Выводит подпись, список или ссылку на источник. |
| 95 | <code>    with ecology:</code> | Помещает следующие элементы в указанную вкладку или колонку Streamlit. |
| 96 | <code>        st.markdown('**Thermal reference comparison and evidence needs**')</code> | Выводит подпись, список или ссылку на источник. |
| 97 | <code>        st.write('A reference comparison can flag a question to investigate. It cannot establish '</code> | Выводит пояснение или вычисленный результат. |
| 98 | <code>                 'ecological harm, causation, legal compliance or human health safety.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 99 | <code>        temp = blank_number('Temperature being screened, °C', 'eco_temperature', minimum=-273.15)</code> | Сохраняет результат выражения в temp. |
| 100 | <code>        limit = blank_number('Your applicable temperature reference, °C', 'eco_reference', minimum=-273.15)</code> | Сохраняет результат выражения в limit. |
| 101 | <code>        source = st.text_input('Reference document / URL, species, season and averaging period', key='eco_source')</code> | Сохраняет результат выражения в source. |
| 102 | <code>        appropriate = st.checkbox('I have checked that the reference matches the water type, species, season and time basis.', key='eco_appropriate')</code> | Сохраняет результат выражения в appropriate. |
| 103 | <code>        if temp is not None and limit is not None and source.strip() and appropriate:</code> | Выполняет следующий блок только при условии temp is not None and limit is not None and source.strip() and appropriate. |
| 104 | <code>            difference = reference_difference(temp, limit)</code> | Сохраняет результат выражения в difference. |
| 105 | <code>            if difference &gt; 0:</code> | Выполняет следующий блок только при условии difference > 0. |
| 106 | <code>                st.warning(f'{difference:.2f} °C above the entered reference. Investigate with suitable site evidence.')</code> | Показывает ограничение или предупреждение; это не результат оценки безопасности. |
| 107 | <code>            elif difference &lt; 0:</code> | Выполняет следующий блок только при условии difference < 0. |
| 108 | <code>                st.info(f'{abs(difference):.2f} °C below the entered reference. This does not demonstrate safety.')</code> | Показывает нейтральное пояснение или запрос недостающих данных. |
| 109 | <code>            else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 110 | <code>                st.info('Equal to the entered reference. Equality does not demonstrate safety.')</code> | Показывает нейтральное пояснение или запрос недостающих данных. |
| 111 | <code>            st.caption('Reference supplied by the user; the app has not verified its authority or applicability. '</code> | Показывает дополнительные допущения мелким текстом. |
| 112 | <code>                       'A scenario temperature remains a scenario. Monthly means cannot test instantaneous maxima.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 113 | <code>        else:</code> | Ветка для случая, когда предыдущее условие не выполнилось либо try завершился без ошибки. |
| 114 | <code>            st.info('Comparison needs both temperatures, a documented reference and an applicability check. '</code> | Показывает нейтральное пояснение или запрос недостающих данных. |
| 115 | <code>                    'No universal safe temperature is supplied.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 116 | <code>        st.markdown('**For a real site investigation, collect:**')</code> | Выводит подпись, список или ссылку на источник. |
| 117 | <code>        st.markdown('- Matched upstream/downstream temperatures, locations, depths and exposure duration.\n'</code> | Выводит подпись, список или ссылку на источник. |
| 118 | <code>                    '- Discharge and receiving-water flows, geometry, tides and meteorology.\n'</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 119 | <code>                    '- Species/life stages, season, baseline ecology and biological observations.\n'</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 120 | <code>                    '- Dissolved oxygen, water chemistry and other potential stressors.\n'</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 121 | <code>                    '- Applicable monitoring and permit documents interpreted by a qualified specialist.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 122 | <code>        st.warning('Human health, radiological safety and overall plant safety are not assessed by this module. '</code> | Показывает ограничение или предупреждение; это не результат оценки безопасности. |
| 123 | <code>                   'They require separate exposure, monitoring and specialist evidence.')</code> | Продолжение поясняющего текста или набора строк из выражения выше; нового расчёта нет. |
| 124 | <code>        st.markdown(f'[EPA CADDIS: temperature as a candidate ecological stressor]({EPA_ECOLOGY})')</code> | Выводит подпись, список или ссылку на источник. |
