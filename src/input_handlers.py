"""Input parsing for incoming OSC and MIDI signals.

This module provides minimal stub classes used by the TouchDesigner project.
Actual implementations will be filled in during development.
"""

from typing import Any


class InputHandler:
    """Basic handler for OSC and MIDI messages."""

    def handle_osc(self, address: str, *args: Any) -> None:
        """Handle an incoming OSC message.

        Parameters
        ----------
        address:
            OSC address pattern of the message.
        *args:
            Message payload values.
        """
        # Placeholder implementation
        print(f"Received OSC: {address} {args}")

    def handle_midi(self, channel: int, control: int, value: int) -> None:
        """Handle an incoming MIDI message.

        Parameters
        ----------
        channel:
            MIDI channel number.
        control:
            Controller or note number.
        value:
            Associated value or velocity.
        """
        # Placeholder implementation
        print(f"Received MIDI: ch={channel} ctrl={control} val={value}")
