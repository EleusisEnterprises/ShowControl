"""
Parses OSC messages specific to Obsidian Onyx, using the generic signal_mapper.

This script will be placed in a Text DAT inside the /Onyx COMP.
"""
import logging
from typing import Tuple
from td import mod

# Reference the generic mapper from the central /scripts COMP
mapper = mod('/scripts/signal_mapper')
LOGGER = logging.getLogger(__name__)

def parse_message(address: str, args: list) -> Tuple[str, float]:
    """
    Parses an Onyx OSC message.
    Onyx uses the '/Mx' namespace.
    Example Addresses:
    - /Mx/fader/4203
    - /Mx/button/6101
    - /Mx/playback/page1/3/go

    Returns
    -------
    Tuple[str, float]
        (signal_name, normalized_value) e.g. ('fader/4203', 1.0)
    """
    try:
        # Use the generic parser with the 'Mx' namespace
        name, norm_value = mapper.parse_osc_message(address, args, namespace='Mx')

        LOGGER.debug("Parsed Onyx OSC %s -> %s:%f", address, name, norm_value)
        return name, norm_value

    except ValueError as e:
        # Re-raise the exception to be handled by the caller
        raise ValueError(f"Failed to parse Onyx message: {e}") from e