"""Plain-language view of a checked publication; no report generation here."""
from pathlib import Path
import streamlit as st
from environment_loader import report_snapshot

STATUS_LABELS = {
    'partial_evidence': 'Historical evidence with limits',
    'insufficient_evidence': 'Not enough evidence',
    'context_only': 'General context, not a site finding',
}
SOURCE_ROLES = {
    'government_reports_via_pudl': 'Government reporting via PUDL',
    'state_monitoring': 'State monitoring',
    'regulator_synthesis': 'Regulator review of earlier studies',
    'operator': 'Operator account',
    'scientific_assessment': 'Scientific literature assessment',
}
MESSAGES = {
    'missing': 'No environmental report has been published for this station. Explore the cooling explanation and check measurement availability below.',
    'module_unavailable': 'Environmental reports are temporarily unavailable. Try Refresh data; the measurement explorer is still available below.',
    'evidence_unavailable': 'This report is unavailable because its files are incomplete or could not be verified. Try Refresh data. Measurements remain available below.',
    'review_required': 'The evidence needs review before this report can be shown, including any unresolved source disagreements. Measurements remain available below.',
}


def statement_evidence(card, root):
    """Display only the reviewed links for this exact statement."""
    scope = card['scope']
    label = ('System ' + str(scope.get('cooling_id_eia')) if scope['level'] == 'system'
             else 'General context' if scope['level'] == 'general' else 'Site context')
    st.caption(label + ' · ' + card['period']['label'])
    st.text(card['statement'])
    # The boundary belongs beside the claim, even when its citations are closed.
    st.caption('Limit: ' + card['limitation'])
    with st.expander('Why this conclusion?', key='proof_' + card['statement_id']):
        st.caption('Exact reviewed wording: ' + card['display_span'])
        if not card['sources']:
            st.write('Review boundary / evidence gap, not a new field observation.')
            review = Path(root) / 'src/model/environment_evidence/CAPABILITY_AUDIT_RU.md'
            if review.is_file():
                st.download_button('Download review notes', review.read_bytes(), file_name='evidence-review.md', mime='text/markdown', key='review_' + card['statement_id'], on_click='ignore')
        for reference in card['sources']:
            st.link_button(reference['title'], reference['url'], wrap=True, width='stretch')
            st.caption('Source role: ' + SOURCE_ROLES.get(reference['role'], reference['role'].replace('_', ' ')))
            st.caption(reference['locator'])
        st.caption('Observation period: ' + card['period']['label'])
        st.caption('Geography: ' + card['geography'])
        if card['counterevidence']:
            st.write('Related evidence addresses a different endpoint; it is not a direct contradiction.')
            for item in card['counterevidence']:
                st.caption(item['source_id'] + ' · ' + item['locator'])
        st.caption('Review basis: ' + card['review_basis'])


def environment_panel(plant_id, system, root, details=None):
    st.header('Environmental report', anchor='environment-report')
    snapshot = report_snapshot(plant_id, root)
    if snapshot.report is None:
        message = MESSAGES[snapshot.state]
        (st.warning if snapshot.state == 'review_required' else st.info)(message)
        st.markdown('[Explore available measurements](#month-ribbon) · [Try the Surry example](#explore-water)')
    else:
        report = snapshot.report
        st.caption('Evidence period: ' + report['period_label'])
        st.caption('The report does not change with the historical month selector. Specialist review has not been performed.')
        cards = details.get('statements', []) if details and details['report_state'] == 'ready' else []
        with st.container(border=True, key='environment_summary'):
            st.subheader('At a glance')
            if cards:
                summary_cards = [card for card in cards if card['target'] == 'summary']
                if not details.get('omitted_system_statement_ids'):
                    st.text(report['summary'])
                else:
                    for card in summary_cards:
                        st.text(card['statement'])
                with st.expander('Evidence behind this summary'):
                    for card in summary_cards:
                        statement_evidence(card, root)
            elif system == 'CW1' or snapshot.state == 'insufficient_evidence':
                st.text(report['summary'])
            else:
                st.write('Site report available. System-specific statement links need review before they can be displayed here.')
        if details and details.get('omitted_system_statement_ids'):
            st.info('CW1 findings are omitted for your selected system. The remaining findings are site or general context, not effects attributed to ' + str(system) + '.')
        if snapshot.state == 'insufficient_evidence':
            st.info('Not enough reviewed evidence for site-specific environmental conclusions. This is not a favourable or unfavourable assessment.')
        elif not cards:
            st.warning('Statement-level source links need review. No substitute citations are assigned.')
        titles = {'water': 'Water', 'animals_plants': 'Animals & plants', 'people': 'People', 'climate': 'Climate', 'unknowns': 'What is unknown'}
        with st.container(key='environment_sections'):
            tabs = st.tabs([titles[section['id']] for section in report['sections']])
            for tab, section in zip(tabs, report['sections']):
                with tab:
                    st.subheader(section['title'])
                    st.caption(STATUS_LABELS[section['status']])
                    section_cards = [card for card in cards if card['target'] == section['id']]
                    if section_cards:
                        # Keep a short entry; the entire reviewed text stays available.
                        for card in section_cards[:1]:
                            statement_evidence(card, root)
                        with st.expander('Read the full finding: ' + titles[section['id']]):
                            for card in section_cards[1:]:
                                statement_evidence(card, root)
                            if not details.get('omitted_system_statement_ids'):
                                with st.expander('Original reviewed wording'):
                                    for paragraph in section['paragraphs']:
                                        st.text(paragraph)
                    elif snapshot.state == 'insufficient_evidence':
                        for paragraph in section['paragraphs']:
                            st.text(paragraph)
                    else:
                        st.info('No reviewed statement links apply to this selection.')
                    if section['periods']:
                        st.caption('Period: ' + '; '.join(period['label'] for period in section['periods']))
    # This navigation destination exists even for a missing or damaged report.
    st.subheader('Sources and limitations', anchor='evidence-methods')
    if snapshot.report is None:
        st.caption('No verified report sources can be displayed for this station right now.')
        return snapshot
    st.caption('Historical sources have different periods. An operator account is distinct from monitoring and general literature.')
    st.caption('Compiled ' + snapshot.report['as_of'] + '; this is not an observation date.')
    for section in snapshot.report['sections']:
        if section['references'] or section['limitations']:
            with st.expander('Sources and limits: ' + section['title']):
                seen = set()
                for reference in section['references']:
                    identity = (reference['url'], reference['public_locator'], reference['role'])
                    if identity in seen:
                        continue
                    seen.add(identity)
                    st.link_button(reference['title'], reference['url'], wrap=True, width='stretch')
                    st.caption(reference['public_locator'])
                    st.caption('Source role: ' + SOURCE_ROLES.get(reference['role'], reference['role'].replace('_', ' ')))
                for limitation in section['limitations']:
                    st.text(limitation)
    return snapshot


def report_method_panel(snapshot):
    """Keep the evidence method and audit out of the consumer report."""
    st.subheader('How the environmental report is prepared')
    st.write('This is a local publication assembled by curated evidence rules, not a trained ecological-safety model. No runtime source search, external API, model fitting or safety score is used.')
    if snapshot.report is not None:
        st.caption(f"Evidence-report contract v{snapshot.report['report_version']} · publication {snapshot.version[:12]}")
        with st.expander('Reviewed claims, scope and technical audit'):
            st.json(snapshot.technical, expanded=False)
