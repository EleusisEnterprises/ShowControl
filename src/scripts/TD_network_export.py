# export_selected_comps.py

import json

# Names of top-level COMPs or DATs you want to include
TARGET = {
    'Onyx',
    'Quickshow',
    'Resolume',
    'Router',
    'APCmini',
    'APC40',
    'scripts',
    'TD_network_export'  # your Execute DAT
}

def walk(node):
    """
    Recursively capture this node and its children,
    but only descend into COMPs/DATs under TARGET.
    """
    info = {
        "name": node.name,
        "type": node.opType,
        "path": node.path,
        "children": []
    }
    for child in node.children:
        # Only include children inside a TARGET branch
        # (we only descend if the *top* parent was in TARGET)
        info["children"].append({
            "name": child.name,
            "type": child.opType,
            "path": child.path
        })
    return info

# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
	return

def onCreate():
	return

def onExit():
	return

def onFrameStart(frame):
	return

def onFrameEnd(frame):
	return

def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
    root = op('/')  # absolute root
    export_list = []

    for c in root.children:
        if c.name in TARGET:
            export_list.append(walk(c))

    out = project.folder + '/td_selected_comps.json'
    with open(out, 'w') as f:
        json.dump(export_list, f, indent=2)
    debug(f"▶️ Exported {len(export_list)} selected COMPs to {out}")
    return