"""OSC input callback handlers for the router component."""

from typing import Any, Dict, List

from ..scripts import signal_mapper

# Store the latest routed messages for testing or inspection
ROUTER_STATE: Dict[str, Any] = {}


def onReceiveOSC(dat: Any, rowIndex: int, message: str, byteData: bytes,
                  timeStamp: float, address: str, args: List[Any], peer: Any) -> None:
    """Handle an incoming OSC message and route it to the internal state."""
    name, value = signal_mapper.parse_osc_message(address, args)
    if name is not None:
        ROUTER_STATE[name] = value
