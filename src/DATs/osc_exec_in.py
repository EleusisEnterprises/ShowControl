"""DAT Execute callbacks for routing incoming OSC messages."""

import osc_helpers

# TouchDesigner requires specific callback names that do not follow PEP 8
# conventions. Disable the related pylint warnings for this module.
# pylint: disable=invalid-name,unused-argument


def onTableChange(dat):
    """Handle table changes by forwarding OSC messages via :mod:`osc_helpers`."""
    # Skip the header row; each subsequent row should contain an OSC
    # address in column 0 and a numeric value in column 1.
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
