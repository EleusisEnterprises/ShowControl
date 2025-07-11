
"""
Module for generating OSC patterns based on user selections.
This script is intended to be linked to a Text DAT in TouchDesigner.
"""

import sys
import os

# Add parent directory to sys.path to allow importing sibling modules
# This assumes the script is in src/router/
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from src.onyx import patterns as onyx_patterns
    from src.resolume import patterns as resolume_patterns
except ImportError as e:
    # This block is for debugging in case of import issues in TD
    print(f"Error importing patterns modules: {e}")
    print(f"sys.path: {sys.path}")
    onyx_patterns = None
    resolume_patterns = None

# Define the available actions and their associated functions and parameters
# This dictionary will drive the UI dropdown and input fields
OSC_ACTIONS = {
    "Onyx: Set Fader": {
        "func": onyx_patterns.set_fader if onyx_patterns else None,
        "params": [
            {"name": "fader_id", "type": int, "min": 0, "max": 9999, "default": 0},
            {"name": "value", "type": int, "min": 0, "max": 255, "default": 0}
        ]
    },
    "Onyx: Press Button": {
        "func": onyx_patterns.press_button if onyx_patterns else None,
        "params": [
            {"name": "button_id", "type": int, "min": 0, "max": 9999, "default": 0},
            {"name": "pressed", "type": bool, "default": True}
        ]
    },
    "Onyx: Playback Action": {
        "func": onyx_patterns.playback_action if onyx_patterns else None,
        "params": [
            {"name": "page", "type": int, "min": 1, "max": 99, "default": 1},
            {"name": "playback", "type": int, "min": 1, "max": 99, "default": 1},
            {"name": "action", "type": str, "options": ["go", "pause", "release", "select"], "default": "go"}
        ]
    },
    "Resolume: Set Layer Opacity": {
        "func": resolume_patterns.set_layer_opacity if resolume_patterns else None,
        "params": [
            {"name": "layer", "type": int, "min": 1, "max": 99, "default": 1},
            {"name": "opacity", "type": float, "min": 0.0, "max": 1.0, "default": 1.0}
        ]
    },
    "Resolume: Trigger Clip": {
        "func": resolume_patterns.trigger_clip if resolume_patterns else None,
        "params": [
            {"name": "layer", "type": int, "min": 1, "max": 99, "default": 1},
            {"name": "clip", "type": int, "min": 1, "max": 99, "default": 1},
            {"name": "connected", "type": bool, "default": True}
        ]
    },
}

def get_action_names():
    """Returns a list of all available action names for the dropdown."""
    return list(OSC_ACTIONS.keys())

def get_action_parameters(action_name):
    """Returns the parameter definitions for a given action name."""
    return OSC_ACTIONS.get(action_name, {}).get("params", [])

def generate_osc_message(action_name, **kwargs):
    """
    Generates the OSC address and value for a given action and its parameters.

    Args:
        action_name (str): The name of the action (e.g., "Onyx: Set Fader").
        **kwargs: Keyword arguments for the parameters of the selected action.

    Returns:
        tuple: (osc_address, osc_value) or (None, None) if action not found or error.
    """
    action_info = OSC_ACTIONS.get(action_name)
    if not action_info or not action_info["func"]:
        print(f"Error: Action '{action_name}' not found or function not loaded.")
        return None, None

    func = action_info["func"]
    try:
        # Filter kwargs to only include parameters expected by the function
        # and convert types as necessary
        func_params = {}
        for param_def in action_info["params"]:
            param_name = param_def["name"]
            if param_name in kwargs:
                # Type conversion
                if param_def["type"] == int:
                    func_params[param_name] = int(kwargs[param_name])
                elif param_def["type"] == float:
                    func_params[param_name] = float(kwargs[param_name])
                elif param_def["type"] == bool:
                    # Assuming boolean comes as 0 or 1 from TD
                    func_params[param_name] = bool(int(kwargs[param_name]))
                else: # str or Literal
                    func_params[param_name] = kwargs[param_name]
            else:
                # Use default if parameter not provided
                if "default" in param_def:
                    func_params[param_name] = param_def["default"]
                else:
                    print(f"Warning: Parameter '{param_name}' missing for action '{action_name}' and no default provided.")

        address, value = func(**func_params)
        return address, value
    except Exception as e:
        print(f"Error generating OSC message for '{action_name}': {e}")
        return None, None

# Example Usage (for testing within Python, not for TD directly)
if __name__ == '__main__':
    print("Available Actions:", get_action_names())

    # Example: Get parameters for "Onyx: Set Fader"
    fader_params = get_action_parameters("Onyx: Set Fader")
    print("Onyx: Set Fader Parameters:", fader_params)

    # Example: Generate OSC message for "Onyx: Set Fader"
    address, value = generate_osc_message("Onyx: Set Fader", fader_id=4203, value=128)
    print(f"Generated OSC: Address='{address}', Value='{value}'")

    # Example: Generate OSC message for "Resolume: Trigger Clip"
    address, value = generate_osc_message("Resolume: Trigger Clip", layer=1, clip=5, connected=1) # connected=1 for True
    print(f"Generated OSC: Address='{address}', Value='{value}'")

    # Example: Playback Action
    address, value = generate_osc_message("Onyx: Playback Action", page=1, playback=3, action="go")
    print(f"Generated OSC: Address='{address}', Value='{value}'")
