"""Tests for the Resolume OSC patterns."""

import pytest

from src.resolume import patterns

def test_set_layer_opacity():
    """Test the set_layer_opacity function."""
    address, value = patterns.set_layer_opacity(1, 0.5)
    assert address == "/composition/layers/1/video/opacity"
    assert value == 0.5

    with pytest.raises(ValueError):
        patterns.set_layer_opacity(1, 1.1)

def test_trigger_clip():
    """Test the trigger_clip function."""
    address, value = patterns.trigger_clip(2, 5)
    assert address == "/composition/layers/2/clips/5/connect"
    assert value == 1

    address, value = patterns.trigger_clip(2, 5, connected=False)
    assert address == "/composition/layers/2/clips/5/connect"
    assert value == 0
