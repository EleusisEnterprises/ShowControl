"""Signal mapping utilities for ShowControl.

This module offers helpers for detecting incoming signal types,
normalizing their values to a 0–1 range, and mapping those
normalized signals to OSC addresses. It is importable via
``mod.scripts.signal_mapper``.
"""

from typing import Any, Tuple


def detect_signal_type(data: Any) -> str:
    """Return the detected signal type.

    Parameters
    ----------
    data:
        Raw data representing a signal. Can be a dict or any
        structure from an input device.

    Returns
    -------
    str
        One of ``"midi"``, ``"osc"``, ``"dmx"``, or ``"unknown"``.
    """
    if isinstance(data, dict):
        keys = set(data)
        if {"address", "args"} <= keys:
            return "osc"
        if {"status", "data1", "data2"} <= keys or {"note", "velocity"} <= keys:
            return "midi"
        if {"universe", "channel", "value"} <= keys:
            return "dmx"
    if isinstance(data, (list, tuple)) and len(data) == 3:
        if all(isinstance(x, int) and 0 <= x <= 255 for x in data):
            return "dmx"
    return "unknown"


def normalize_signal(name: str, value: Any) -> Tuple[str, float]:
    """Normalize a value to the range 0–1.

    Parameters
    ----------
    name:
        Name or type hint for the signal.
    value:
        Raw numeric value.

    Returns
    -------
    tuple
        ``(standardized_name, normalized_value)``
    """
    try:
        value_f = float(value)
    except (TypeError, ValueError):
        return name.lower(), 0.0

    lower = name.lower()
    if lower in {"midi", "cc", "note"}:
        value_f /= 127.0
    elif lower == "dmx":
        value_f /= 255.0
    if value_f < 0:
        value_f = 0.0
    elif value_f > 1:
        value_f = 1.0
    return lower, value_f


def to_osc_address(signal: Tuple[str, float] | str) -> str:
    """Convert a signal name into an OSC address.

    Parameters
    ----------
    signal:
        Either a ``(name, value)`` tuple or the signal name alone.

    Returns
    -------
    str
        OSC address string beginning with ``/``.
    """
    name = signal[0] if isinstance(signal, tuple) else signal
    if isinstance(name, int):
        return f"/{name}"
    name_str = str(name)
    if not name_str.startswith("/"):
        name_str = "/" + name_str.replace("_", "/")
    return name_str
