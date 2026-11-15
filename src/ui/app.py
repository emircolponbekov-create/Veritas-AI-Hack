"""Read-only Streamlit UI for one registered cooling system at a time."""
import sys
import logging
from html import escape
from pathlib import Path
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_loader import history_chart, METHOD_LABELS
from multistation_loader import ROOT, registry_snapshot, measurements_snapshot, verified_results
from water_scene import hero_html, install_motion, water_chart
from impact_panel import impact_panel
from environment_panel import environment_panel, report_method_panel
from exploration_panel import availability, support_call, journey_panel, month_panel

LOG = logging.getLogger(__name__)

REASONS = {
    'mixed_site_nuclear_attribution_unconfirmed': 'Mixed-site attribution to nuclear generation is unconfirmed.',
    'no_complete_pairs': 'No complete intake/discharge temperature pairs are available.',
    'no_explicit_measured_pairs': 'No pairs have an explicitly measured source method.',
    'suspect_measured_rows_retained_no_automatic_exclusion': 'Suspect reported measurements were retained and require review.',
    'cooling_scheme_semantics_require_review': 'Intake/discharge meaning for this cooling scheme requires review.',
    'fixed_time_coverage_insufficient': 'Insufficient coverage of the fixed train/validation/test periods.',
    'recirculating_mixed_or_unknown_cooling_codes': 'Recirculating, mixed or unknown cooling metadata limits interpretation.',
    'missing_temperatures_retained_and_ineligible': 'Missing temperatures were retained and are ineligible.',
    'reported_measurement_not_independent_sensor_validation': 'Source-reported measurements; no independent sensor validation.',
    'historical_monthly_retrospective_only_no_ecosystem_inference': 'Historical monthly records; no ecosystem conclusions.',
    'historical_cooling_metadata_incomplete_or_changed': 'Historical cooling metadata may be incomplete or changed.',
}


def source_panel(entry):
    with st.expander('Source, identifiers and limitations', expanded=entry['status'] != 'ready_for_model_check'):
        source = entry['provenance']
        st.markdown(f"[Source snapshot URL]({source['source_url']})")
        st.write(f"Original units: {source['source_units']}; display: {source['units']}. Celsius = (Fahrenheit - 32) × 5/9.")
        st.write(f"Reuse: {source['license']}")
        with st.expander('Technical provenance'):
            st.write(f"Dataset: {entry['dataset_id']} | Data: {entry['status']} | Model: {entry['model_status']}")
            st.write(f"Local observations: {entry['observations']['path']}")
            st.write(f"Source table: {source['table']}")
            st.caption(f"Frozen source SHA-256: {source['raw_sha256']}. The nightly URL may serve a newer snapshot.")
        for reason in entry['limitations']:
            st.write('- ' + REASONS.get(reason, reason.replace('_', ' ')))
        if entry['review_months']:
            st.write('Months requiring review (not silently removed):')
            st.json(entry['review_months'], expanded=False)


