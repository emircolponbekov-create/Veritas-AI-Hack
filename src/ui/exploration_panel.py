"""Small, read-only views over the MODEL story-support contract."""
import base64
import logging
from html import escape
import pandas as pd
import streamlit as st
from water_scene import water_chart

LOG = logging.getLogger(__name__)
MONTH_STATUS = {
    'verified_measurement': 'Verified reported measurement',
    'excluded_method': 'Excluded: reporting method is not an explicit thermometer measurement',
    'missing_temperatures': 'Unavailable: incomplete temperature pair',
    'missing_month': 'Unavailable: no source record for this month',
    'review_required': 'Data review required: values withheld',
    'blocked': 'Unavailable: this dataset is blocked or reference only',
}


def availability(record):
    """Independent availability flags; no score or quality ranking."""
    if record is None:
        return 'Availability could not be verified'
    flags = []
    if record.get('report_state') == 'missing':
        flags.append('No ecological report')
    if record.get('has_substantive_environment_report'):
        flags.append('Environmental report')
    if record.get('has_insufficient_evidence_report'):
        flags.append('Insufficient ecological evidence')
    if record.get('any_system_has_verified_measurements', record.get('has_verified_measurements')):
        flags.append('Measurements')
    if record.get('any_system_has_verified_model_results', record.get('has_verified_model_results')):
        flags.append('Saved model')
    if record.get('any_system_requires_review', record.get('requires_review')) or record.get('report_state') in {'review_required', 'evidence_unavailable'}:
        flags.append('Review needed')
    if record.get('data_blocked') or record.get('no_temperature_pairs'):
        flags.append('No confirmed temperature pairs')
    return ' · '.join(flags) or 'No verified materials yet'


def support_call(provider, method, *args):
    """A failed story feature must not prevent the legacy explorer from loading."""
    if provider is None:
        return None
    try:
        return getattr(provider, method)(*args)
    except (OSError, ValueError, KeyError, TypeError, ImportError):
        LOG.warning('Story support unavailable: %s', method)
        return None


def journey_panel(payload, identifier):
    st.header('Follow a drop', anchor='drop-journey')
    if payload is None:
        st.info('The cooling explanation is temporarily unavailable. Measurements can still be explored below.')
        return
    family = payload['cooling_family']
    family_label = {'once_through': 'Once-through cooling', 'recirculating': 'Recirculating cooling', 'unknown': 'General educational scheme — cooling type unconfirmed'}[family]
    st.caption(family_label + ' · Historical metadata, not a current engineering map.')
    steps = payload['steps']
    stage_ids = [step['id'] for step in steps]
    selected = st.segmented_control('Choose a stage', stage_ids, default=stage_ids[0], required=True,
        format_func=lambda value: str(stage_ids.index(value) + 1) + ' / ' + next(step['title'] for step in steps if step['id'] == value),
        key='journey_' + identifier, wrap=True)
    step = next(step for step in steps if step['id'] == selected)
    # A local illustration uses no spatial data, plume geometry or station imagery.
    loop = '<path d="M340 135 C340 178 230 178 230 135 L230 105 L255 105" fill="none" stroke="#aed7d4" stroke-width="3"/><text x="325" y="184" text-anchor="middle">cool &amp; reuse</text>' if family == 'recirculating' else ''
    labels = ['Intake', 'Heat exchange', 'Conditional release' if family == 'recirculating' else 'Discharge & mixing']
    shapes = [
        '<path d="M55 112q15-16 30 0t30 0t30 0M70 96q15-16 30 0t30 0"/>',
        '<path d="M290 75v55m15-55v55m15-55v55m15-55v55M275 88h80m-80 30h80"/>',
        '<path d="M500 96q15-16 30 0t30 0t30 0M500 118q15-16 30 0t30 0t30 0"/>',
    ]
    nodes = ''.join(f'<g stroke="{("#d0f56f" if i == stage_ids.index(selected) else "#72eee4")}" stroke-width="3" fill="none">{shape}</g><text x="{100+i*220}" y="55" text-anchor="middle">{escape(labels[i])}</text>' for i, shape in enumerate(shapes))
    release_dash = ' stroke-dasharray="5 6"' if family == 'recirculating' else ''
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 200"><g fill="#e7f6f2" font-family="Segoe UI, sans-serif" font-size="16">' + nodes + '<path d="M155 105h100m-10-8 10 8-10 8" fill="none" stroke="#72eee4" stroke-width="2"/><path d="M375 105h100m-10-8 10 8-10 8" fill="none" stroke="#72eee4" stroke-width="2"' + release_dash + '/>' + loop + '</g></svg>'
    image = base64.b64encode(svg.encode()).decode('ascii')
    st.html('<div class="journey-art"><img alt="' + escape('Educational sequence: ' + ' to '.join(labels)) + '" src="data:image/svg+xml;base64,' + image + '"/></div>')
    st.subheader(step['title'])
    st.write(step['general_explanation'])
    st.caption('Educational illustration, not a traced water particle, thermal map or assessment of harm or safety.')
    with st.expander('Stage sources and what remains unknown'):
        st.write(step['confirmed_for_system'])
        for reference in step['sources']:
            st.link_button(reference['title'], reference['url'], wrap=True)
            st.caption(reference['role'].replace('_', ' ') + ' · ' + reference['locator'])
        if step.get('site_context'):
            context = step['site_context']
            st.write(context['text'])
            st.link_button(context['source']['title'], context['source']['url'], wrap=True)
            st.caption('Operator account · ' + context['source']['locator'] + ' · ' + context['source']['period'])
            st.caption(context['limitation'])
        st.caption('Metadata period: ' + ' to '.join(payload['period']))
        for unknown in step['unknowns'] + payload['limitations']:
            st.write(unknown)


