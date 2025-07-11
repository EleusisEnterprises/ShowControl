# `scripts/` – Shared Utility Modules

General-purpose Python functions and helpers used across all components.

Examples:
- OSC message parsing
- DMX/NDI/MIDI translation tools
- Routing utilities
- `signal_mapper` – automatic signal handling and mapping based on pattern definitions

The `signal_mapper` module reads mapping JSON files and automatically converts raw device input into normalized router messages. Import it via `mod.scripts.signal_mapper`.

Referenced across components via `mod.scripts.<module>`.
