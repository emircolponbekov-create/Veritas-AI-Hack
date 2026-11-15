"""Scenario widgets retain explicit inputs and display correct units/results."""
import asyncio
import os
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[2]


class ImpactScreenTests(unittest.TestCase):
    def test_scenarios_and_reference_gate(self):
        if os.environ.get('VERITAS_UI_NO_SOCKET_TESTS') == '1':
            def nonrunning_loop():
                loop = MagicMock(spec=asyncio.AbstractEventLoop)
                loop.is_closed.return_value = False
                return loop
            factory = patch('streamlit.testing.v1.local_script_runner.asyncio.new_event_loop',
                            side_effect=nonrunning_loop)
            factory.start()
            self.addCleanup(factory.stop)
        from streamlit.testing.v1 import AppTest
        script = f'''
import sys
sys.path.insert(0, {str(ROOT)!r})
sys.path.insert(0, {str(ROOT / 'src/ui')!r})
from impact_panel import impact_panel
impact_panel()
'''
        at = AppTest.from_string(script).run(timeout=30)
        self.assertFalse(at.exception)
        self.assertEqual(len(at.success), 0)
        for key, value in [('mix_ambient', 20.), ('mix_discharge', 30.),
                           ('mix_bypass', 90.), ('mix_flow', 10.),
                           ('box_volume', 360000.), ('box_flow', 10.),
                           ('box_delta', 10.), ('box_hours', 1.),
                           ('lca_generation', 1.)]:
            at.number_input(key=key).set_value(value)
        at.run(timeout=30)
        self.assertFalse(at.exception)
        self.assertTrue(any('21.00' in x.value and '+1.00' in x.value for x in at.success))
        self.assertTrue(any('+1.000' in x.value for x in at.success))
        self.assertTrue(any('12,000.0' in x.value for x in at.markdown))
        at.number_input(key='eco_temperature').set_value(25.)
        at.number_input(key='eco_reference').set_value(20.)
        at.run(timeout=30)
        self.assertFalse(any('above the entered reference' in x.value for x in at.warning))
        at.text_input(key='eco_source').set_value('Illustrative reference, not a site permit')
        at.checkbox(key='eco_appropriate').check()
        at.run(timeout=30)
        self.assertFalse(at.exception)
        self.assertTrue(any('5.00' in x.value and 'above' in x.value for x in at.warning))
