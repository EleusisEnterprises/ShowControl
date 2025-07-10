"""Utility functions for Open Sound Control communication."""

from typing import Any, Iterable


class OSCClient:
    """Very small placeholder OSC client."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        self.host = host
        self.port = port

    def send(self, address: str, *args: Any) -> None:
        """Pretend to send an OSC message to the configured host/port."""
        msg = f"OSC -> {self.host}:{self.port} {address} {args}"
        print(msg)


def bundle(messages: Iterable[tuple[str, tuple[Any, ...]]]) -> None:
    """Send a bundle of OSC messages.

    Parameters
    ----------
    messages:
        Iterable of tuples in the form ``(address, args)``.
    """
    client = OSCClient()
    for addr, args in messages:
        client.send(addr, *args)
