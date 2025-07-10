# DATs Directory

This folder holds all external Text DAT scripts used by **showcontrol.toe**. Each `.txt` file here is loaded by a corresponding Text DAT in TouchDesigner with **“Keep in sync with external file”** enabled. Edit these files in VSCode and your changes will hot-reload in TD.

## Files

- **`dat_execute_in.txt`**  
  - Attached to `/project1/dat_execute_in` (DAT Execute DAT)  
  - Contains the `onTableChange(dat)` callback that reads OSC In DAT rows, extracts `address` and `value`, and calls:
    ```python
    import osc_helpers
    osc_helpers.handle_incoming(address, value)
    ```

- **`osc_in_dat.txt`** *(optional template)*  
  - Can be used to document or pre-populate settings for `/project1/osc_in_dat` (OSC In DAT)  
  - Example content might include comments on port number, address filters, etc.

- **`osc_out_dat.txt`**  
  - Used by `/project1/osc_out_dat` (OSC Out DAT)  
  - Defines a helper snippet that writes `[address, value]` rows before sending, for example:
    ```python
    def send_via_dat(address, value):
        op('osc_out_dat').clear()
        op('osc_out_dat').appendRow([address, value])
        op('osc_out_dat').send()
    ```

## Usage

1. **Open** the `.txt` file in VSCode.  
2. **Edit** or extend the Python code snippet as needed.  
3. **Save**—TouchDesigner will auto-update the linked Text DAT.  
4. **Test** in TD: trigger OSC messages or UI actions to confirm the updated callback logic is running.

---

Keep this README up to date as you add new Text DAT scripts or change their responsibilities!
