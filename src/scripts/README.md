# Python Helper Scripts

All external Python code used by TouchDesigner lives here:

- `osc_helpers.py` → load JSON, route incoming OSC, fire outgoing OSC
- `ui_helpers.py` → build addresses from UI selections, expose helper functions

## Function Overview

### osc_helpers.py
- **handle_outgoing(address, value)** – send a single OSC message via the `osc_out` DAT.
- **handle_incoming()** – placeholder to process queued OSC messages.

### ui_helpers.py
- **get_selected_layer(dropdown)** – return the selected label from a Dropdown COMP.
- **get_numeric_value(field)** – fetch a numeric value from a parameter or field COMP.
- **build_osc_address(parts)** – join elements into a sanitized OSC address.
- **assemble_osc_address(layer_dd, channel_dd, index_field=None)** – combine UI selections into `/layer/channel/index`.
