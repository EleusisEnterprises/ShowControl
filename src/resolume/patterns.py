"""Module for generating OSC patterns for Resolume Arena."""

from typing import Literal

def set_layer_opacity(layer: int, opacity: float) -> tuple[str, float]:
    """Generate an OSC message to set the opacity of a layer.

    Args:
        layer: The layer number (1-indexed).
        opacity: The opacity value (0.0 to 1.0).

    Returns:
        A tuple containing the OSC address and value.
    """
    if not 0.0 <= opacity <= 1.0:
        raise ValueError("Opacity must be between 0.0 and 1.0")
    return f"/composition/layers/{layer}/video/opacity", opacity

def trigger_clip(layer: int, clip: int, connected: bool = True) -> tuple[str, int]:
    """Generate an OSC message to trigger a clip.

    Args:
        layer: The layer number (1-indexed).
        clip: The clip number (1-indexed).
        connected: True to connect (trigger) the clip, False to disconnect.

    Returns:
        A tuple containing the OSC address and value.
    """
    return f"/composition/layers/{layer}/clips/{clip}/connect", 1 if connected else 0
