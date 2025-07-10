# Source Configs & Scripts

This folder holds:  

- `input_handlers.py`: Ingests and parses incoming OSC/MIDI signals.
- `routing_engine.py`: Core logic that maps inputs → outputs.
- `osc_utils.py`: Helper functions for sending/receiving OSC messages.
- `ui_callbacks.py`: Logic for UI button presses, dropdowns, etc.
- `stage_utils.py`: (Planned) Utilities for 3D stage modeling and projection mapping.

<!-- Example configs live in `config/routing_map.json`, `config/input_aliases.json`, and `config/endpoints.json`. -->

- `*.json` → OSC patterns & software mappings  
- `scripts/` → Python modules that handle OSC input, routing, and UI logic  

## DATs Directory

`src/DATs/` holds the external, editable Text DAT scripts:

- **dat_execute_in.txt** → hooked into `/project1/dat_execute_in` DAT Execute DAT  
- **osc_in_dat.txt** → optional template for `/project1/osc_in_dat` OSC In DAT  
- **osc_out_dat.txt** → used by `/project1/scripts/osc_helpers.py` to send messages via OSC Out DAT

These `.txt` files let you edit all your DAT logic in VSCode, then hot-reload in TD.

## JSON Schemas

- **osc_patterns.json** maps generic cue names to OSC address templates.
- **resolume_mapping.json** translates those generic names to Resolume-specific addresses.
- **laser_mapping.json** does the same for laser controllers.

These files let `osc_helpers.handle_incoming` route a single generic message to multiple targets.