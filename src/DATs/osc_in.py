"""OSC In DAT callback.

This module defines :func:`onReceiveOSC`, which TouchDesigner calls
whenever an OSC message arrives. The default implementation simply
prints the address and arguments to the Textport. Modify it as needed
for your project.
"""

# pylint: disable=invalid-name,unused-argument

def onReceiveOSC(dat, rowIndex, message, byteData, timeStamp, address, args, peer):
    """Handle a received OSC message from the OSC In DAT.

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