def model_panel(entry, measurements, month, token, root):
    st.subheader('How well does the model estimate ΔT?')
    st.caption('A retrospective estimate using intake temperature and season. Same-month intake is known after the month; publication can lag.')
    if measurements is None or entry['status'] != 'ready_for_model_check' or entry['model_status'] == 'not_trained':
        st.info('Model not ready')
        return
    try:
        results, scores = verified_results(entry, measurements, token, root)
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        st.info('Model not ready')
        LOG.warning('Saved comparison unavailable: %s', type(exc).__name__)
        st.warning('Saved results are temporarily unavailable or need review. Refresh data to retry.')
        return
    if month in results.index:
        row = results.loc[month]
        cols = st.columns(2)
        cols[0].metric('Model estimate of ΔT, °C', f'{row.model_delta_t_c:.2f}')
        cols[1].metric('Absolute error for this month, °C', f'{abs(row.model_delta_t_c - row.reported_delta_t_c):.2f}')
    else:
        st.info('No model estimate for this month')
    st.markdown('**Held-out test comparison for this system**')
    st.caption(f'{len(results)} identical eligible test months: {results.index.min()} to {results.index.max()}. MAE recalculated from CSV; lower is better. Baselines: train 2010–2021 only. Model selection: validation 2022–2023.')
    st.dataframe(pd.DataFrame({'Method': list(METHOD_LABELS.values()),
                              'MAE (°C)': [scores[field] for field in METHOD_LABELS],
                              'Test months': len(results)}), hide_index=True, width='stretch',
                 column_config={'MAE (°C)': st.column_config.NumberColumn(format='%.3f')})
    difference = scores['model_delta_t_c'] - min(scores['median_baseline_delta_t_c'], scores['seasonal_baseline_delta_t_c'])
    comparison = 'worse' if difference > 0 else 'better'
    st.write(f'Model MAE is {comparison} than the best simple baseline by {abs(difference):.3f} °C.' if difference else 'Model MAE equals the best simple baseline.')
    chart = results[['reported_delta_t_c', *METHOD_LABELS]].copy()
    chart.index = pd.to_datetime(chart.index)
    chart = chart.reindex(pd.date_range(chart.index.min(), chart.index.max(), freq='MS'))
    water_chart(chart.rename(columns={'reported_delta_t_c': 'Reported measurement', **METHOD_LABELS}),
                  x_label='Test month', y_label='Cooling-system ΔT (°C)', height=300,
                  color=['#70eee4', '#a6b8c6', '#ffc86b', '#c3a1ff'], selected_month=month)
    worst_month = (results.model_delta_t_c - results.reported_delta_t_c).abs().idxmax()
    worst = results.loc[worst_month]
    with st.expander('A closer look: largest model error'):
        st.write(f'{worst_month}: reported ΔT {worst.reported_delta_t_c:.2f} °C; '
                 f'model estimate {worst.model_delta_t_c:.2f} °C; '
                 f'absolute error {abs(worst.model_delta_t_c - worst.reported_delta_t_c):.2f} °C.')
        st.caption('One example from this historical test. Small MAE differences do not establish statistical significance.')


