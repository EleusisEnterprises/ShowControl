# Python Modules

This folder contains all modular logic for handling signals and UI inside TouchDesigner.

- `input_handlers.py`: Ingests and parses incoming OSC/MIDI signals.
- `routing_engine.py`: Core logic that maps inputs → outputs.
- `osc_utils.py`: Helper functions for sending/receiving OSC messages.
- `ui_callbacks.py`: Logic for UI button presses, dropdowns, etc.
- `stage_utils.py`: (Planned) Utilities for 3D stage modeling and projection mapping.

Each module currently exposes small stub classes or functions so new
contributors can experiment with the system without writing everything
from scratch. These stubs print basic information to the console and
serve as starting points for future development.
