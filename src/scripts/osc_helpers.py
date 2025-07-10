from __future__ import annotations
import json
import os
from typing import Any, List

# TouchDesigner provides a global `op` function for looking up operators.
# When running outside of TD (e.g. unit tests or static analysis), that
# function is missing, so supply a dummy fallback.
if 'op' not in globals():  # pragma: no cover - used only for type checking
    def op(_path):  # type: ignore
        return None

# Resolve paths relative to this script
SRC_DIR = os.path.dirname(os.path.dirname(__file__))
PATTERNS_PATH = os.path.join(SRC_DIR, 'osc_patterns.json')
MAPPING_FILES = [
    os.path.join(SRC_DIR, 'resolume_mapping.json'),
    os.path.join(SRC_DIR, 'laser_mapping.json'),
]

_patterns: dict[str, Any] = {}
_mappings: dict[str, Any] = {}

def _read_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _load_configs() -> None:
    """Load pattern routing rules and merge mapping files."""
    global _patterns, _mappings
    _patterns = _read_json(PATTERNS_PATH)
    _mappings = {}
    for mf in MAPPING_FILES:
        _mappings.update(_read_json(mf))

# Load configs on import
_load_configs()

def handle_outgoing(address: str, value: Any) -> None:
    """Send an OSC message via the osc_out DAT."""
    out = op('osc_out')
    if not out:
        return
    out.clear()
    out.appendRow([address, value])
    out.send()

def handle_incoming(address: str, value: Any) -> List[str]:
    """Translate a generic OSC address into target-specific messages."""
    generics = _patterns.get(address)
    if not generics:
        return []

    if not isinstance(generics, list):
        generics = [generics]

    sent: List[str] = []
    for key in generics:
        mapped = _mappings.get(key)
        if not mapped:
            continue
        if isinstance(mapped, list):
            for dest in mapped:
                handle_outgoing(dest, value)
                sent.append(dest)
        else:
            handle_outgoing(mapped, value)
            sent.append(mapped)
    return sent

def reload_mappings() -> None:
    """Public helper to reload JSON routing data at runtime."""
    _load_configs()
