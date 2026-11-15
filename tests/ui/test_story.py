"""Regression coverage for the read-only story-support UI."""
import asyncio
import base64
import json
import os
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src/ui'))
from exploration_panel import availability
from water_scene import hero_html


class StoryTests(unittest.TestCase):
    def setUp(self):
        if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':
            def loop():
                result = MagicMock(spec=asyncio.AbstractEventLoop)
                result.is_closed.return_value = False
                return result
            factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop', side_effect=loop)
            factory.start()
            self.addCleanup(factory.stop)

    def screen(self):
        from streamlit.testing.v1 import AppTest
        screen = AppTest.from_file(str(ROOT / 'src/ui/app.py')).run(timeout=40)
        self.assertFalse(screen.exception, str(screen.exception))
        return screen

    def test_surry_journey_exclusion_and_motion_control(self):
        screen = self.screen()
        self.assertEqual(screen.select_slider[0].value, '2025-12')
        self.assertEqual([node.value for node in screen.metric], ['6.11', '12.78', '6.67'])
        self.assertTrue(any('Why this conclusion?' == node.label for node in screen.expander))
        screen.segmented_control[0].set_value('heat_transfer').run(timeout=40)
        self.assertFalse(screen.exception)
        self.assertEqual(screen.segmented_control[0].value, 'heat_transfer')
        self.assertTrue(any('heat' in node.value.lower() for node in screen.markdown))
        screen.select_slider[0].set_value('2024-08').run(timeout=40)
        self.assertFalse(screen.exception)
        self.assertEqual(len(screen.metric), 0)
        self.assertTrue(any('Excluded' in node.value for node in screen.info))
        self.assertTrue(any('James River' in node.value for node in screen.text))
        screen.toggle(key='reduce_motion').set_value(True).run(timeout=40)
        self.assertFalse(screen.exception)
        self.assertTrue(screen.toggle(key='reduce_motion').value)
        self.assertEqual(screen.select_slider[0].value, '2024-08')
        screen.selectbox(key='system_3806').select('eia_3806_435732').run(timeout=40)
        self.assertEqual(len(screen.metric), 0)
        self.assertFalse(any('warmer cooling-water discharge from CW1' in node.value for node in screen.text))
        self.assertTrue(any('CW1 findings are omitted' in node.value for node in screen.info))

    def test_brunswick_switch_and_absent_report(self):
        screen = self.screen()
        screen.selectbox(key='plant').select(6014).run(timeout=40)
        registry = json.loads((ROOT / 'data/model_artifacts/multistation/registry.json').read_text())
        systems = [entry for entry in registry['datasets'] if entry['plant_id_eia'] == 6014 and entry['cooling_id_eia'] in {'1', '2'}]
        self.assertEqual(len(systems), 2)
        for entry in systems:
            screen.selectbox(key='system_6014').select(entry['dataset_id']).run(timeout=40)
            self.assertFalse(screen.exception)
            self.assertEqual(len(screen.metric), 3)
            self.assertTrue(any('No environmental report' in node.value for node in screen.info))
            self.assertFalse(any('James River' in node.value for node in screen.text))
            self.assertIn('month_' + entry['dataset_id'], screen.session_state)
        self.assertEqual(len(screen.select_slider), 1)

    def test_explicit_gaps_never_have_temperature_cards(self):
        from streamlit.testing.v1 import AppTest
        script = f"""
import sys
sys.path.insert(0, {str(ROOT / 'src/ui')!r})
from exploration_panel import month_panel
payload = {{'state':'available','rows':[{{'report_month': month, 'status':status, 'intake_temperature_c':None,'discharge_temperature_c':None,'delta_t_c':None}} for month,status in [('2025-01','missing_month'),('2025-02','missing_temperatures')]]}}
month_panel(payload, 'gap_fixture')
"""
        screen = AppTest.from_string(script).run(timeout=20)
        self.assertFalse(screen.exception)
        self.assertEqual(len(screen.metric), 0)
        self.assertTrue(any('incomplete temperature pair' in node.value for node in screen.info))
        screen.select_slider[0].set_value('2025-01').run(timeout=20)
        self.assertEqual(len(screen.metric), 0)
        self.assertTrue(any('no source record' in node.value for node in screen.info))

    def test_navigation_flags_and_motion_contract(self):
        html = hero_html(True)
        anchors = set(re.findall(r'href="#([^" ]+)"', html))
        self.assertEqual(anchors, {'lab-home','explore-water','environment-report','drop-journey','month-ribbon','evidence-methods'})
        self.assertIn('data-reduced="true"', html)
        # Sections exist before their availability branches in their respective views.
        source = (ROOT / 'src/ui/environment_panel.py').read_text(encoding='utf-8') + (ROOT / 'src/ui/exploration_panel.py').read_text(encoding='utf-8')
        for target in ['environment-report', 'evidence-methods', 'drop-journey', 'month-ribbon']:
            self.assertIn("anchor='" + target + "'", source)
        css = (ROOT / 'src/ui/style.css').read_text(encoding='utf-8')
        js = (ROOT / 'src/ui/motion.js').read_text(encoding='utf-8')
        self.assertIn('.lab-motion-off', css)
        self.assertIn('prefers-reduced-motion', js)
        self.assertIn('document.hidden', js)
        self.assertIn('!reduced()', js)
        flags = availability({'has_insufficient_evidence_report':True,'any_system_has_verified_measurements':True,'any_system_has_verified_model_results':True})
        self.assertIn('Insufficient ecological evidence', flags)
        self.assertIn('Measurements', flags)
        self.assertIn('Saved model', flags)


if __name__ == '__main__':
    unittest.main()
