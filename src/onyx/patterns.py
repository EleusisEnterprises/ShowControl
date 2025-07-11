"""Module for generating OSC patterns for Obsidian Onyx."""

from typing import Literal

def set_fader(fader_id: int, value: int) -> tuple[str, int]:
    """Generate an OSC message to set a fader value.

    Args:
        fader_id: The ID of the fader (e.g., 4203 for fader 1).
        value: The value to set the fader to (0-255).

    Returns:
        A tuple containing the OSC address and value.
    """
    if not 0 <= value <= 255:
        raise ValueError("Fader value must be between 0 and 255")
    return f"/Mx/fader/{fader_id}", value

def press_button(button_id: int, pressed: bool = True) -> tuple[str, int]:
    """Generate an OSC message to press or release a button.

    Args:
        button_id: The ID of the button.
        pressed: True to press the button, False to release.

    Returns:
        A tuple containing the OSC address and value.
    """
    return f"/Mx/button/{button_id}", 1 if pressed else 0

def playback_action(
    page: int,
    playback: int,
    action: Literal["go", "pause", "release", "select"],
) -> tuple[str, int]:
    """Generate an OSC message for a playback action.

    Args:
        page: The playback page number.
        playback: The playback fader number on the page.
        action: The action to perform.

    Returns:
        A tuple containing the OSC address and a value (typically 1 for go).
    """
    return f"/Mx/playback/page{page}/{playback}/{action}", 1