def render_technical(entry, identifier, plant_id, token, root, publication, month):
    status_label = {'ready_for_model_check': 'Measured records available', 'measurements_only': 'Measurements with limitations',
                    'review_required': 'Data review required', 'blocked': 'Data unavailable', 'reference_only': 'Reference only'}
    st.markdown(f'<div class="lab-context"><h2>{escape(entry["plant_name"])}</h2>'
                f'<p>System {escape(str(entry["cooling_id_eia"]))} &nbsp; · &nbsp; EIA {plant_id}'
                f' &nbsp; · &nbsp; {status_label.get(entry["status"], "See source details")}</p></div>', unsafe_allow_html=True)
    measurements = None
    if entry['status'] in {'blocked', 'reference_only'}:
        st.warning('Temperature data unavailable for confirmed measurement display. See reasons above; no numbers are substituted.')
    elif entry['status'] == 'review_required':
        st.error('Data review required. Unresolved suspect measurements: temperature cards and model comparisons are withheld pending review.')
    else:
        try:
            measurements, audit = measurements_snapshot(entry, token, root)
        except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
            LOG.warning('Technical measurements unavailable: %s', type(exc).__name__)
            st.warning('Measured data are temporarily unavailable or need review. Refresh data to retry.')
        else:
            if measurements.empty:
                st.warning('No eligible measured temperature pairs are available.')
            else:
                months = measurements.report_month.tolist()
    st.markdown('<div class="lab-note"><b>Read this difference correctly.</b> ΔT = discharge − intake temperature across the cooling system. '
                'It is not the heating of the whole water body.</div>', unsafe_allow_html=True)
    overview, performance, evidence, impacts = st.tabs(['Water overview', 'Model performance', 'Sources & context', 'Impact scenarios'])
    with overview:
        st.subheader('The historical picture')
        st.caption('Reported monthly cooling-system ΔT · explore the trend, not an environmental safety score.')
        if measurements is not None and not measurements.empty:
            water_chart(history_chart(measurements).rename(columns={'reported_delta_t_c': 'Reported measurement'}),
                          x_label='Reporting month', y_label='Cooling-system ΔT (°C)', height=330, color=['#70eee4'], selected_month=month)
            temperatures = measurements.set_index('report_month')[['intake_temperature_c', 'discharge_temperature_c']].copy()
            temperatures.index = pd.to_datetime(temperatures.index)
            temperatures = temperatures.reindex(pd.date_range(temperatures.index.min(), temperatures.index.max(), freq='MS'))
            st.subheader('Intake & discharge temperature')
            st.caption(f'Selected month: {month}. Source-reported monthly averages; gaps remain unavailable.')
            water_chart(temperatures.rename(columns={'intake_temperature_c': 'Measured intake', 'discharge_temperature_c': 'Measured discharge'}),
                          x_label='Reporting month', y_label='Temperature (°C)', height=270, color=['#70eee4', '#ffc86b'], selected_month=month)
            st.caption(f"{audit['eligible']} eligible months out of {audit['total']} rows · {months[0]} to {months[-1]}. Gaps are unavailable/excluded months, not zero. Rounding does not imply sensor precision.")
            with st.expander('Excluded months and split coverage'):
                st.write(', '.join(audit['excluded']) or 'None')
                st.write(entry['split_counts'])
        else:
            st.info('No confirmed measurement series to display. See Sources & context for limitations.')
        st.markdown('<div id="measurement-context" class="lab-eyebrow">02 / Ecosystem context</div>', unsafe_allow_html=True)
        left, right = st.columns(2)
        with left:
            st.subheader('What we know')
            st.write('Eligible records describe source-reported monthly intake and discharge temperatures for the selected system. Saved estimates are checked against that system and its test months.')
        with right:
            st.subheader("What we don't know")
            st.write('These records cannot establish harm or safety for people, animals or plants. Monthly averages do not describe local peaks, mixing or downstream temperatures. Results do not automatically apply to Akkuyu or another system.')
    with performance:
        model_panel(entry, measurements, month, token, root)
    with evidence:
        st.subheader('Evidence behind this view')
        st.caption('EIA Form 923 · distributed by Catalyst Cooperative PUDL. Historical records, not live monitoring.')
        st.markdown('[Open data & methodology](#measurement-methods)')
    with impacts:
        impact_panel()
    st.markdown('<section id="measurement-methods" class="section-heading"><div class="lab-eyebrow">04 / Data &amp; methodology</div>'
                '<h2>Follow the evidence.</h2><p>Reported measurements and saved model estimates are kept separate. '
                'Explore the source, reporting method and limits for this cooling system.</p></section>', unsafe_allow_html=True)
    source_panel(entry)
    st.markdown('<section id="scenario-context" class="lab-note"><div class="lab-eyebrow">03 / Climate &amp; emissions</div><h3>Explore explicit scenarios</h3>'
                'Open Impact scenarios for idealized mixing and water-volume heat balances, a literature-based lifecycle '
                'emissions scenario and an ecological evidence checklist. Inputs are independent of the selected station. '
                'These calculations do not establish site impacts, legal compliance or safety.</section>', unsafe_allow_html=True)
    report_method_panel(publication)


def select_surry():
    st.session_state['plant'] = 3806


def story_support(root):
    """Revalidate the MODEL snapshot; never cache a provider across reruns."""
    try:
        from src.model.site_support import SiteSupport, read_catalog
        provider = SiteSupport(root)
        try:
            catalog = read_catalog(root)
        except (OSError, ValueError, KeyError, TypeError):
            catalog = provider.catalog()
        return provider, catalog
    except (OSError, ValueError, KeyError, TypeError, ImportError):
        LOG.warning('Story-support catalog unavailable')
        return None, None


