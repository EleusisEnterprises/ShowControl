# `scripts/` – Shared Utility Modules

General-purpose Python functions and helpers used across all components.

Examples:
- OSC message parsing
- DMX/NDI/MIDI translation tools
- `signal_mapper.py` – A utility for parsing and normalizing raw OSC messages into standardized signals.

The modules in this directory are intended to be referenced from other components in the TouchDesigner network.

Referenced across components via `mod.scripts.<module>`.

## Using `signal_mapper`

The `signal_mapper` module is designed to be called from a DAT, like an OSC In DAT's callback script, to process incoming messages.

```python
# Inside a DAT callback, e.g., /Router/osc_in_callbacks
def onReceiveOSC(dat, rowIndex, message, address, args, peer):
    # Get a reference to the central signal_mapper module
    mapper = mod.scripts.signal_mapper
    try:
        # Call the function from the central module
        signal_name, norm_value = mapper.parse_osc_message(address, args)
        # Now do something with your clean, normalized data
        op('normalized_signals')[signal_name] = norm_value
    except ValueError as e:
        debug(f"Could not parse OSC message: {e}")
    return
```
