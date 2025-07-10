from TD import op

"""OSC Out helper functions for TouchDesigner.

This module is loaded by ``/project1/osc_out_dat`` and provides a single
:func:`send_via_dat` function to transmit OSC messages. The function clears the
DAT, appends ``[address, value]`` and triggers ``send()`` so the message is
immediately dispatched.
"""

# pylint: disable=undefined-variable

from typing import Any


def send_via_dat(address: str, value: Any) -> None:
    """Send an OSC message using ``osc_out_dat``.

    Parameters
    ----------
    address : str
        Destination OSC address.
    value : Any
        Value to send with the message.
    """
    out_dat = op('osc_out_dat')
    if not out_dat:
        return
    out_dat.clear()
    out_dat.appendRow([address, value])
    out_dat.send()