# Source Configs & Scripts

This folder contains all source-controlled code and configuration referenced by
the TouchDesigner project. The root README outlines the high-level philosophy of
keeping logic in Python and JSON rather than buried inside `.toe` networks.
Here you will find the modules and data that implement that approach.

This folder holds:

- `scripts/osc_helpers.py` – loads OSC patterns/mappings and sends messages.
- `scripts/ui_helpers.py` – helper utilities for building addresses from UI selections.
- `scripts/ui_builder.py` – constructs a small address-builder UI component within TouchDesigner.
- `DATs/*.py` – callback scripts executed by TouchDesigner (see below).
- `scripts/routing_engine.py` – wraps `osc_helpers` with a simple `route_message`
  API for the rest of the project.
- `scripts/address_generators.py` – utilities that produce large mapping tables
  for Resolume and Onyx.

<!-- Example configs live in `config/routing_map.json`, `config/input_aliases.json`, and `config/endpoints.json`. -->

- `*.json` → OSC patterns & software mappings  
- `scripts/` → Python modules that handle OSC input, routing, and UI logic  

## DATs Directory

`src/DATs/` holds the external Python DAT scripts:

- **osc_exec_in.py** → hooked into `/project1/dat_execute_in` DAT Execute DAT. It now exposes `send_from_ui()` so UI elements can trigger OSC messages directly.
- **osc_in.py** → optional template for `/project1/osc_in_dat` OSC In DAT
- **osc_out.py** → used by `/project1/scripts/osc_helpers.py` to send messages via OSC Out DAT
- **init_path.py** → adds `src/scripts` to `sys.path` when the project starts so
  all modules can be imported inside TouchDesigner.

These `.py` files let you edit all your DAT logic in VSCode, then hot-reload in TD. Plain-text `.txt` versions work the same way if you prefer that extension.

## JSON Schemas

- **osc_patterns.json** maps generic cue names to OSC address templates.
- **resolume_mapping.json** translates those generic names to Resolume-specific addresses.
- **laser_mapping.json** does the same for laser controllers.
- **onyx_mapping.json** maps generic cues to Obsidian Onyx lighting commands.

These files let `routing_engine.route_message` route a single generic message to multiple targets.

`resolume_mapping.json` and `onyx_mapping.json` can be regenerated using
`scripts/address_generators.py` if you need more layers or playbacks.
The `ui_builder.create_address_builder()` function adds a small component to
your project. Trigger its button to call `osc_exec_in.send_from_ui()` and send
the composed OSC message via the router.
