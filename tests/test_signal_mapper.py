
import pytest

from src.scripts import signal_mapper


def test_detect_signal_type():
    midi_msg = {'note': 60, 'velocity': 100}
    osc_msg = {'address': '/fader/1', 'value': 0.5}
    dmx_msg = {'dmx_ch': 1, 'value': 255}

    assert signal_mapper.detect_signal_type(midi_msg) == 'MIDI'
    assert signal_mapper.detect_signal_type(osc_msg) == 'OSC'
    assert signal_mapper.detect_signal_type(dmx_msg) == 'DMX'


def test_normalization_and_address_mapping():
    # normalization 64 from 0-127 to 0-1
    val = signal_mapper.normalize_value(64, 0, 127)
    assert pytest.approx(val, rel=1e-3) == 64 / 127

    assert signal_mapper.map_internal_to_osc('fader_1') == '/fader/1'
    assert signal_mapper.map_osc_to_internal('/fader/2') == 'fader_2'
