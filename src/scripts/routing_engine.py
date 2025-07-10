from __future__ import annotations

"""Routing engine that resolves generic OSC messages into destination addresses."""

from typing import Any, List
import osc_helpers


def _format_address(template: str, value: Any) -> str:
    """Return the template with ``{value}`` replaced if present."""
    try:
        return template.format(value=value)
    except Exception:
        return template


def route_message(address: str, value: Any) -> List[str]:
    """Map an incoming OSC message to its destination addresses.

    The function uses the routing tables loaded by :mod:`osc_helpers`. Any
    ``{value}`` placeholder in a destination address will be replaced with
    the numeric ``value`` provided.

    Parameters
    ----------
    address:
        Incoming OSC address to look up.
    value:
        Message payload to forward.

    Returns
    -------
    list of str
        The resolved destination addresses that were sent.
    """
    # Ensure the helper module has the latest data loaded.
    osc_helpers.reload_mappings()

    patterns = osc_helpers._patterns  # type: ignore[attr-defined]
    mappings = osc_helpers._mappings  # type: ignore[attr-defined]

    generics = patterns.get(address)
    if not generics:
        return []
    if not isinstance(generics, list):
        generics = [generics]

    sent: List[str] = []
    for key in generics:
        dests = mappings.get(key)
        if not dests:
            continue
        if not isinstance(dests, list):
            dests = [dests]
        for dest in dests:
            formatted = _format_address(dest, value)
            osc_helpers.handle_outgoing(formatted, value)
            sent.append(formatted)
    return sent
