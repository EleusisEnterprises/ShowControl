# `onyx/` – Obsidian Onyx Integration

Handles all logic for integrating with the Onyx lighting control platform.

- **Incoming OSC:** Parses messages from Onyx (faders, buttons, etc.) into normalized signals.
- **Outgoing Control:** Formats and sends messages (OSC, DMX, NDI) to control Onyx.
- `onyx_osc_parser.py`: A dedicated script for interpreting Onyx's `/Mx` OSC namespace.

This component relies on the generic `signal_mapper.py` for normalization.