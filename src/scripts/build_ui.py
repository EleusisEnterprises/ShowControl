
"""
This script builds a user interface inside a specified component in TouchDesigner.
It is designed to be run from a Text DAT within a TouchDesigner project.

This script now uses the patterns modules to generate OSC addresses, ensuring
consistency with the rest of the project.

Instructions:
1.  In your TouchDesigner project, create a new Text DAT.
2.  Copy and paste the entire content of this script into the Text DAT.
3.  Modify the `ROUTER_PATH` variable below to point to your router component if it's not '/project1/router'.
4.  Right-click on the Text DAT and select 'Run Script'.
5.  The script will create sliders for Onyx and Resolume inside your router component.

To make the sliders functional, you will need to connect them to an OSC Out CHOP
to send OSC messages. This script adds comments on how to achieve this.
"""

# --- CONFIGURATION ---
# IMPORTANT: Change this path to match the location of your router component.
ROUTER_PATH = '/project1/router'

# --- SCRIPT ---
# Import the pattern modules to generate OSC addresses
from src.onyx import patterns as onyx_patterns
from src.resolume import patterns as resolume_patterns

def build_ui():
    """The main function to build the UI."""
    try:
        import td
    except ImportError:
        print("This script must be run inside TouchDesigner.")
        ui.messageBox("Error", "This script must be run inside TouchDesigner.")
        return

    router_op = op(ROUTER_PATH)
    if not router_op:
        msg = f"Error: Component not found at '{ROUTER_PATH}'. Please check the ROUTER_PATH variable in this script."
        print(msg)
        ui.messageBox('Error', msg)
        return

    # --- Clear existing UI to prevent duplicates ---
    print("Clearing old UI elements...")
    for child in router_op.findChildren(depth=1):
        if child.name.startswith('ui_'):
            child.destroy()

    # --- Create Onyx Controls ---
    print("Creating Onyx controls...")
    onyx_label = router_op.create(labelCOMP, 'ui_onyx_label')
    onyx_label.par.text = 'Onyx Playback Faders'
    onyx_label.par.alignx = 'left'
    onyx_label.nodeX = -400
    onyx_label.nodeY = 400

    for i in range(10):
        fader_num = i + 1
        # According to ONYXCONTEXT.md, fader IDs start at 4203 and increment by 10
        fader_id = 4203 + (i * 10)
        slider_name = f'ui_onyx_fader_{fader_num}'
        slider = router_op.create(sliderCOMP, slider_name)
        
        slider.nodeX = -400 + (i * 120)
        slider.nodeY = 300
        
        slider.par.label = f'Fader {fader_num}'
        
        # Generate the OSC address using the patterns module
        osc_address, _ = onyx_patterns.set_fader(fader_id, 0) # value is a placeholder

        # To make this slider send OSC:
        # 1. Create an OSC Out CHOP.
        # 2. Set its 'Network Address' to the target device's IP.
        # 3. Set its 'Port' to the target's listening port (e.g., 9000 for Onyx).
        # 4. In the OSC Out CHOP's parameters, set 'CHOP to' to this slider's CHOP output.
        # 5. Set the 'OSC Address' parameter to the generated address: {osc_address}
        # 6. The slider's value range is 0-1. Onyx expects 0-255.
        #    You can use a Math CHOP between the slider and the OSC Out CHOP
        #    to multiply the value by 255.

    # --- Create Resolume Controls ---
    print("Creating Resolume controls...")
    resolume_label = router_op.create(labelCOMP, 'ui_resolume_label')
    resolume_label.par.text = 'Resolume Layer Opacity'
    resolume_label.par.alignx = 'left'
    resolume_label.nodeX = -400
    resolume_label.nodeY = 150

    for i in range(5): # Create controls for 5 layers
        layer_num = i + 1
        slider_name = f'ui_resolume_layer_{layer_num}'
        slider = router_op.create(sliderCOMP, slider_name)
        
        slider.nodeX = -400 + (i * 120)
        slider.nodeY = 50
        
        slider.par.label = f'Layer {layer_num} Opacity'
        
        # Generate the OSC address using the patterns module
        osc_address, _ = resolume_patterns.set_layer_opacity(layer_num, 0.0) # value is a placeholder

        # To make this slider send OSC:
        # 1. Use the same OSC Out CHOP as for Onyx, or a new one for Resolume.
        # 2. Connect this slider's output to it.
        # 3. Set the 'OSC Address' to the generated address: {osc_address}
        # 4. The slider's 0-1 value range matches what Resolume expects for opacity.

    print("UI creation complete.")
    print("Please connect the sliders to OSC Out CHOPs to make them functional.")

# --- Run the script ---
if __name__ == '__main__':
    build_ui()
