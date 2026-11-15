"""Optional impact scenarios: explicit inputs, assumptions and evidence gaps."""
import streamlit as st

from src.fuel.scenarios import (
    IPCC_URL, IPCC_NUCLEAR_G_PER_KWH, mixed_stream,
    closed_volume_rise, lifecycle_tonnes, reference_difference,
)

EPA_THERMAL = 'https://www.epa.gov/system/files/documents/2023-07/Thermal-Discharges-Report.pdf'
EPA_ECOLOGY = 'https://www.epa.gov/caddis/temperature'


def blank_number(label, key, *, minimum=None, help=None):
    return st.number_input(label, value=None, min_value=minimum, key=key,
                           placeholder='Enter a scenario input', help=help)


def impact_panel():
    st.subheader('Explore possible impacts — with explicit assumptions')
    st.warning('Scenario calculations, not measured impacts or a safety assessment. '
               'These inputs are independent of the selected station. No saved ML result is changed.')
    mixing, volume, climate, ecology = st.tabs([
        'Mixing', 'Water-body heat balance', 'Lifecycle emissions', 'Ecological evidence'])
    with mixing:
        st.markdown('**Two-stream mixing scenario**')
        st.write('Estimate the temperature after complete mixing of a discharge and a separate ambient stream. '
                 'This is neither a spatial plume model nor the temperature of an entire sea or lake.')
        left, right = st.columns(2)
        with left:
            ambient = blank_number('Ambient water temperature, °C', 'mix_ambient', minimum=-273.15)
            bypass = blank_number('Ambient bypass flow, m³/s', 'mix_bypass', minimum=0.0,
                                  help='Flow reaching the mixing point EXCLUDING the discharged water. Do not double-count a withdrawal/return.')
        with right:
            discharge = blank_number('Discharge temperature, °C', 'mix_discharge', minimum=-273.15)
            flow = blank_number('Discharge flow, m³/s', 'mix_flow', minimum=0.0)
        if all(x is not None for x in (ambient, discharge, bypass, flow)):
            try:
                result = mixed_stream(ambient, discharge, bypass, flow)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success(f"Scenario mixed temperature: {result['mixed_c']:.2f} °C; "
                           f"change from ambient: {result['rise_c']:+.2f} °C.")
        else:
            st.info('Enter all four inputs to calculate. Missing site flow is not inferred from ΔT.')
        st.latex(r'T_{mix}=\frac{Q_aT_a+Q_dT_d}{Q_a+Q_d}')
        st.caption('Assumes synchronous steady flows, complete mixing, equal constant density/heat capacity, '
                   'no atmospheric heat exchange, evaporation, stratification, tides or recirculation. '
                   'Monthly average flow × monthly average temperature does not generally equal mean heat flux.')
        st.markdown(f'[EPA: thermal discharge modelling and mixing]({EPA_THERMAL})')
    with volume:
        st.markdown('**Idealized average heating of a closed water volume**')
        st.write('A fixed, perfectly mixed freshwater volume is circulated through a cooler that adds a constant ΔT. '
                 'All circulated water returns; this is not a model with an additional incoming discharge volume.')
        left, right = st.columns(2)
        with left:
            amount = blank_number('Water volume, m³', 'box_volume', minimum=0.0)
            circulation = blank_number('Recirculated cooling flow, m³/s', 'box_flow', minimum=0.0)
        with right:
            delta = blank_number('Constant system ΔT, °C', 'box_delta')
            hours = blank_number('Duration, hours', 'box_hours', minimum=0.0)
        if all(x is not None for x in (amount, circulation, delta, hours)):
            try:
                rise = closed_volume_rise(amount, circulation, delta, hours)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success(f'Idealized volume-average temperature change: {rise:+.3f} °C.')
        else:
            st.info('Enter volume, circulation, system ΔT and duration. No site volume or circulation is assumed.')
        st.latex(r'\Delta T_{body}=\frac{Q_c\,\Delta T_{system}\,t}{V},\quad t\text{ in seconds}')
        st.warning('No heat losses or natural inflows/outflows, constant water properties and heat input. '
                   'Long-duration results may be physically unrealistic. This is not a validated prediction '
                   'or a general upper bound for a real water body; other heat inputs also exist.')
    with climate:
        st.markdown('**Electricity-generation lifecycle scenario**')
        generation = blank_number('Electricity generation over your chosen period, TWh', 'lca_generation', minimum=0.0)
        st.write('IPCC AR5 (2014), Annex III, Table A.III.2 reports nuclear lifecycle intensities '
                 'of 3.7 / 12 / 110 g CO₂e per kWh (literature minimum / median / maximum).')
        st.caption('A dated cross-study literature range, not a confidence interval, a station-specific factor '
                   'or direct measured stack emissions. It includes the lifecycle, not only mining/milling. '
                   'Do not add a separate mining estimate to this total.')
        if generation is not None:
            try:
                values = [lifecycle_tonnes(generation, factor) for factor in IPCC_NUCLEAR_G_PER_KWH]
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.write(f'Scenario total for the entered period: **{values[1]:,.1f} t CO₂e** at the literature median; '
                         f'**{values[0]:,.1f}–{values[2]:,.1f} t CO₂e** using the literature endpoints.')
        else:
            st.info('Enter generation to calculate. Plant generation is not inferred from cooling-system temperature.')
        st.latex(r'E_{tCO_2e}=G_{TWh}\times I_{gCO_2e/kWh}\times 1000')
        st.markdown(f'[IPCC AR5 final Annex III, Table A.III.2]({IPCC_URL})')
    with ecology:
        st.markdown('**Thermal reference comparison and evidence needs**')
        st.write('A reference comparison can flag a question to investigate. It cannot establish '
                 'ecological harm, causation, legal compliance or human health safety.')
        temp = blank_number('Temperature being screened, °C', 'eco_temperature', minimum=-273.15)
        limit = blank_number('Your applicable temperature reference, °C', 'eco_reference', minimum=-273.15)
        source = st.text_input('Reference document / URL, species, season and averaging period', key='eco_source')
        appropriate = st.checkbox('I have checked that the reference matches the water type, species, season and time basis.', key='eco_appropriate')
        if temp is not None and limit is not None and source.strip() and appropriate:
            difference = reference_difference(temp, limit)
            if difference > 0:
                st.warning(f'{difference:.2f} °C above the entered reference. Investigate with suitable site evidence.')
            elif difference < 0:
                st.info(f'{abs(difference):.2f} °C below the entered reference. This does not demonstrate safety.')
            else:
                st.info('Equal to the entered reference. Equality does not demonstrate safety.')
            st.caption('Reference supplied by the user; the app has not verified its authority or applicability. '
                       'A scenario temperature remains a scenario. Monthly means cannot test instantaneous maxima.')
        else:
            st.info('Comparison needs both temperatures, a documented reference and an applicability check. '
                    'No universal safe temperature is supplied.')
        st.markdown('**For a real site investigation, collect:**')
        st.markdown('- Matched upstream/downstream temperatures, locations, depths and exposure duration.\n'
                    '- Discharge and receiving-water flows, geometry, tides and meteorology.\n'
                    '- Species/life stages, season, baseline ecology and biological observations.\n'
                    '- Dissolved oxygen, water chemistry and other potential stressors.\n'
                    '- Applicable monitoring and permit documents interpreted by a qualified specialist.')
        st.warning('Human health, radiological safety and overall plant safety are not assessed by this module. '
                   'They require separate exposure, monitoring and specialist evidence.')
        st.markdown(f'[EPA CADDIS: temperature as a candidate ecological stressor]({EPA_ECOLOGY})')
