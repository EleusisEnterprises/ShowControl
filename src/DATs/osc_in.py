"""Callback module for an ``OSC In DAT`` operator.

The :func:`onReceiveOSC` function is connected to ``/project1/osc_in_dat`` in the
TouchDesigner project. It runs whenever an OSC message arrives. For details on
how callbacks fit into the Python environment, consult ``TDCONTEXT.md``.
The default implementation simply prints the address and arguments to the
Textport.
"""

from TD import DAT


def onReceiveOSC(dat: 'DAT', rowIndex, message, byteData, timeStamp, address, args, peer) -> None:
    """Handle a received OSC message from the linked ``OSC In DAT``.

    Parameters
    ----------
    dat : DAT
        The DAT that received the message.
    rowIndex : int
        Row index where the message was placed.
    message : str
        ASCII representation of the message.
    byteData : bytes
        Raw byte data of the message.
    timeStamp : float
        Arrival time of the OSC message.
    address : str
        OSC address of the message.
    args : list
        Values contained within the OSC message.
    peer : object
        Information about the sender.
    """
    # Access variables so they are not considered unused by linters
    _ = (dat, rowIndex, message, byteData, timeStamp, peer)
    print(f"Received OSC {address}: {args}")
    return

