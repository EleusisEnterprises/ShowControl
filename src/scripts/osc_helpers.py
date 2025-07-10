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
