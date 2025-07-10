from __future__ import annotations

"""Helper functions to generate OSC mapping dictionaries."""

from typing import Dict


def generate_resolume_mapping(layers: int = 4, clips_per_layer: int = 4) -> Dict[str, str]:
    """Return a mapping dictionary for Resolume addresses."""
    mapping: Dict[str, str] = {
        "master_dimmer": "/composition/video/opacity",
    }
    for layer in range(1, layers + 1):
        mapping[f"layer_{layer}_opacity"] = f"/composition/layers/{layer}/video/opacity"
        for clip in range(1, clips_per_layer + 1):
            key = f"layer_{layer}_clip_{clip}_connect"
            mapping[key] = f"/composition/layers/{layer}/clips/{clip}/connect"
    return mapping


def generate_onyx_mapping(playbacks: int = 20) -> Dict[str, str]:
    """Return a mapping dictionary for Onyx playback controls."""
    mapping: Dict[str, str] = {}
    for pb in range(1, playbacks + 1):
        if pb <= 10:
            base = 4200 + (pb - 1) * 10
        else:
            base = 4600 + (pb - 11) * 10
        mapping[f"playback_{pb}_go"] = f"/Mx/button/{base + 1}"
        mapping[f"playback_{pb}_pause"] = f"/Mx/button/{base + 2}"
        mapping[f"playback_{pb}_level"] = f"/Mx/fader/{base + 3}"
        mapping[f"playback_{pb}_select"] = f"/Mx/button/{base + 4}"
        mapping[f"playback_{pb}_flash"] = f"/Mx/button/{base + 5}"
    mapping["grand_master_level"] = "/Mx/fader/2202"
    mapping["grand_master_flash"] = "/Mx/button/2201"
    return mapping


if __name__ == "__main__":
    import json
    import os

    here = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(here, "resolume_mapping.json"), "w") as f:
        json.dump(generate_resolume_mapping(), f, indent=2)
    with open(os.path.join(here, "onyx_mapping.json"), "w") as f:
        json.dump(generate_onyx_mapping(), f, indent=2)
