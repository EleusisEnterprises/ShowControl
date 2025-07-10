# DATs Directory

This folder holds all external Text DAT scripts used by **showcontrol.toe**. Each `.py` file here is loaded by a corresponding Text DAT in TouchDesigner with **“Keep in sync with external file”** enabled. Edit these files in VSCode and your changes will hot-reload in TD.

## Files

- **`osc_exec_in.py`**
  - Attached to `/project1/dat_execute_in` (DAT Execute DAT)  
  - Contains the `onTableChange(dat)` callback that reads OSC In DAT rows, extracts `address` and `value`, and calls:

    ```python
    import osc_helpers
    osc_helpers.handle_incoming(address, value)
    ```

- **`osc_in.py`**
  - Callback for `/project1/osc_in_dat` (OSC In DAT)
  - The default code prints the received OSC address and arguments to the Textport.

- **`osc_out.py`**
  - Used by `/project1/osc_out_dat` (OSC Out DAT)  
  - Defines `send_via_dat` which writes `[address, value]` rows before sending:

    ```python
    def send_via_dat(address, value):
        op('osc_out_dat').clear()
        op('osc_out_dat').appendRow([address, value])
        op('osc_out_dat').send()
    ```

## Usage

1. **Open** the `.py` file in VSCode.
2. **Edit** or extend the Python code snippet as needed.
3. **In TouchDesigner**, set the Text DAT's *File* parameter to this path and enable **Sync to File** so changes auto-reload.
4. **Save** the file—TouchDesigner will update the linked DAT.
5. **Test** in TD: trigger OSC messages or UI actions to confirm the updated callback logic is running.

---

Keep this README up to date as you add new Text DAT scripts or change their responsibilities!
