# `router/` – Central Signal Hub

Handles the normalized signal intake and dispatch. This is the logic that
receives named and normalized controls from all devices and routes them to
their destinations.

The `osc_in_callbacks` module now leverages `signal_mapper` to interpret incoming
OSC messages. Parsed signals are forwarded using `signal_router.dispatch` which
will invoke a registered handler or log the value if no handler is present.

Expected behavior:

1. OSC addresses matching `/signal/<name>` with a numeric argument are
   normalized to a 0–1 range.
2. Messages with unknown addresses or unsupported types are logged and ignored.
3. A custom handler may be registered via `signal_router.set_handler` to receive
   `(name, value)` pairs for further routing.

Additional modules in this folder may include GUI handlers, mapping logic, and
routing configuration loaders.

## `osc_pattern_generator.py`

This new module facilitates the dynamic generation of OSC addresses and values
based on user selections within a TouchDesigner UI. It acts as a bridge between
the user interface and the underlying pattern generation logic defined in modules
like `src/onyx/patterns.py` and `src/resolume/patterns.py`.

It exposes functions (`get_action_names`, `get_action_parameters`,
`generate_osc_message`) that can be called directly from TouchDesigner Python
scripts to:

- Populate dropdown menus with available OSC control actions.
- Retrieve parameter definitions for selected actions to dynamically build UI input fields.
- Generate the final OSC address and value tuple for sending.

This allows for a flexible and extensible UI for controlling various systems
via OSC without hardcoding addresses.