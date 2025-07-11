# `scripts/` – Shared Utility Modules

General-purpose Python functions and helpers used across all components.

Examples:
- OSC message parsing
- DMX/NDI/MIDI translation tools
- Routing utilities

Referenced across components via `mod.scripts.<module>`.

## Using `signal_mapper`

```python
from mod.scripts import signal_mapper

raw = {"note": 60, "velocity": 100}
kind = signal_mapper.detect_signal_type(raw)  # 'midi'
name, value = signal_mapper.normalize_signal(kind, raw["velocity"])
address = signal_mapper.to_osc_address(name)
```

