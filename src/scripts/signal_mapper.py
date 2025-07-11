
"""Utilities for interpreting raw OSC messages into normalized signal data.
"""

import logging
from typing import Any, Tuple

LOGGER = logging.getLogger(__name__)


def parse_osc_message(address: str, args: list[Any], namespace: str = "signal") -> Tuple[str, float]:
    """Parse an OSC address and arguments into a normalized signal.

    Parameters
    ----------
    address: str
        OSC address like ``/signal/fader1``.
    args: list
        Arguments from the OSC packet.
    namespace: str
        The expected top-level namespace in the OSC address,
        e.g., 'signal' for addresses like ``/signal/fader1``.

    Returns
    -------
    Tuple[str, float]
        ``(signal_name, normalized_value)``.

    Raises
    ------
    ValueError
        If the address or arguments cannot be interpreted.
    """
    expected_prefix = f"/{namespace}/"
    if not address.startswith(expected_prefix):
        raise ValueError(
            f"Unhandled address: {address}, expected format '/{namespace}/<name>'"
        )

    if not args:
        raise ValueError("Missing value in OSC args")

    # Remove the prefix to get the signal name
    name = address[len(expected_prefix):]
    value = args[0]

    # Normalize numeric values to 0-1 range
    if isinstance(value, (int, float)):
        val_float = float(value)
        if 0 <= val_float <= 1:
            norm = val_float
        elif 0 <= val_float <= 127:
            norm = val_float / 127.0
        elif 0 <= val_float <= 255:
            norm = val_float / 255.0
        else:
            raise ValueError(f"Unsupported numeric range for {value}")
    else:
        raise ValueError(f"Unsupported value type: {type(value)!r}")

    LOGGER.debug("Parsed OSC %s %s -> %s:%f", address, args, name, norm)
    return name, norm