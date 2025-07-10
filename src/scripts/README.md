# Python Helper Scripts

All external Python code used by TouchDesigner lives here:

- `osc_helpers.py` – loads routing JSON, maps incoming OSC messages, and sends
  them out again. The `handle_incoming(address, value)` function now accepts the
  parameters passed by `osc_exec_in.py`, looks up the address in
  `osc_patterns.json`, translates the result through mapping files (e.g.,
  `resolume_mapping.json`), and forwards each destination address/value via
  `handle_outgoing`.
- `ui_helpers.py` – build addresses from UI selections and expose helper
  functions.
