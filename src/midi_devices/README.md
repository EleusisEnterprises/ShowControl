# `midi_devices/` – Input Devices via MIDI

Contains the input normalization logic and device-specific handlers for MIDI controllers (e.g., APCmini, APC40).

Each subfolder/module converts raw MIDI (note/cc) into named, normalized control signals.