"""Coastal presentation: local imagery, optional motion and measured charts."""
import base64
import re
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ASSET = Path(__file__).parent / 'assets' / 'coastline.png'


def water_chart(frame, *, x_label, y_label, height, color, selected_month=None):
    """Show actual monthly values, preserve null gaps and mark the selected month."""
    data = frame.rename_axis('date').reset_index().melt('date', var_name='Series', value_name='value')
    encoding = dict(
        x=alt.X('date:T', title=x_label),
        y=alt.Y('value:Q', title=y_label, scale=alt.Scale(zero=False)),
        color=alt.Color('Series:N', scale=alt.Scale(domain=list(frame.columns), range=color),
                        legend=alt.Legend(orient='bottom', title=None)),
        tooltip=[alt.Tooltip('date:T', title='Month', format='%Y-%m'), 'Series:N',
                 alt.Tooltip('value:Q', title=y_label, format='.2f')],
    )
    chart = alt.Chart(data).mark_line(strokeWidth=2.3).encode(**encoding)
    if selected_month and pd.Timestamp(selected_month) in frame.index:
        selected = data[data.date == pd.Timestamp(selected_month)].dropna(subset=['value'])
        if not selected.empty:
            rule = alt.Chart(pd.DataFrame({'date': [pd.Timestamp(selected_month)]})).mark_rule(
                color='#d0f56f', strokeDash=[3, 5], opacity=.6).encode(x='date:T')
            points = alt.Chart(selected).mark_circle(size=80, stroke='#062830', strokeWidth=2).encode(**encoding)
            text = alt.Chart(selected.iloc[:1]).mark_text(
                align='right', dx=-9, dy=-16, color='#d0f56f', fontSize=12,
            ).encode(x='date:T', y='value:Q', text=alt.value(selected_month))
            chart = chart + rule + points + text
    chart = chart.properties(height=height, background='#062830').configure(font='Segoe UI').configure_view(stroke=None).configure_axis(
        labelColor='#b9d2d4', titleColor='#daece8', gridColor='#24434b', gridOpacity=.5,
        domainColor='#52777e', labelPadding=8, titlePadding=12,
    ).configure_legend(labelColor='#d4eae5', padding=12)
    st.altair_chart(chart, width='stretch', theme=None)


def hero_html(reduced=False):
    """Embed the supplied image locally; never rely on an expiring download URL."""
    image = ''
    missing = ''
    if ASSET.is_file():
        encoded = base64.b64encode(ASSET.read_bytes()).decode('ascii')
        image = f'<image href="data:image/png;base64,{encoded}" width="1672" height="941"/>'
    else:
        missing = '<span class="asset-missing">Coastal background unavailable locally</span>'
    paths = [
        'M1510 315 C1430 365 1410 445 1270 455 S1020 460 850 560 S500 590 120 845',
        'M1500 325 C1420 380 1440 430 1280 470 S1010 510 820 550 S460 690 70 810',
        'M1520 330 C1480 410 1360 440 1240 485 S1000 460 790 590 S420 650 90 890',
    ]
    particles = ''.join(
        f'<circle class="flow-particle" r="{1.2 + i % 3 * .65}" fill="{["#b9fff2", "#66f1df", "#e4f9b0"][i % 3]}" '
        f'style="offset-path:path(\'{paths[i % 3]}\');--travel:{13 + i % 5 * 3}s;--delay:-{i * 2.7}s;--opacity:{.25 + i % 4 * .15}"></circle>'
        for i in range(16)
    )
    html = '''<div class="lab-topline"><a class="lab-brand" href="#lab-home"><span class="ripple-mark" aria-hidden="true">&#9678;</span><span>NUCLEAR WATER /<br>CLIMATE LAB</span></a>
<nav aria-label="Page sections"><a href="#explore-water">Explore</a><a href="#environment-report">Environment</a><a href="#drop-journey">Follow a drop</a><a href="#month-ribbon">Months</a><a href="#evidence-methods">Methodology</a></nav>
<span class="lab-tag">Research prototype</span></div>
<section id="lab-home" class="lab-hero scene-paused">
<div class="water-scene" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1672 941" preserveAspectRatio="xMidYMin slice" focusable="false">
<defs><clipPath id="water-mask"><path d="M0 270L350 290 670 245 770 235 950 280 1110 290 1270 305 1450 320 1550 350 1672 390V941H0Z"/></clipPath>
<linearGradient id="thermal-gradient" x1="1" y1="0" x2="0" y2="1"><stop stop-color="#ffc86b"/><stop offset=".28" stop-color="#b7e8a7"/><stop offset=".6" stop-color="#21d9cd"/><stop offset="1" stop-color="#0daaaa" stop-opacity="0"/></linearGradient>
<filter id="soft-water"><feGaussianBlur stdDeviation="19"/></filter>
<linearGradient id="glint"><stop stop-color="#9eece0" stop-opacity="0"/><stop offset=".5" stop-color="#b6fff2" stop-opacity=".16"/><stop offset="1" stop-color="#9eece0" stop-opacity="0"/></linearGradient></defs>
<g class="coast-layer">''' + image + '''</g>
<g clip-path="url(#water-mask)"><g class="plume-layer" filter="url(#soft-water)">
<path class="plume-ribbon ribbon-a" d="M1510 330C1390 360 1490 430 1260 460S1000 470 820 570 480 620 160 840" fill="none" stroke="url(#thermal-gradient)" stroke-width="72"/>
<path class="plume-ribbon ribbon-b" d="M1510 350C1370 400 1450 465 1200 475S1000 555 780 570 520 700 80 900" fill="none" stroke="url(#thermal-gradient)" stroke-width="43"/></g>
<g class="water-glints"><ellipse cx="900" cy="430" rx="430" ry="24" fill="url(#glint)"/><ellipse cx="430" cy="675" rx="330" ry="18" fill="url(#glint)"/></g>
''' + particles + '''</g></svg></div>
<div class="hero-copy"><div class="lab-eyebrow">Water. Energy. Evidence.</div><h1>Energy leaves<br>a <em>ripple.</em></h1>
<p>Explore the link between nuclear energy,<br>cooling water and living ecosystems.</p><p class="hero-start">Historical measurements. Reviewed sources.<br>Start with the Surry example below.</p>
<div class="hero-actions"><a class="primary-action" href="#explore-water">Explore the water &nbsp; &#8594;</a><a href="#evidence-methods">View the evidence</a></div>
<div class="lab-tags"><span class="lab-tag">Reported measurements</span><span class="lab-tag">Retrospective ML</span></div></div>
<div class="scene-caption">Illustrative scene &middot; not a measured thermal map</div>''' + missing + '</section>'
    # Streamlit sanitizes inline SVG. Mount only our trusted local SVG in motion.js.
    svg = re.search(r'<svg[\s\S]*?</svg>', html).group(0)
    encoded_svg = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    html = html.replace('scene-paused"', 'scene-paused" data-reduced="' + str(reduced).lower() + '"')
    return html.replace(svg, f'<div class="scene-vector" data-vector="{encoded_svg}"></div>')


def install_motion(reduced=False):
    # Only our own local script is executable. Data and user input never enter it.
    script = Path(__file__).with_name('motion.js').read_text(encoding='utf-8')
    setting = 'document.documentElement.classList.toggle("lab-motion-off", ' + str(reduced).lower() + ');'
    st.html('<script>' + setting + script + '</script>', unsafe_allow_javascript=True)
