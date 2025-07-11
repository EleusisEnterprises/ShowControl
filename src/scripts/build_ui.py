
"""
This script builds a user interface inside a specified component in TouchDesigner.
It is designed to be called by a runner script.
"""

# --- SCRIPT ---
from src.onyx import patterns as onyx_patterns
from src.resolume import patterns as resolume_patterns

def build_ui(target_op):
    """The main function to build the UI inside the target_op."""
    if not target_op:
        msg = "Error: Invalid target component provided to build_ui."
        print(msg)
        ui.messageBox('Error', msg)
        return

    print(f"Building UI inside {target_op.path}...")

    # --- Clear existing UI to prevent duplicates ---
    print("Clearing old UI elements...")
    for child in target_op.findChildren(depth=1):
        if child.name.startswith('ui_'):
            child.destroy()

    # --- Create Onyx Controls ---
    print("Creating Onyx controls...")
    onyx_label = target_op.create(labelCOMP, 'ui_onyx_label')
    onyx_label.par.text = 'Onyx Playback Faders'
    onyx_label.par.alignx = 'left'
    onyx_label.nodeX = -400
    onyx_label.nodeY = 400

    for i in range(10):
        fader_num = i + 1
        fader_id = 4203 + (i * 10)
        slider_name = f'ui_onyx_fader_{fader_num}'
        slider = target_op.create(sliderCOMP, slider_name)
        
        slider.nodeX = -400 + (i * 120)
        slider.nodeY = 300
        slider.par.label = f'Fader {fader_num}'
        
        osc_address, _ = onyx_patterns.set_fader(fader_id, 0)
        # Add a comment with the OSC address for easy debugging
        slider.par.help = f"OSC Address: {osc_address}"

    # --- Create Resolume Controls ---
    print("Creating Resolume controls...")
    resolume_label = target_op.create(labelCOMP, 'ui_resolume_label')
    resolume_label.par.text = 'Resolume Layer Opacity'
    resolume_label.par.alignx = 'left'
    resolume_label.nodeX = -400
    resolume_label.nodeY = 150

    for i in range(5):
        layer_num = i + 1
        slider_name = f'ui_resolume_layer_{layer_num}'
        slider = target_op.create(sliderCOMP, slider_name)
        
        slider.nodeX = -400 + (i * 120)
        slider.nodeY = 50
        slider.par.label = f'Layer {layer_num} Opacity'
        
        osc_address, _ = resolume_patterns.set_layer_opacity(layer_num, 0.0)
        # Add a comment with the OSC address for easy debugging
        slider.par.help = f"OSC Address: {osc_address}"

    print("UI creation complete.")
    print("Connect sliders to an OSC Out CHOP to make them functional.")

# This script is not meant to be run directly anymore.
# It should be called by a runner script inside TouchDesigner.
if __name__ == '__main__':
    print("This script is designed to be imported and called from a runner, not run directly.")
