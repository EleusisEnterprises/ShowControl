"""Module for generating OSC patterns specifically for Resolume Arena.

This module provides Python functions that construct the correct OSC addresses and
values required to control various parameters within Resolume Arena, such as
layer opacity and clip triggering. These functions are designed to be called by
other parts of the ShowControl system, including the `osc_pattern_generator.py`
for UI-driven OSC message creation.
"""

from typing import Literal

def set_layer_opacity(layer: int, opacity: float) -> tuple[str, float]:
    """Generate an OSC message to set the opacity of a specific layer in Resolume.

    This function constructs the OSC address in the format
    `/composition/layers/{layer}/video/opacity` and returns the specified opacity value.
    Resolume expects opacity values between 0.0 (fully transparent) and 1.0 (fully opaque).

    Args:
        layer: The layer number in Resolume (1-indexed).
        opacity: The desired opacity value (0.0 to 1.0).

    Returns:
        A tuple containing the OSC address (str) and the opacity value (float).

    Raises:
        ValueError: If the provided opacity value is outside the valid range of 0.0 to 1.0.
    """
    if not 0.0 <= opacity <= 1.0:
        raise ValueError("Opacity must be between 0.0 and 1.0")
    return f"/composition/layers/{layer}/video/opacity", opacity

def trigger_clip(layer: int, clip: int, connected: bool = True) -> tuple[str, int]:
    """Generate an OSC message to trigger or disconnect a clip in Resolume.

    This function constructs the OSC address in the format
    `/composition/layers/{layer}/clips/{clip}/connect`. The OSC value is 1 to trigger
    (connect) the clip and 0 to disconnect it.

    Args:
        layer: The layer number where the clip is located (1-indexed).
        clip: The clip number within the specified layer (1-indexed).
        connected: A boolean indicating whether to connect (trigger) the clip (True)
                   or disconnect it (False). Defaults to True.

    Returns:
        A tuple containing the OSC address (str) and the connection state (int: 1 for connect, 0 for disconnect).
    """
    return f"/composition/layers/{layer}/clips/{clip}/connect", 1 if connected else 0