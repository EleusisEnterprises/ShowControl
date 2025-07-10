# Python Helper Scripts

All external Python code used by TouchDesigner lives here. These modules are
imported by the Text DATs in `src/DATs/` and can also be executed outside of
TouchDesigner for headless testing.

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
- `ui_builder.py` – convenience utilities that create a small address builder
  COMP and wire its button to `osc_exec_in.send_from_ui()`.
- `address_generators.py` – scripts that generate large mapping tables
  (e.g. Resolume layers or Onyx playbacks) and write them to the JSON files.

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

### ui_builder.py

- **create_address_builder(parent, name='osc_address_builder')** – add a
  ready-made UI component that assembles an OSC address and sends it through the
  routing engine when its button is pressed.

### address_generators.py

- **generate_resolume_mapping(layers=4, clips_per_layer=4)** – produce a mapping
  dictionary for Resolume addresses.
- **generate_onyx_mapping(playbacks=20)** – produce an Onyx playback mapping.
