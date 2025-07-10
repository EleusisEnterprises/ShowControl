# TouchDesigner Python Integration and Operator Overview

## Python Integration in TouchDesigner

TouchDesigner uses **Python 3** as its built-in scripting language for automating and controlling projects. A custom Python environment is included with TouchDesigner, providing specialized modules and classes (accessible via the `td` and `tdu` modules).

* **Operators as Python Objects**: Every node (Operator or *OP*) is represented by a Python object. Core classes include:

  * **OP Class**: Base for all operators, with methods like `name`, `path`, `children`, and `parent()`.
  * **Globals**: `me` (the operator running the script) and `root` (the project root).
  * **Access Helpers**: `op('path')` returns the OP at that path; `ops('pattern')` returns a list matching the pattern.

* **Controlling Parameters**: Operator parameters are accessed through the `par` member:

  ```python
  # Set the first channel value of a Constant CHOP named 'constant1'
  op('constant1').par.value0 = 5

  # Get an evaluated parameter value (useful if driven by an expression)
  width = op('sphere1').par.tx.eval()

  # Pulse a button parameter
  op('trigger1').par.pulse.pulse()
  ```

* **Expressions vs. Scripts**:

  * **Expressions**: Small Python snippets entered directly into parameter fields, returning values.
  * **DAT Scripts**: Held in Text DATs or specialized Execute DATs for event-driven logic.

* **Event Callbacks**: Execute DATs (CHOP Execute, DAT Execute, Panel Execute, etc.) provide callback templates such as `onValueChange()`, `onTableChange()`, `onClick()`, `onFrameStart()`, etc., enabling push-based reactions alongside TouchDesigner’s pull-based cooking.

* **Component Extensions**: Custom Python classes attached to COMPs add methods and persistent data, accessed via `comp.ext.ExtensionName` or promoted directly on the component.

## OP Types and Python Interaction

### CHOPs (Channel Operators)

Handle time-sliced numeric data—LFOs, audio, control signals.

* **Examples**: Constant CHOP, Wave CHOP, Noise CHOP, Trail CHOP.
* **Python**: Access channels and samples:

  ```python
  channel = op('noise1')['chan1']      # Channel object
  firstSample = channel[0]             # First sample value
  allChannels = op('noise1').chans()   # List of Channel objects
  array = op('noise1').numpyArray()    # 2D NumPy array of samples
  ```

### SOPs (Surface Operators)

Create and modify 3D geometry—meshes, curves, particles.

* **Examples**: Sphere SOP, Box SOP, Transform SOP, Merge SOP, Script SOP.
* **Python**: Modify parameters or generate geometry:

  ```python
  # Change a Sphere SOP radius
  op('sphere1').par.radiusx = 2

  # Script SOP cook callback
  def cook(scriptOP):
      scriptOP.clear()
      for i in range(100):
          scriptOP.appendPoint([i,0,0])
      return
  ```

### TOPs (Texture Operators)

Process 2D images and pixel data on the GPU—video, shaders, effects.

* **Examples**: Movie File In TOP, Composite TOP, Blur TOP, Render TOP, Script TOP.
* **Python**: Control files and parameters, query resolution, push NumPy arrays:

  ```python
  op('moviefilein1').par.file = 'video.mp4'
  width, height = op('render1').width, op('render1').height

  # Script TOP cook callback
  def cook(scriptOP):
      import numpy as np
      arr = np.zeros((512,512,3), dtype=np.uint8)
      scriptOP.copyNumpyArray(arr)
      return
  ```

### DATs (Data Operators)

Store and run text or table data—scripts, tables, network data.

* **Examples**: Table DAT, Text DAT, OSC In DAT, DAT Execute DAT, Web DAT.
* **Python**: Manipulate table cells, run scripts, read/write text:

  ```python
  tab = op('table1')
  tab[1,'Value'] = '42'
  tab.appendRow(['New','Row'])

  text = op('text1').text
  op('text1').run()
  ```

### COMPs (Components)

Containers for operator networks—UI panels, 3D objects, layouts.

* **Examples**: Base COMP, Container COMP, Geometry COMP, Camera COMP, Panel COMPs.
* **Python**: Navigate and manipulate hierarchy, create/destroy OPs:

  ```python
  comp = op('container1')
  children = comp.children
  comp.create(tdu.OPTOP, 'Constant')
  op('toDelete').destroy()
  ```

* **Extensions**: Attach classes for custom APIs on components.

### MATs (Material Operators)

Define shaders and materials for 3D geometry.

* **Examples**: Phong MAT, PBR MAT, Constant MAT, GLSL MAT.
* **Python**: Adjust shader parameters, assign to Geometry:

  ```python
  mat = op('phong1')
  mat.par.specular = 0.5
  op('geo1').par.material = op('constant1')
  ```

## Unified Workflow & OSC-API Foundation

* **Unified Access**: Every OP is a Python object reachable via `op()`, enabling dynamic creation, parameter control, network rewiring, and event handling.
* **Hybrid Model**: Combine node-based cooking with Execute DAT callbacks for responsive interactivity.
* **OSC-API Approach**: Use JSON configs for generic inputs/outputs, Python helpers for routing logic (`osc_helpers.py`), and DAT scripts for OSC I/O—realizing a central API hub for all OSC communications.

## End of README
