"""
Module for generating OSC patterns based on user selections within TouchDesigner.

This script is intended to be linked to a Text DAT in a TouchDesigner project.
It provides functions that TouchDesigner UI components (like dropdowns and text inputs)
can call to dynamically generate OSC addresses and values for various control actions
across different integrated systems (e.g., Onyx, Resolume).
"""

import sys
import os
from typing import Any, Dict, List, Literal, Tuple, Union

# --- Path Configuration for Module Imports ---
# This block ensures that the script can correctly import sibling modules
# (like src.onyx.patterns and src.resolume.patterns) when run within TouchDesigner.
# TouchDesigner's default sys.path might not include the project root,
# which is necessary for absolute imports from 'src'.
script_dir = os.path.dirname(__file__)
# Navigate up two levels from 'src/router/' to reach the project root 'C:/Users/corey/ShowControl/'
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Import Pattern Generation Modules ---
# Attempt to import the specific pattern generation modules.
# These modules contain the functions that define how OSC addresses are structured
# for different target systems (e.g., Onyx lighting console, Resolume Arena).
try:
    from src.onyx import patterns as onyx_patterns
    from src.resolume import patterns as resolume_patterns
except ImportError as e:
    # This error handling is crucial for debugging within TouchDesigner.
    # If the imports fail (e.g., due to incorrect sys.path or missing files),
    # it will print an informative message to the TouchDesigner Textport.
    print(f"Error importing patterns modules: {e}")
    print(f"sys.path: {sys.path}")
    # Set patterns to None to prevent errors when accessing their functions later
    onyx_patterns = None
    resolume_patterns = None

# --- OSC Action Definitions ---
# This dictionary is the core configuration for the UI.
# It defines all the available OSC control actions that the user can select.
# Each entry maps a user-friendly action name (e.g., "Onyx: Set Fader")
# to its corresponding Python function and a list of its required parameters.
#
# Structure of each parameter definition:
# - "name": The keyword argument name for the function.
# - "type": The expected Python type (int, float, bool, str). Used for type conversion.
# - "min", "max": (Optional) Range constraints for numerical inputs.
# - "default": (Optional) Default value for the parameter.
# - "options": (Optional) For string types, a list of valid choices (e.g., for Literal types).
OSC_ACTIONS: Dict[str, Dict[str, Any]] = {
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

# --- Public Functions for TouchDesigner Integration ---

def get_action_names() -> List[str]:
    """
    Returns a list of all available OSC action names.
    This function is typically called by a TouchDesigner Dropdown COMP
    to populate its menu options.
    """
    return list(OSC_ACTIONS.keys())

def get_action_parameters(action_name: str) -> List[Dict[str, Any]]:
    """
    Returns the parameter definitions for a given OSC action.
    This function is called by TouchDesigner to dynamically create or
    configure input fields (e.g., Text COMPs, Sliders, Toggles)
    based on the selected action.

    Args:
        action_name (str): The user-friendly name of the OSC action.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each describing a parameter.
                              Returns an empty list if the action is not found.
    """
    return OSC_ACTIONS.get(action_name, {}).get("params", [])

def generate_osc_message(action_name: str, **kwargs: Union[str, int, float, bool]) -> Tuple[Union[str, None], Union[int, float, None]]:
    """
    Generates the OSC address and value for a given action and its parameters.
    This is the primary function called by a TouchDesigner Button COMP or similar
    to trigger the OSC message generation.

    Args:
        action_name (str): The name of the action (e.g., "Onyx: Set Fader").
        **kwargs: Keyword arguments representing the user-provided values for
                  the parameters of the selected action. These values typically
                  come from TouchDesigner UI input COMPs.

    Returns:
        Tuple[Union[str, None], Union[int, float, None]]:
            A tuple containing the generated OSC address (str) and value (int or float).
            Returns (None, None) if the action is not found, its function is not loaded,
            or an error occurs during message generation.
    """
    action_info = OSC_ACTIONS.get(action_name)
    if not action_info or not action_info["func"]:
        print(f"Error: Action '{action_name}' not found or its associated function is not loaded.")
        return None, None

    func = action_info["func"]
    try:
        # Prepare parameters for the pattern generation function.
        # This loop filters kwargs to only include parameters expected by the function
        # and performs necessary type conversions from string inputs (common from TD UI).
        func_params: Dict[str, Any] = {}
        for param_def in action_info["params"]:
            param_name = param_def["name"]
            if param_name in kwargs:
                # Perform type conversion based on the defined parameter type.
                # TouchDesigner UI inputs often return values as strings,
                # so explicit conversion is necessary.
                if param_def["type"] == int:
                    func_params[param_name] = int(kwargs[param_name])
                elif param_def["type"] == float:
                    func_params[param_name] = float(kwargs[param_name])
                elif param_def["type"] == bool:
                    # Boolean values from TD often come as 0 or 1 (int or string).
                    # Convert to int first, then to bool.
                    func_params[param_name] = bool(int(kwargs[param_name]))
                else:  # Default to string for 'str' or 'Literal' types
                    func_params[param_name] = kwargs[param_name]
            else:
                # If a parameter is not provided in kwargs, use its default value if available.
                if "default" in param_def:
                    func_params[param_name] = param_def["default"]
                else:
                    # Log a warning if a required parameter is missing and has no default.
                    print(f"Warning: Parameter '{param_name}' missing for action '{action_name}' and no default provided.")

        # Call the specific pattern generation function with the prepared parameters.
        address, value = func(**func_params)
        return address, value
    except Exception as e:
        # Catch any errors during function execution and log them to the Textport.
        print(f"Error generating OSC message for '{action_name}': {e}")
        return None, None

# --- Example Usage (for testing within a standard Python environment) ---
# This block is executed only when the script is run directly (not imported as a module).
# It provides a way to test the functions without needing TouchDesigner.
if __name__ == '__main__':
    print("--- OSC Pattern Generator Test ---")
    print("\nAvailable Actions:", get_action_names())

    # Example 1: Get parameters for "Onyx: Set Fader"
    fader_params = get_action_parameters("Onyx: Set Fader")
    print("\nOnyx: Set Fader Parameters:", fader_params)

    # Example 2: Generate OSC message for "Onyx: Set Fader"
    # Simulate inputs from TD UI (e.g., fader_id=4203, value=128)
    address, value = generate_osc_message("Onyx: Set Fader", fader_id=4203, value=128)
    print(f"Generated OSC: Address='{address}', Value='{value}'")

    # Example 3: Generate OSC message for "Resolume: Trigger Clip"
    # Simulate inputs from TD UI (e.g., layer=1, clip=5, connected=1 for True)
    address, value = generate_osc_message("Resolume: Trigger Clip", layer=1, clip=5, connected=1)
    print(f"Generated OSC: Address='{address}', Value='{value}'")

    # Example 4: Generate OSC message for "Onyx: Playback Action"
    # Simulate inputs from TD UI (e.g., page=1, playback=3, action="go")
    address, value = generate_osc_message("Onyx: Playback Action", page=1, playback=3, action="go")
    print(f"Generated OSC: Address='{address}', Value='{value}'")

    # Example 5: Test with missing parameter (should use default)
    address, value = generate_osc_message("Onyx: Press Button", button_id=10) # 'pressed' will use default True
    print(f"Generated OSC (Button with default): Address='{address}', Value='{value}'")

    # Example 6: Test with non-existent action
    address, value = generate_osc_message("NonExistent: Action", some_param=1)
    print(f"Generated OSC (Non-existent): Address='{address}', Value='{value}'")