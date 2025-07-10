"""Core logic for routing incoming signals to destinations."""

from typing import Any, Dict


class RoutingEngine:
    """Simple routing engine placeholder."""

    def __init__(self) -> None:
        # mapping of input name to output address
        self.routes: Dict[str, str] = {}

    def add_route(self, source: str, destination: str) -> None:
        """Register a mapping from a source signal to an OSC address."""
        self.routes[source] = destination

    def route(self, source: str, *payload: Any) -> None:
        """Route the incoming payload if a mapping exists."""
        dest = self.routes.get(source)
        if dest:
            from .osc_utils import OSCClient

            client = OSCClient()
            client.send(dest, *payload)
        else:
            print(f"No route for {source}")
