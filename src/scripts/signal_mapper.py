
"""Utilities for interpreting raw OSC messages into normalized signal data.
"""

import logging
from typing import Any, Tuple

LOGGER = logging.getLogger(__name__)


def parse_osc_message(address: str, args: list[Any]) -> Tuple[str, float]:
    """Parse an OSC address and arguments into a normalized signal.

    Parameters
    ----------
    address: str
        OSC address like ``/signal/fader1``.
    args: list
        Arguments from the OSC packet.

    Returns
    -------
    Tuple[str, float]
        ``(signal_name, normalized_value)``.

    Raises
    ------
    ValueError
        If the address or arguments cannot be interpreted.
    """
    if not address.startswith("/signal/"):
        raise ValueError(f"Unhandled address: {address}")

    if not args:
        raise ValueError("Missing value in OSC args")

    name = address.split("/", 2)[-1]
    value = args[0]

    # Normalize numeric values to 0-1 range
    if isinstance(value, (int, float)):
        if 0 <= value <= 1:
            norm = float(value)
        elif 0 <= value <= 127:
            norm = float(value) / 127
        elif 0 <= value <= 255:
            norm = float(value) / 255
        else:
            raise ValueError(f"Unsupported numeric range for {value}")
    else:
        raise ValueError(f"Unsupported value type: {type(value)!r}")

    LOGGER.debug("Parsed OSC %s %s -> %s:%f", address, args, name, norm)
    return name, norm