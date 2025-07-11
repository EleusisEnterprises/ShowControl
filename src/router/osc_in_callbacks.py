
"""OSC input callbacks for the central router component."""

import logging
from typing import Any

from ..scripts import signal_mapper
from .signal_router import dispatch

LOGGER = logging.getLogger(__name__)


def onReceiveOSC(dat: Any, rowIndex: int, message: str, byteData: bytes,
                  timeStamp: float, address: str, args: list[Any], peer: Any) -> None:
    """Handle incoming OSC messages from connected devices.

    Parameters correspond to TouchDesigner's OSC In DAT callback signature.
    The function normalizes incoming messages using :mod:`signal_mapper` and
    dispatches them to the router. Unrecognized messages are logged.
    """
    try:
        signal_name, value = signal_mapper.parse_osc_message(address, args)
    except ValueError as exc:
        LOGGER.warning("Ignored OSC message %s %s: %s", address, args, exc)
        return

    try:
        dispatch(signal_name, value)
    except Exception as exc:  # pragma: no cover - runtime safety
        LOGGER.error("Failed to dispatch %s=%s: %s", signal_name, value, exc)
