# Python Helper Scripts

All external Python code used by TouchDesigner lives here:

- `osc_helpers.py` – loads routing JSON, maps incoming OSC messages, and sends
  them out again. The `handle_incoming(address, value)` function now accepts the
  parameters passed by `osc_exec_in.py`, looks up the address in
  `osc_patterns.json`, translates the result through mapping files (e.g.,
  `resolume_mapping.json`), and forwards each destination address/value via
  `handle_outgoing`.
- `routing_engine.py` – higher level router that exposes `route_message` to
  resolve generic addresses using those mappings and substitute parameters
  before forwarding the OSC data.
- `ui_helpers.py` – build addresses from UI selections and expose helper
  functions.

## Function Overview

### osc_helpers.py

- **handle_outgoing(address, value)** – send a single OSC message via the `osc_out` DAT.
- **handle_incoming()** – placeholder to process queued OSC messages.

### routing_engine.py

- **route_message(address, value)** – look up `address` in the loaded pattern
  tables and send formatted destination messages using `osc_helpers.handle_outgoing`.

### ui_helpers.py

- **get_selected_layer(dropdown)** – return the selected label from a Dropdown COMP.
- **get_numeric_value(field)** – fetch a numeric value from a parameter or field COMP.
- **build_osc_address(parts)** – join elements into a sanitized OSC address.
- **assemble_osc_address(layer_dd, channel_dd, index_field=None)** – combine UI selections into `/layer/channel/index`.
