from __future__ import annotations

"""Utilities to construct an address-builder UI inside TouchDesigner."""

from typing import Any

if 'op' not in globals():  # pragma: no cover - used for type hints
    def op(_):
        return None


def create_address_builder(parent: Any, name: str = 'osc_address_builder') -> Any:
    """Create a simple UI for building OSC addresses.

    The component contains two Dropdown COMPs (layer and channel), an optional
    numeric Field COMP for an index, and a button that sends the assembled
    address using :mod:`ui_helpers` and :mod:`routing_engine`.
    """
    comp = parent.create(baseCOMP, name)  # type: ignore[name-defined]
    layer_dd = comp.create(dropdownCOMP, 'layer')  # type: ignore[name-defined]
    channel_dd = comp.create(dropdownCOMP, 'channel')  # type: ignore[name-defined]
    index_field = comp.create(fieldCOMP, 'index')  # type: ignore[name-defined]
    send_btn = comp.create(buttonCOMP, 'send')  # type: ignore[name-defined]

    callbacks = comp.create(textDAT, 'send_callbacks')  # type: ignore[name-defined]
    callbacks.text = (
        "import ui_helpers, routing_engine\n"
        "def send(addr_builder):\n"
        "    address = ui_helpers.assemble_osc_address(\n"
        "        addr_builder.op('layer'),\n"
        "        addr_builder.op('channel'),\n"
        "        addr_builder.op('index')\n"
        "    )\n"
        "    value = ui_helpers.get_numeric_value(addr_builder.op('index'))\n"
        "    routing_engine.route_message(address, value)\n"
    )
    send_btn.par.command = "op('{}').run('send', me.parent())".format(callbacks.path)
    return comp
