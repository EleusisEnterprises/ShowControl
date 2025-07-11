"""Module for generating OSC patterns specifically for Obsidian Onyx lighting consoles.

This module provides Python functions that construct the correct OSC addresses and
values required to control various parameters within Onyx, such as faders, buttons,
and playback actions. These functions are designed to be called by other parts of
the ShowControl system, including the `osc_pattern_generator.py` for UI-driven
OSC message creation.
"""

from typing import Literal

def set_fader(fader_id: int, value: int) -> tuple[str, int]:
    """Generate an OSC message to set a fader value on the Onyx console.

    This function constructs the OSC address in the format `/Mx/fader/{fader_id}`
    and returns the specified value. Onyx faders typically expect values in the
    range of 0-255.

    Args:
        fader_id: The unique identifier for the fader on the Onyx console.
                  (e.g., 4203 for fader 1).
        value: The value to set the fader to (0-255). This will be the OSC argument.

    Returns:
        A tuple containing the OSC address (str) and the fader value (int).

    Raises:
        ValueError: If the provided fader value is outside the valid range of 0-255.
    """
    if not 0 <= value <= 255:
        raise ValueError("Fader value must be between 0 and 255")
    return f"/Mx/fader/{fader_id}", value

def press_button(button_id: int, pressed: bool = True) -> tuple[str, int]:
    """Generate an OSC message to press or release a button on the Onyx console.

    This function constructs the OSC address in the format `/Mx/button/{button_id}`.
    The OSC value will be 1 for a press (or active state) and 0 for a release
    (or inactive state).

    Args:
        button_id: The unique identifier for the button on the Onyx console.
        pressed: A boolean indicating whether the button is being pressed (True)
                 or released (False). Defaults to True.

    Returns:
        A tuple containing the OSC address (str) and the button state (int: 1 for pressed, 0 for released).
    """
    return f"/Mx/button/{button_id}", 1 if pressed else 0

def playback_action(
    page: int,
    playback: int,
    action: Literal["go", "pause", "release", "select"],
) -> tuple[str, int]:
    """Generate an OSC message for a specific playback action on the Onyx console.

    This function constructs the OSC address in the format
    `/Mx/playback/page{page}/{playback}/{action}`. The OSC value is typically 1
    to trigger the action.

    Args:
        page: The page number where the playback is located.
        playback: The playback fader/button number on the specified page.
        action: The specific action to perform. Must be one of "go", "pause",
                "release", or "select".

    Returns:
        A tuple containing the OSC address (str) and the action value (int, typically 1).
    """
    return f"/Mx/playback/page{page}/{playback}/{action}", 1