def month_panel(payload, identifier):
    """One month widget includes every historical calendar slot, including gaps."""
    st.header('A ribbon of months', anchor='month-ribbon')
    st.write('Explore the reported water temperature before and after cooling, one historical month at a time.')
    if not payload or payload['state'] != 'available' or not payload['rows']:
        st.info('The monthly record is temporarily unavailable. No replacement temperatures are shown.')
        return None
    rows = {row['report_month']: row for row in payload['rows']}
    months = list(rows)
    verified = [month for month, row in rows.items() if row['status'] == 'verified_measurement']
    month = st.select_slider('Historical reporting month', months, value=verified[-1] if verified else months[-1],
        key='month_' + identifier, persist_state='session', help='Arrow keys move by one month. Excluded and missing months remain selectable. No autoplay.')
    row = rows[month]
    st.subheader(pd.Timestamp(month).strftime('%B %Y'))
    st.caption(MONTH_STATUS[row['status']])
    if row['status'] == 'verified_measurement':
        for column, label, field in zip(st.columns(3), ['Intake temperature, °C', 'Discharge temperature, °C', 'Reported ΔT, °C'],
                ['intake_temperature_c', 'discharge_temperature_c', 'delta_t_c']):
            column.metric(label, f'{row[field]:.2f}')
        difference = row['delta_t_c']
        direction = 'warmer' if difference > 0 else 'cooler' if difference < 0 else 'the same temperature'
        comparison = f'{abs(difference):.2f} °C {direction}' if difference else direction
        st.write(f'In {pd.Timestamp(month).strftime("%B %Y")}, water leaving this system was {comparison} compared with water entering it, based on reported monthly averages.')
    else:
        st.info(MONTH_STATUS[row['status']] + '. This month has no confirmed temperature cards or substituted values.')
    st.caption('This difference is across the cooling system, not warming of the whole water body. The ecological report has its own evidence periods and does not change with this month.')
    frame = pd.DataFrame(payload['rows']).set_index('report_month')[['intake_temperature_c', 'discharge_temperature_c']]
    frame.index = pd.to_datetime(frame.index)
    if verified:
        water_chart(frame.rename(columns={'intake_temperature_c': 'Measured intake', 'discharge_temperature_c': 'Measured discharge'}),
            x_label='Reporting month', y_label='Temperature (°C)', height=260, color=['#70eee4', '#ffc86b'], selected_month=month)
    else:
        st.info('No confirmed temperature series for this system. An empty chart would not represent a measurement.')
    st.caption(f'{len(verified)} verified measured months / {len(months)} calendar months · {months[0]} to {months[-1]}. Gaps are unavailable, never zero or interpolated. Rounding is not sensor precision.')
    with st.expander('Missing, excluded and review-blocked months'):
        unavailable = [dict(Month=key, Status=MONTH_STATUS[value['status']]) for key, value in rows.items() if value['status'] != 'verified_measurement']
        if unavailable:
            st.table(unavailable)
        else:
            st.write('Every month in this period has a verified reported measurement.')
    return month
