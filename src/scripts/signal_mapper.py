
from typing import Any, Tuple, Optional

OSC_ADDRESS_MAP = {
    '/fader/1': 'fader_1',
    '/fader/2': 'fader_2',
    '/button/1': 'button_1',
}

INVERSE_OSC_ADDRESS_MAP = {v: k for k, v in OSC_ADDRESS_MAP.items()}

def detect_signal_type(data: Any) -> str:
    """Return the signal type based on the payload structure."""
    if isinstance(data, dict):
        if {'note', 'velocity'} <= data.keys() or {'cc', 'value'} <= data.keys():
            return 'MIDI'
        if 'address' in data:
            return 'OSC'
        if {'dmx_ch', 'value'} <= data.keys() or {'universe', 'channel'} <= data.keys():
            return 'DMX'
    if isinstance(data, (bytes, bytearray)) and len(data) in (2, 3):
        return 'MIDI'
    return 'UNKNOWN'


def normalize_value(value: float, src_min: float, src_max: float, dst_min: float = 0.0,
                     dst_max: float = 1.0) -> float:
    """Normalize a value from a source range to a destination range."""
    if src_max == src_min:
        raise ValueError('Invalid source range')
    ratio = (value - src_min) / (src_max - src_min)
    return dst_min + ratio * (dst_max - dst_min)


def map_osc_to_internal(address: str) -> Optional[str]:
    """Convert an OSC address to an internal control name."""
    return OSC_ADDRESS_MAP.get(address)


def map_internal_to_osc(name: str) -> Optional[str]:
    """Convert an internal control name to an OSC address."""
    return INVERSE_OSC_ADDRESS_MAP.get(name)


def parse_osc_message(address: str, args: list) -> Tuple[Optional[str], Optional[Any]]:
    """Parse an incoming OSC message to an internal control and value."""
    name = map_osc_to_internal(address)
    value = args[0] if args else None
    return name, value

