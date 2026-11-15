"""Transparent scenario arithmetic, independent of retrospective ML artifacts."""
from math import isfinite

IPCC_URL = 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'
IPCC_NUCLEAR_G_PER_KWH = (3.7, 12.0, 110.0)


def finite(value, name, *, minimum=None, positive=False):
    """Reject missing, nonnumeric, nonfinite and out-of-domain inputs."""
    if isinstance(value, bool):
        raise ValueError(f'{name} must be a number.')
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f'{name} must be a finite number.') from None
    if not isfinite(value):
        raise ValueError(f'{name} must be finite.')
    if minimum is not None and value < minimum:
        raise ValueError(f'{name} must be at least {minimum}.')
    if positive and value <= 0:
        raise ValueError(f'{name} must be greater than zero.')
    return value


def mixed_stream(ambient_c, discharge_c, bypass_m3_s, discharge_m3_s):
    """Ideal steady complete mixing of TWO separate equal-density water streams."""
    ambient = finite(ambient_c, 'Ambient temperature', minimum=-273.15)
    discharge = finite(discharge_c, 'Discharge temperature', minimum=-273.15)
    bypass = finite(bypass_m3_s, 'Bypass flow', minimum=0)
    flow = finite(discharge_m3_s, 'Discharge flow', positive=True)
    fraction = 1 / (1 + bypass / flow)
    temperature = finite(ambient + fraction * (discharge - ambient), 'Mixed temperature')
    return {'mixed_c': temperature, 'rise_c': temperature - ambient,
            'discharge_fraction': fraction}


def closed_volume_rise(volume_m3, recirculation_m3_s, system_delta_c, hours):
    """Adiabatic fixed-volume recirculation box, constant heat input, no added water."""
    volume = finite(volume_m3, 'Water volume', positive=True)
    flow = finite(recirculation_m3_s, 'Recirculation flow', minimum=0)
    delta = finite(system_delta_c, 'Cooling-system temperature rise')
    duration = finite(hours, 'Duration', minimum=0)
    # Equal constant water density and heat capacity cancel in the heat balance.
    return finite(flow * delta * duration * 3600 / volume, 'Volume-average change')


def lifecycle_tonnes(generation_twh, factor_g_per_kwh):
    """Electricity × literature intensity; TWh→kWh (1e9), grams→tonnes (1e-6)."""
    generation = finite(generation_twh, 'Electricity generation', minimum=0)
    factor = finite(factor_g_per_kwh, 'Lifecycle intensity', minimum=0)
    return finite(generation * factor * 1000, 'Lifecycle scenario total')


def reference_difference(temperature_c, reference_c):
    """Arithmetic relative to a user-supplied reference, never a safety verdict."""
    return finite(finite(temperature_c, 'Temperature', minimum=-273.15) - finite(
        reference_c, 'Reference temperature', minimum=-273.15), 'Reference difference')
