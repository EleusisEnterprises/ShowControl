
import os, json

# Load configuration files relative to this script
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PATTERNS_FILE = os.path.join(BASE_DIR, 'osc_patterns.json')
RESOLUME_FILE = os.path.join(BASE_DIR, 'resolume_mapping.json')
LASER_FILE = os.path.join(BASE_DIR, 'laser_mapping.json')

with open(PATTERNS_FILE) as f:
    OSC_PATTERNS = json.load(f)
with open(RESOLUME_FILE) as f:
    RESOLUME_MAP = json.load(f)
with open(LASER_FILE) as f:
    LASER_MAP = json.load(f)

def handle_outgoing(address, value):
    out = op('osc_out')
=======
import json
import os

# Resolve paths relative to this file
SRC_DIR = os.path.dirname(os.path.dirname(__file__))
PATTERNS_PATH = os.path.join(SRC_DIR, 'osc_patterns.json')
MAPPING_FILES = [
    os.path.join(SRC_DIR, 'resolume_mapping.json'),
    os.path.join(SRC_DIR, 'laser_mapping.json'),
]

_patterns = {}
_mappings = {}

def _read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Invalid JSON or empty file
            return {}


def _load_configs():
    """Load pattern routing rules and merge mapping files."""
    global _patterns, _mappings
    _patterns = _read_json(PATTERNS_PATH)
    _mappings = {}
    for mf in MAPPING_FILES:
        _mappings.update(_read_json(mf))


# Load configs on import
_load_configs()


def handle_outgoing(address, value):
    """Send an OSC message via the osc_out DAT."""
    out = op('osc_out')  # get the outgoing OSC table operator

    out.clear()
    out.appendRow([address, value])
    out.send()


def handle_incoming(address, value):
    """Translate generic OSC messages into target-specific addresses."""
    messages = []
    key = None
    for name, pattern in OSC_PATTERNS.items():
        if address == pattern:
            key = name
            break
    if key is None:
        return messages

    if key in RESOLUME_MAP:
        target = RESOLUME_MAP[key]
        handle_outgoing(target, value)
        messages.append(target)
    if key in LASER_MAP:
        target = LASER_MAP[key]
        handle_outgoing(target, value)
        messages.append(target)
    return messages
    """Map an incoming OSC address/value to one or more outgoing messages."""
    # Obtain generic keys for this incoming address
    generics = _patterns.get(address)
    if not generics:
        return  # nothing mapped

    if not isinstance(generics, list):
        generics = [generics]

    for key in generics:
        mapped = _mappings.get(key)
        if not mapped:
            continue
        if isinstance(mapped, list):
            for dest in mapped:
                handle_outgoing(dest, value)
        else:
            handle_outgoing(mapped, value)


def reload_mappings():
    """Public helper to reload JSON routing data at runtime."""
    _load_configs()
