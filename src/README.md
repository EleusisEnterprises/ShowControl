# Source Configs & Scripts

This folder holds:  

- `*.json` → OSC patterns & software mappings  
- `scripts/` → Python modules that handle OSC input, routing, and UI logic  

## DATs Directory

`src/DATs/` holds the external, editable Text DAT scripts:

- **dat_execute_in.txt** → hooked into `/project1/dat_execute_in` DAT Execute DAT  
- **osc_in_dat.txt** → optional template for `/project1/osc_in_dat` OSC In DAT  
- **osc_out_dat.txt** → used by `/project1/scripts/osc_helpers.py` to send messages via OSC Out DAT

These `.txt` files let you edit all your DAT logic in VSCode, then hot-reload in TD.
