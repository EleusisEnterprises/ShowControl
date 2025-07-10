import sys
import os

# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
 # Add the TouchDesigner project folder to sys.path
 proj_folder = project.folder
 if proj_folder not in sys.path:
    sys.path.append(proj_folder)

 # Add your scripts folder to sys.path
 scripts_folder = os.path.join(proj_folder, 'src', 'scripts')
 if scripts_folder not in sys.path:
    sys.path.append(scripts_folder)
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
	return

def onProjectPostSave():
	return

	