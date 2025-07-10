"""DAT Execute callbacks for routing incoming OSC messages."""

These functions are linked to the ``/project1/dat_execute_in`` operator in the
TouchDesigner project. For an overview of how DAT callbacks work inside
TouchDesigner, see the accompanying ``TDCONTEXT.md`` file.
"""
from td import DAT, tdu
import routing_engine

import osc_helpers
from TD import DAT


    The callback forwards each OSC row to :func:`routing_engine.route_message`.
    See ``TDCONTEXT.md`` for an overview of callback execution.
    """
    for row in dat.rows()[1:]:
        address = row[0].val
        raw_value = row[1].val

        # Try parsing the value as a float. TouchDesigner provides
        # ``tdu.tryParse`` which returns ``None`` for invalid input.
        value = None
        if 'tdu' in globals() and hasattr(tdu, 'tryParse'):  # pragma: no cover
            value = tdu.tryParse(raw_value)

        if value is None:
            try:
                value = float(raw_value)
            except (TypeError, ValueError):
                print(f"osc_exec_in: invalid value '{raw_value}' for {address}")
                continue

        routing_engine.route_message(address, value)
        value = float(row[1].val)
        osc_helpers.handle_incoming(address, value)
    return


def onRowChange(dat, rows):
    """Callback triggered when rows change; currently unused."""
    return


def onColChange(dat, cols):
    """Callback triggered when columns change; currently unused."""
    return


def onCellChange(dat, cells, prev):
    """Callback triggered when individual cells change; currently unused."""
    return


def onSizeChange(dat):
    """Callback triggered when table size changes; currently unused."""
    return