def render(root=ROOT):
    st.set_page_config(page_title='Nuclear Water & Climate Lab', page_icon='🌊', layout='wide')
    st.markdown('<style>' + Path(__file__).with_name('style.css').read_text(encoding='utf-8') + '</style>', unsafe_allow_html=True)
    reduced = st.session_state.get('reduce_motion', False)
    st.html(hero_html(reduced))
    try:
        registry, token = registry_snapshot(root)
    except (OSError, ValueError, KeyError, TypeError):
        st.error('The station catalog is temporarily unavailable. Refresh the page to retry.')
        install_motion(reduced)
        return
    entries = registry['datasets']
    plants = {e['plant_id_eia']: e['plant_name'] for e in entries}
    ids = sorted(plants, key=lambda plant: (plants[plant], plant))
    if not ids:
        st.warning('No registered systems are available.')
        install_motion(reduced)
        return
    provider, catalog = story_support(root)
    plant_flags = {row['plant_id_eia']: row for row in catalog['plants']} if catalog else {}
    system_flags = {row['dataset_id']: row for row in catalog['systems']} if catalog else {}
    st.markdown('<div id="explore-water" class="lab-eyebrow">01 / Start with a station</div>', unsafe_allow_html=True)
    st.subheader('What does the evidence tell us?')
    st.write('Start with Surry: explore a source-based environmental report, follow the cooling process, then browse historical water measurements. Other sites have different evidence coverage.')
    site_column, settings = st.columns([3, 1], vertical_alignment='bottom')
    plant_id = site_column.selectbox('Plant site — available materials', ids, index=ids.index(3806) if 3806 in ids else 0,
        format_func=lambda plant: plants[plant] + ' · ' + availability(plant_flags.get(plant)), key='plant')
    with settings:
        reduced = st.toggle('Reduce decorative motion', key='reduce_motion', help='Turns off decorative movement and fades. Your operating system’s reduced-motion setting is always respected.')
        st.button('Refresh data', help='Reread verified files. No training or external source search.', width='stretch')
    st.caption(availability(plant_flags.get(plant_id)) + '. Availability flags may coexist; they are not an environmental rating.')
    if catalog:
        coverage = plant_flags[plant_id]
        st.caption(f"Measurements: {coverage['verified_measurement_systems']}/{coverage['system_count']} registered systems; saved models: {coverage['verified_model_systems']}/{coverage['system_count']}. This is coverage, not a safety score.")
    if not catalog:
        st.info('Material availability could not be verified. Individual measurement and report readers remain available.')
    if plant_id != 3806:
        st.button('Explore the Surry example', on_click=select_surry)
    systems = sorted([e for e in entries if e['plant_id_eia'] == plant_id], key=lambda e: e['cooling_id_eia'])
    system_ids = [e['dataset_id'] for e in systems]
    default = next((i for i, e in enumerate(systems) if plant_id == 3806 and e['cooling_id_eia'] == 'CW1'), 0)
    with st.expander('Cooling system and measurement coverage'):
        identifier = st.selectbox('Cooling system', system_ids, index=default,
            format_func=lambda value: next(e['cooling_id_eia'] for e in systems if e['dataset_id'] == value) + ' · ' + availability(system_flags.get(value)),
            key=f'system_{plant_id}')
        st.caption('Each system has its own measurements and review status. Site reports and system findings have different scopes.')
    entry = next(e for e in systems if e['dataset_id'] == identifier)
    st.caption(plants[plant_id] + ' · Selected cooling system ' + str(entry['cooling_id_eia']))
    details = support_call(provider, 'claim_details', plant_id, entry['cooling_id_eia'])
    publication = environment_panel(plant_id, entry['cooling_id_eia'], root, details)
    journey_panel(support_call(provider, 'journey', identifier), identifier)
    timeline = support_call(provider, 'timeline', identifier)
    month = month_panel(timeline, identifier)
    st.markdown('<div class="lab-note"><b>The role of AI.</b> Ridge estimates a completed month’s cooling-system temperature difference. '
        'Environmental reports use reviewed sources and rules, not a trained environmental-safety model. No overall safety or environmental score is calculated.</div>', unsafe_allow_html=True)
    st.header('Explore the details', anchor='technical-details')
    st.caption('Saved model comparisons, original measurements, assumptions and explicit user-entered scenarios. Model estimates stay separate from measured temperatures.')
    if st.toggle('Show measurements, model results and scenarios', key='technical_details'):
        with st.container(key='technical_explorer'):
            render_technical(entry, identifier, plant_id, token, root, publication, month)
    st.markdown('<div class="lab-footer">Nuclear Water &amp; Climate Lab / Historical data. Transparent estimates. '
        'No environmental safety ranking.<br>Data: EIA · Catalyst Cooperative PUDL | Built with Streamlit</div>', unsafe_allow_html=True)
    install_motion(reduced)


if __name__ == '__main__':
    render()
