"""Tests for the Onyx OSC patterns."""

import pytest

from src.onyx import patterns

def test_set_fader():
    """Test the set_fader function."""
    address, value = patterns.set_fader(4203, 128)
    assert address == "/Mx/fader/4203"
    assert value == 128

    with pytest.raises(ValueError):
        patterns.set_fader(4203, 256)

def test_press_button():
    """Test the press_button function."""
    address, value = patterns.press_button(1234)
    assert address == "/Mx/button/1234"
    assert value == 1

    address, value = patterns.press_button(1234, pressed=False)
    assert address == "/Mx/button/1234"
    assert value == 0

def test_playback_action():
    """Test the playback_action function."""
    address, value = patterns.playback_action(1, 2, "go")
    assert address == "/Mx/playback/page1/2/go"
    assert value == 1
