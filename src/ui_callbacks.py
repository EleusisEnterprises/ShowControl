"""Callbacks triggered by TouchDesigner UI components."""

from typing import Any


def on_button_press(name: str) -> None:
    """Handle a generic button press."""
    print(f"Button pressed: {name}")


def on_dropdown_select(name: str, value: Any) -> None:
    """Handle dropdown value changes."""
    print(f"Dropdown '{name}' selected {value}")
