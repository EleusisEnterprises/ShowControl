# `src/` – Core Application Code

This folder contains all executable logic and routing code for the ShowControl system.
It includes per-device COMPs, signal pattern mapping, and the main router logic.

Organized for clarity and modular development in VS Code, all device and routing logic lives here.

## UI-Driven OSC Pattern Generation

A new capability has been introduced to dynamically generate OSC addresses and values
through a user interface within TouchDesigner. This leverages the `router` module,
specifically `osc_pattern_generator.py`, which acts as an intermediary between the UI
and the device-specific pattern generation logic found in modules like `onyx/patterns.py`
and `resolume/patterns.py`. This allows for flexible and intuitive control of connected
systems via OSC.