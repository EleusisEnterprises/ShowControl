# Source Configs & Scripts

This folder holds:  

- `scripts/osc_helpers.py` – loads OSC patterns/mappings and sends messages.
- `scripts/ui_helpers.py` – helper utilities for building addresses from UI selections.
- `DATs/*.py` – callback scripts executed by TouchDesigner (see below).

<!-- Example configs live in `config/routing_map.json`, `config/input_aliases.json`, and `config/endpoints.json`. -->

- `*.json` → OSC patterns & software mappings  
- `scripts/` → Python modules that handle OSC input, routing, and UI logic  

## DATs Directory

`src/DATs/` holds the external Python DAT scripts:

- **osc_exec_in.py** → hooked into `/project1/dat_execute_in` DAT Execute DAT
- **osc_in.py** → optional template for `/project1/osc_in_dat` OSC In DAT
- **osc_out.py** → used by `/project1/scripts/osc_helpers.py` to send messages via OSC Out DAT

These `.py` files let you edit all your DAT logic in VSCode, then hot-reload in TD. Plain-text `.txt` versions work the same way if you prefer that extension.

## JSON Schemas

- **osc_patterns.json** maps generic cue names to OSC address templates.
- **resolume_mapping.json** translates those generic names to Resolume-specific addresses.
- **laser_mapping.json** does the same for laser controllers.

These files let `osc_helpers.handle_incoming` route a single generic message to multiple targets.
