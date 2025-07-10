"""Callbacks for the ``DAT Execute`` DAT that routes incoming OSC messages.

These functions are linked to the ``/project1/dat_execute_in`` operator in the
TouchDesigner project. For an overview of how DAT callbacks work inside
TouchDesigner, see the accompanying ``TDCONTEXT.md`` file.
"""
from td import DAT, tdu
import routing_engine

# TouchDesigner requires specific callback names that do not follow PEP 8
# conventions. Disable the related pylint warnings for this module.
# pylint: disable=invalid-name,unused-argument

def onTableChange(dat: 'DAT') -> None:
    """Handle table changes from the linked ``DAT Execute`` DAT.

    The callback forwards each OSC row to :func:`routing_engine.route_message`.
    See ``TDCONTEXT.md`` for an overview of callback execution.
    """
    for row in dat.rows()[1:]:
        # Ensure the row has at least two cells before accessing them.
        if len(row) < 2:
            print("osc_exec_in: skipping row with missing columns", row)
            continue

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
    return


def onRowChange(dat: 'DAT', rows) -> None:
    """Called when table rows change; currently unused."""
    return


def onColChange(dat: 'DAT', cols) -> None:
    """Called when table columns change; currently unused."""
    return


def onCellChange(dat: 'DAT', cells, prev) -> None:
    """Called when individual cells change; currently unused."""
    return


def onSizeChange(dat: 'DAT') -> None:
    """Called when table size changes; currently unused."""
    return
