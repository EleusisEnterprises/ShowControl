# `scripts/` – Shared Utility Modules

General-purpose Python functions and helpers used across all components.

Examples:
- OSC message parsing
- DMX/NDI/MIDI translation tools
- Routing utilities
- `signal_mapper.py` – detection and normalization helpers for MIDI, OSC, and DMX
- `signal_mapper` – automatic signal handling and mapping based on pattern definitions

The `signal_mapper` module reads mapping JSON files and automatically converts raw device input into normalized router messages. Import it via `mod.scripts.signal_mapper`.

Referenced across components via `mod.scripts.<module>`.

## Using `signal_mapper`

```python
from mod.scripts import signal_mapper

raw = {"note": 60, "velocity": 100}
kind = signal_mapper.detect_signal_type(raw)  # 'midi'
name, value = signal_mapper.normalize_signal(kind, raw["velocity"])
address = signal_mapper.to_osc_address(name)
```

