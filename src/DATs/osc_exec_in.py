"""DAT Execute callbacks for routing incoming OSC messages."""


import osc_helpers
from TD import DAT


def onTableChange(dat):
    """Handle table changes by forwarding OSC messages via :mod:`osc_helpers`."""
    for row in dat.rows()[1:]:
        address = row[0].val
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
