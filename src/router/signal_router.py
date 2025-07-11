"""Simple router dispatcher for normalized signals."""

import logging
from typing import Callable

LOGGER = logging.getLogger(__name__)

# Global handler; in real TouchDesigner environment this would be replaced
_HANDLER: Callable[[str, float], None] | None = None


def set_handler(handler: Callable[[str, float], None]) -> None:
    """Register a handler for incoming normalized signals."""
    global _HANDLER
    _HANDLER = handler
    LOGGER.debug("Router handler set to %s", handler)


def dispatch(signal_name: str, value: float) -> None:
    """Send a signal to the registered handler or log if none is set."""
    if _HANDLER is not None:
        try:
            _HANDLER(signal_name, value)
        except Exception as exc:  # pragma: no cover - best effort logging
            LOGGER.error("Error in router handler for %s: %s", signal_name, exc)
    else:
        LOGGER.info("Signal %s=%f (no handler)", signal_name, value)
