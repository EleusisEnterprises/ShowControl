import mod.scripts.signal_mapper as sm


def test_detect_signal_type():
    assert sm.detect_signal_type({'address': '/fader/1', 'args': [1]}) == 'osc'
    assert sm.detect_signal_type({'note': 60, 'velocity': 100}) == 'midi'
    assert sm.detect_signal_type({'universe': 1, 'channel': 1, 'value': 255}) == 'dmx'
    assert sm.detect_signal_type('foo') == 'unknown'


def test_normalize_signal():
    assert sm.normalize_signal('midi', 64) == ('midi', 64/127)
    assert sm.normalize_signal('dmx', 255) == ('dmx', 1.0)
    assert sm.normalize_signal('custom', 0.5) == ('custom', 0.5)


def test_to_osc_address():
    assert sm.to_osc_address(('fader_1', 0.5)) == '/fader/1'
    assert sm.to_osc_address('layer_1') == '/layer/1'

