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
