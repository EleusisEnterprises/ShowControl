# Using ONYX OSC Implementation: Addressing Logic Deep Dive

This document provides an in-depth look at Obsidian Control’s ONYX lighting software and its Open Sound Control (OSC) interface. It is structured for inclusion as Markdown context in a code repository and is intended to inform an AI coding assistant (e.g., Codex) on how OSC messages map to ONYX controls. We’ll cover enabling OSC, the OSC namespace, button and fader addressing, playback page logic, device spaces, numeric ID patterns, and programmatic generation of OSC addresses.

## 1. Introduction to ONYX and OSC

ONYX is a PC-based lighting control platform used for installations, touring shows, and broadcast environments. While it offers a rich visual interface for patching fixtures and building cue lists, it also exposes virtually all console functions via OSC over UDP, allowing external devices and software to trigger playbacks, adjust faders, navigate cue lists, and more.

## 2. Enabling and Configuring OSC in ONYX

Before sending OSC, you must enable it on the console:

1. **Access OSC Settings**  
   - Press **MENU → Network → Settings → Interfaces**.  
   - Set the **Remote** adapter to **Automatic** and **enable OSC** on that adapter.  
2. **Configure OSC Devices**  
   - Go to **Network → OSC → Devices**.  
   - Activate one of the 16 OSC device slots, name it (e.g., “iPad Remote”), and enter the remote device’s IP and **Incoming Port**.  
3. **Match Ports**  
   - Ensure your external controller’s **Target Port** equals ONYX’s **Outgoing Port**, and your external listener’s port matches ONYX’s **Incoming Port**.

Once applied, ONYX listens for UDP packets matching its OSC address schema on the specified port.

## 3. OSC Namespace and Message Structure

All OSC messages for ONYX begin with the namespace prefix:

```
/Mx
```

This prefix is followed by:

```
/Mx/<category>/<identifier>[/<subIdentifier>][/<action>]  <arguments...>
```

- **`/Mx`** – Root prefix for ONYX OSC.  
- **`<category>`** – Control type (e.g., `button`, `fader`, `playback`).  
- **`<identifier>`** – A numeric code encoding bank, type, and unit.  
- **`<subIdentifier>`** (optional) – Further refines the control (e.g., device space).  
- **`<action>`** (optional) – Specific action (e.g., `go`, `off`, `toggle`).  

Arguments follow as one or more numeric values (integers or floats).

## 4. Button Addressing Logic

Buttons (playback GO, flash, f-keys, etc.) use the **`button`** category:

```
/Mx/button/<buttonID> <value>
```

- **`<buttonID>`** – A four-digit code:  
  - **P** (prefix): `4` for buttons  
  - **T** (type): `2` for main playbacks, other codes for flash or f-keys  
  - **UU** (unit): playback index (01–10 for playbacks 1–10)  
- **`<value>`** – `1` (press/on) or `0` (release/off)  

### Example: Playback 1 GO on Bank 1

```
/Mx/button/4201 1
```

This sends a GO command to Playback 1 on Bank 1.

#### Extended Button Clusters

ONYX groups extra playbacks or f-keys in batches using adjacent numeric ranges. For example, button indexes 0–63 map to these addresses, incrementing predictably across pages and banks.

## 5. Fader Addressing Logic

Faders (playback levels, grand master, FX sliders) use the **`fader`** category:

```
/Mx/fader/<faderID> <value>
```

- **`<faderID>`** – Four-digit code:  
  - **P**: `2` for faders  
  - **T**: `1` for main faders, `2` for grand master, etc.  
  - **UU**: unit index (01–10 for playback faders 1–10)  
- **`<value>`** – Normalized float (0.0–1.0) or integer (0–255)  

### Main Playback Fader Example

```
/Mx/fader/2101 0.75
```

Sets Playback 1’s fader to 75%.

### Grand Master Example

```
/Mx/fader/2202 0
```

Drops the grand master to zero (full blackout).

#### Extended Fader Ranges

Some surfaces map faders 11–20 to MIDI codes and convert these to `/Mx/fader/21NN` addresses, following the same prefix logic.

## 6. Playback Page Commands and Device Spaces

Higher-level page controls use:

```
/Mx/playback/page<bank>/<controlID>/<action>
```

- **`<bank>`** – Bank number (1–500)  
- **`<controlID>`** – Internal index for the control within that bank  
- **`<action>`** – Actions: `go`, `off`, `toggle`, `flash`  

### Example: Trigger GO via Page Command

```
/Mx/playback/page1/63/go
```

#### Device Spaces

ONYX can sync multiple OSC devices using **Device Space IDs** (0–15), allowing split-bank setups. Activate the matching slot in ONYX’s OSC Devices table.

## 7. Numeric ID Patterns and Generation

4-digit OSC IDs follow a **`PTUU`** pattern:

```
P    T    UU
```

- **P** = Prefix digit (2 for faders, 4 for buttons)  
- **T** = Type code (e.g., 1 for main, 2 for grand master)  
- **UU** = Unit index (01–10 for first ten)  

This schema lets you compute any button or fader address algorithmically.

## 8. Programmatic Address Generation

def onyx_button_address(playback: int, bank: int=1) -> str:
    if not 1 <= playback <= 10:
        raise ValueError("Playback must be 1–10")
    return f"/Mx/button/42{playback:02d}"

def onyx_fader_address(fader: int, grand_master: bool=False) -> str:
    if grand_master:
        return "/Mx/fader/2202"
    if not 1 <= fader <= 10:
        raise ValueError("Fader must be 1–10")
    return f"/Mx/fader/21{fader:02d}"

## 9. Best Practices for Pattern Implementation

- **Centralize Address Logic:** Keep prefixes and patterns in one module.  
- **Use Constants:** Define `BUTTON_PREFIX`, `FADER_PREFIX`, etc.  
- **Validate Ranges:** Check unit indices against supported ranges.  
- **Document Device Spaces:** Map Device Space IDs to banks/surfaces.  
- **Test with an OSC Monitor:** Verify generated messages before live use.

## 10. Integrating with Repositories and AI Agents

1. **Externalize Code:** Store address-gen functions in `onyx_osc.py`.  
2. **Include README:** Describe the OSC schema and examples in Markdown.  
3. **Sync Config Files:** Keep JSON/YAML endpoint mappings in the repo.  
4. **Annotate Examples:** Comment how `/Mx/button/4201` maps to Playback 1 GO.

By maintaining structured code and clear documentation, your AI assistant will have full context to automate ONYX control patterns reliably.
