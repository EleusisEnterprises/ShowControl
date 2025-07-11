
"""
This is the runner script for building the TouchDesigner UI.

Instructions:
1.  Place the contents of this script into a Text DAT in your TouchDesigner project.
2.  Ensure your project's root directory (the one containing the 'src' folder) is
    added to the Python 64-bit Module Path in TouchDesigner's preferences
    (Edit > Preferences > General > Python 64-bit Module Path).
    Alternatively, this script attempts to add the project path automatically.
3.  Right-click the Text DAT and select 'Run Script'.

This script will import the build_ui function from the main script file
and execute it, building the UI in your router component.
"""

import sys
import os

# --- Add project root to Python path ---
# This allows TouchDesigner to find the 'src' module.
# Assumes the .toe file is in the project root.
project_root = project.folder
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    # Import the main UI building function
    from src.scripts.build_ui import build_ui
    
    # Execute the function
    print("Executing build_ui() from src.scripts.build_ui...")
    build_ui()
    print("UI build process finished.")

except ImportError as e:
    error_msg = f"Failed to import UI builder. Make sure the project root is in your Python path. Details: {e}"
    print(error_msg)
    ui.messageBox("Import Error", error_msg)
except Exception as e:
    error_msg = f"An unexpected error occurred: {e}"
    print(error_msg)
    ui.messageBox("Error", error_msg)
