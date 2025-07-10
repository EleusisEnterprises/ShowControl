"""Callbacks for the ``DAT Execute`` DAT that routes incoming OSC messages.

These functions are linked to the ``/project1/dat_execute_in`` operator in the
TouchDesigner project. For an overview of how DAT callbacks work inside
TouchDesigner, see the accompanying ``TDCONTEXT.md`` file.
"""

import osc_helpers

# TouchDesigner requires specific callback names that do not follow PEP 8
# conventions. Disable the related pylint warnings for this module.
# pylint: disable=invalid-name,unused-argument


def onTableChange(dat: 'DAT') -> None:
    """Handle table changes from the linked ``DAT Execute`` DAT.

    The callback forwards each OSC row to :func:`osc_helpers.handle_incoming`.
    See ``TDCONTEXT.md`` for an overview of callback execution.
    """
    for row in dat.rows()[1:]:
        address = row[0].val
        value = float(row[1].val)
        osc_helpers.handle_incoming(address, value)
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
