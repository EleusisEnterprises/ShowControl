# `onyx/` – Obsidian Onyx Integration

Handles all logic for integrating with the Onyx lighting control platform.

- **Incoming OSC:** `onyx_osc_parser.py` interprets messages from Onyx (faders, buttons, etc.) into normalized signals.
- **Outgoing OSC:** `patterns.py` provides helper functions to generate correctly formatted OSC messages for controlling Onyx faders, buttons, and playback.

This component relies on the generic `signal_mapper.py` for normalization.

## Sending Commands to Onyx

To send commands, import the `patterns` module from its Text DAT and use its functions with an OSC Out DAT (e.g., `/Onyx/osc_out_onyx`).

```python
# Example inside a script in the /Onyx COMP
onyx_patterns = mod('patterns')
onyx_sender = op('osc_out_onyx')

# Set fader 1 (ID 4203) to 50%
address, value = onyx_patterns.set_fader(4203, 128)
onyx_sender.sendOSC(address, [value])

# Press GO on playback 3 on page 1
address, value = onyx_patterns.playback_action(1, 3, 'go')
onyx_sender.sendOSC(address, [value])
```