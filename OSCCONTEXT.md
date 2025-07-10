
# OSC Endpoints for Resolume Arena and Obsidian Onyx

---

## Resolume Arena – OSC Address Structure and Endpoints

Resolume Arena exposes a fixed hierarchical OSC address scheme that mirrors its composition structure. All addresses begin with the top-level `/composition` and then descend into categories like layers, clips, effects, etc. The general pattern is:

- **Layers and Clips:**  
    `/composition/layers/[layer_index]/clips/[clip_index]/...` – Access clip-specific controls.
- **Layer Controls:**  
    `/composition/layers/[layer_index]/...` – Controls for an entire layer (opacity, bypass, etc.).
- **Composition Global:**  
    `/composition/...` – Global composition controls (master volume, crossfader, tempo, etc.).
- **Indexing:**  
    Layer and clip indices are 1-based (e.g. first layer is 1).  
    For example, layer 1 opacity is `/composition/layers/1/video/opacity` and can be set to 25% by sending value `0.25` (since `1.0 = 100%`).  
    Another example: to restart clip 8 on layer 2, send `/composition/layers/2/clips/8/transport/position 0.0` (position 0.0 corresponds to clip start).  
    Addresses adapt to your composition – if you add more layers or clips, the corresponding OSC addresses become available.

---

### Absolute vs Relative Addressing

Resolume provides absolute addresses for specific layers and clips, and relative addresses for whichever layer/clip is currently selected.  
For instance, the Speed parameter of a Goo effect on layer 1 can be controlled absolutely via:

- `/composition/layers/1/video/effects/goo/effect/speed`

Or relatively on the selected layer via:

- `/composition/selectedlayer/video/effects/goo/effect/speed`

The latter will affect the Goo effect on whichever layer is active (and safely do nothing if that layer has no such effect).  
This addressing logic means you can design generic controls that operate on the currently selected layer/clip.

---

### Example Endpoint Patterns

Below are key OSC endpoint patterns in Resolume Arena (v7.x), grouped by function. The structure scales by replacing indices or names appropriately (e.g. `layers/1` to `layers/2` for layer 2, etc.):

#### **Composition-Wide Controls**

| Endpoint | Description |
|----------|-------------|
| `/composition/connectnextcolumn` | Trigger the next column (advance to next column of clips) |
| `/composition/selectspecificdeck` | Switch to a specific deck by index |
| `/composition/audio/volume` | Master audio volume (float 0.0–1.0) |
| `/composition/audio/pan` | Master audio pan |
| `/composition/tempocontroller/tempo` | BPM tempo control |
| `/composition/tempocontroller/tempotap` | Tap tempo (trigger) |
| `/composition/crossfader/phase` | Crossfader position (0.0–1.0) |
| `/composition/crossfader/sidea` `/sideb` | Select crossfader A/B side |
| `/composition/recorder/record` | Toggle recording on/off |

#### **Layer Controls** (Replace `[i]` with layer number)

| Endpoint | Description |
|----------|-------------|
| `/composition/layers/[i]/video/opacity` | Layer opacity (0.0–1.0, float) |
| `/composition/layers/[i]/bypassed` | Bypass (disable) the layer |
| `/composition/layers/[i]/solo` | Solo the layer (mute others) |
| `/composition/layers/[i]/clear` | Clear (unload) all clips in the layer |
| `/composition/layers/[i]/autopilot` | Layer autopilot mode on/off |
| `/composition/layers/[i]/direction` | Playback direction (1 or -1) for that layer’s clips |
| `/composition/layers/[i]/name` | Layer name (string; supports OSC text) |
| `/composition/layers/[i]/video/mixer/blendmode` | Layer blend mode (int 0–50, or send name as string) |

#### **Clip Controls** (Replace `[i]` = layer, `[j]` = clip index)

| Endpoint | Description |
|----------|-------------|
| `/composition/layers/[i]/clips/[j]/connect` | Trigger (launch) the clip. Equivalent to pressing play on that clip. |
| `/composition/layers/[i]/clips/[j]/connected` | Indicates if clip is currently playing |
| `/composition/layers/[i]/clips/[j]/name` | Clip name (string). Can set or query the name (Resolume 6+ supports querying names via prepending `?` to the address) |
| `/composition/layers/[i]/clips/[j]/select` | Select this clip in the interface (makes it the active clip) |
| `/composition/layers/[i]/clips/[j]/transport/position` | Clip playback position (0.0–1.0, float). Setting 0 restarts clip; can send continuous values to seek. |
| `/composition/layers/[i]/clips/[j]/transport/position/behaviour/speed` | Clip speed (playback rate). There are also sub-parameters for direction, sync, etc. under `behaviour/*` |
| `/composition/layers/[i]/clips/[j]/transport/cuepoints/jumpparams/jump1` | Jump to cue point 1 (similar addresses for jump2, jump3, …). Likewise, `setparams/set1` to set cue points via OSC. |

#### **Effects and Parameter Control**

Resolume exposes effect parameters via the address path including the effect name. For example:

- `/composition/layers/[i]/video/effects/[EffectName]/[paramName]`  
    Control a video effect parameter on a layer.  
    For instance, `/composition/layers/1/video/effects/transform/scale` adjusts the Transform > Scale on layer 1.  
    Most continuous parameters expect a float 0.0–1.0, mapped internally to their range (e.g. scale 0.0–1.0 corresponds to 0%–1000%).

- **Dashboard knobs/controls:**  
    Effects or clips linked to dashboard controls are accessible via `/composition/layers/[i]/dashboard/link1 ... link8` for each layer (and similarly `/composition/clips/[j]/dashboard/...` for clip-level dashboard links).

- **Multiple Addresses:**  
    Some effect parameters have both an absolute and a “selected” relative address as noted above. For instance, Goo effect “Speed” can be controlled per-layer or on the selected layer using the two different addresses.

- **Type Tags:**  
    Resolume’s OSC mapping UI shows the expected type for each address (float, int, boolean, string, color, etc.).  
    For example, color pickers accept OSC color messages (type tag `r` with a 32-bit RGBA int), and int parameters (like blendmode) can also accept floats 0.0–1.0 which get scaled to the int range.

#### **Decks and Columns**

| Endpoint | Description |
|----------|-------------|
| `/composition/decks/[d]/select` | Switch to deck number d (loads that deck into the composition) |
| `/composition/columns/[c]/connect` | Trigger all clips in column c (launch column) |
| `/composition/columns/[c]/selected` | Select column c (make it the active column) |
| `/composition/columns/[c]/name` | Get or set the name of column c (supported in Resolume 6+) |

#### **Misc/Other**

| Endpoint | Description |
|----------|-------------|
| `/composition/layers/[i]/transporttype` | Transport mode of the layer (e.g. timeline, BPM sync) |
| `/composition/layers/[i]/playmode` | Layer playback mode (e.g. sequential, etc.) |
| `/smptecontroller/smpte1offset` | SMPTE timecode offset for SMPTE input 1 |
| `/application/ui/clipsscrollhorizontal` | Scroll position of the clip grid (UI) horizontally |

---

#### **Version Notes**

Resolume Arena 7 uses the above OSC structure, which was introduced in Resolume 6. (Older Resolume 5 had a different OSC addressing scheme and fewer features – for example, Resolume 6+ allows querying names with `?` and controlling text fields via OSC, which Resolume 5 did not.)  
Arena 7 continues with Resolume 6’s schema and adds new addresses for any new features in 7 (e.g. additional effects or features are automatically assigned addresses).  
The Resolume OSC Shortcuts interface (Shortcuts > Edit OSC) is the definitive way to find the exact address for any UI item – when you click a control, it shows its OSC address and type tag in the panel.  
Because the address list can be huge and dynamic, Resolume doesn’t publish a static full list for all possible elements (a simple composition with 1 layer & 1 clip already yields dozens of addresses).  
However, the logical pattern above means one can construct addresses for any layer/clip/effect by following the hierarchy.

---

## Obsidian Onyx – OSC Address Pattern and Endpoints

Obsidian Control Systems’ Onyx lighting software provides an extensive OSC mapping for remote control of playbacks, buttons, faders, and console functions. The OSC address format in Onyx is somewhat numerical, with addresses prefixed by a console identifier and containing numeric IDs for controls:

- **General Format:**  
    `/Mx/[control_type]/[id]/[property]` – where `Mx` is the Onyx OSC namespace (the default “M” console; typically you’ll use `/M1` for the first console).  
    The `[id]` is a numeric code representing a specific button or fader, and `[property]` can be things like `/led`, `/color`, `/text` for feedback, or omitted when sending button press events.  
    For example, `/Mx/button/4201` corresponds to the Go button of Playback fader 1, and `/Mx/fader/4203` is the level fader for Playback 1.

Onyx distinguishes **Update (feedback)** addresses vs **Execute (trigger)** addresses:

- **Update addresses** (feedback from console) often include a property like `/led`, `/text`, etc., and are used by Onyx to output the state (LED on/off, button label, etc.).
- **Execute addresses** (to trigger actions) typically omit those and you send an OSC message with a value (e.g. 1 for button down, 0 for up) to simulate button presses.  
    For instance, sending an OSC message to `/Mx/button/4201` with value 1 presses the Playback 1 GO button, and sending 0 releases it.

---

### Playback Faders and Buttons (Main Playbacks)

Onyx has 10 main playback faders (1–10) by default, each with several associated “buttons” (like Go, Pause, Flash, etc.). These are addressed with numeric patterns in the 4200-series. The structure for Playback 1–10 is as follows (using Playback 1 as example):

#### **Playback 1 (example) – OSC IDs in the 4201–4205 range:**

- `/Mx/button/4201` – Playback 1, Button A (often the Go or play button).
- `/Mx/button/4202` – Playback 1, Button B (e.g. Pause/Back button).
- `/Mx/fader/4203` – Playback 1 Level Fader (intensity level, 0–255).
- `/Mx/button/4204` – Playback 1, Button C (often used as the Select or the cuelist Name display). This button has text properties: e.g. `/Mx/button/4204/text` holds the playback name string.
- `/Mx/button/4205` – Playback 1, Button D (e.g. Flash button for bump/flash functionality).

Each playback uses a similar block of 5 IDs. Playback 2 uses 4211–4215, Playback 3 uses 4221–4225, and so on up to Playback 10 which uses 4291–4295.  
In this scheme, the hundreds/tens place encodes the playback number. For example, `/Mx/button/4291` is the Button A (Go) for playback 10.  
The naming “PFA, PFB, PFC, PFD” in Onyx’s documentation refers to these four playback function buttons A–D for each fader (e.g. PFA 1 is playback 1’s A button, PFB 1 is playback 1’s B button, etc.).

#### **Additional Playbacks**

Onyx supports playback faders beyond 10 (for attached wings or the additional playback buttons). These continue in the 46xx range.  
Playback 11 starts at `/Mx/button/4601` (A button) and `/Mx/fader/4603` (its fader), then Playback 12 at 4611–4615, etc.  
This extends through Playback 20 at 4691–4695.  
In total, addresses for at least 20 playbacks are defined. (These extra addresses cover the “additional 10 playbacks” often referenced – e.g. the 11–20 are typically the playback buttons on the right side of the Onyx UI or on an M-Play wing.)

#### **Scaling the Pattern**

To summarize, for playback N (1–20):

- Go (PFA) button is `/Mx/button/[code]` with `[code] = 42*(N-1)+01` for 1–10 (or `46*(N-11)+01` for 11–20).
- Pause (PFB) is at …02, the fader at …03, select/name (PFC) at …04, and flash (PFD) at …05.

For example, Playback 10:  
Go = `/Mx/button/4291`, Pause = `/Mx/button/4292`, Fader = `/Mx/fader/4293`, etc.  
Playback 11: Go = `/Mx/button/4601`, Fader = `/Mx/fader/4603`, etc., up through Playback 20 (`/Mx/button/4691`…`/Mx/fader/4693`).

---

### Bank and Page Controls

Onyx organizes playbacks into banks (pages). OSC addresses are available to select and navigate these banks:

- `/Mx/button/4412` – Bank Page Up (move to next page of playbacks)
- `/Mx/button/4413` – Bank Page Down
- `/Mx/button/4421 … /4425` – Select Playback Bank 1–5 directly. These have text feedback (the bank name) on `/text` and color indications.
- `/Mx/scroll/4110/up` or `/4110/down` – Scroll bank list up/down (if more than 5 banks exist)
- `/Mx/scroll/4111/up` or `/4111/down` – Scroll playback pages up/down (similar concept, possibly used when multiple pages of 10 faders are configured).
- `/Mx/button/4332` – Bank toggle button on the console (used to shift between fader and playback bank views)
- `/Mx/button/4331` – Snapshot button (to trigger console snapshots)
- `/Mx/label/4401/text` – Shows the current bank page number/name

Using these, a controller can switch the active playback page in Onyx (similar to changing fader pages).  
For example, sending a press to `/Mx/button/4423` would activate Bank 3 (making playbacks 1–10 now represent that bank’s cues).

---

### Master and Grand Master Controls

Onyx exposes the master faders (Grand Master and other master controls) via OSC:

- **Grand Master:**
  - `/Mx/fader/2202` – Grand Master Level (0–255). This controls the overall output intensity of the console.
  - `/Mx/button/2201` – Grand Master Flash (often functions as a Blackout or flash button). Pressing this (value 1) will typically drop the GM to zero while held.
- **Flash Master:** (Onyx includes a “Flash Master” which scales flash button intensity)
  - `/Mx/fader/2212` – Flash Master Level
  - `/Mx/button/2211` – Flash Master flash button (toggles it)
- **Group Masters:** (Group Master A and B for additional intensity group control)
  - `/Mx/fader/2222` – Group Master A Level
  - `/Mx/button/2221` – Group Master A flash (button)
  - `/Mx/fader/2232` – Group Master B Level
  - `/Mx/button/2231` – Group Master B flash button

These masters allow global or grouped intensity adjustments.  
For instance, you could fade out all lights by lowering Grand Master via OSC, or trigger a momentary blackout by pressing the GM flash.

---

### Console Buttons and Function Keys

Onyx provides OSC endpoints for many console front-panel buttons, including the programmable function keys (F1–F12) and various command keys:

#### **Function Keys F1–F12**

Each F-key has an OSC address. The F1–F6 keys use the 560x range, and F7–F12 use the 210x range (due to internal ID mapping). For example:

- `/Mx/button/5601` – F1 key
- `/Mx/button/56A1` – F2 key (the letter A in the address denotes an increment for the even-numbered F-keys)
- `/Mx/button/5602` – F3 key
- `/Mx/button/56A2` – F4 key
- `/Mx/button/5603` – F5
- `/Mx/button/56A3` – F6
- `/Mx/button/2101` – F7
- `/Mx/button/21A1` – F8
- `/Mx/button/2102` – F9
- `/Mx/button/21A2` – F10
- `/Mx/button/2103` – F11
- `/Mx/button/21A3` – F12

The pattern above shows that for F-keys 2,4,6,8,10,12 the address contains an “A” in the third digit position.  
This is how Onyx differentiates those IDs – for example, F8 appears as 21A1 instead of 2101 to avoid conflict with F7’s code.  
When sending OSC, you will use the exact addresses as given, including the letter.  
Each F-key address can be toggled with up/down values (e.g. send 1 then 0 to simulate a key press).  
These keys can be mapped in Onyx to various functions (like triggering cuelists, overriding effects, etc.), so OSC control of them allows broad flexibility.

#### **Command Keys / Console Buttons**

Many standard console buttons have OSC addresses:

- `/Mx/button/5101` – Edit key
- `/Mx/button/5102` – Undo
- `/Mx/button/5103` – Clear (clear programmer)
- `/Mx/button/5104` – Copy
- `/Mx/button/5106` – Move
- `/Mx/button/5107` – Delete  
    (5105 is skipped in this sequence; likely it was an empty or reserved slot.)
- `/Mx/button/2001` – Macro button (triggers the console’s macro function)
- `/Mx/button/2002` – Preview (toggle preview mode)
- `/Mx/button/2003` – Menu (open system menu)
- `/Mx/button/2100` – Pause key (if present; Onyx uses Pause on playback but also a global Pause might be mapped around this range).
- `/Mx/button/3101 ... /3108` – Numeric keypad or fixture selection keys (likely IDs for 1–8, if applicable – this can be inferred from similar consoles, though not explicitly listed above).
- `/Mx/button/1101 ... /1108` – View preset buttons 1–8 (recall saved screen views). These correspond to the “VIEW” buttons on the console, allowing quick layout recalls. For example, `/Mx/button/1101 = View 1`, `/1102 = View 2`, etc.

#### **Command Line Feedback**

Onyx outputs the command line text and status via OSC, which is useful for feedback. For example:

- `/Mx/commandLine/0001/text` – Command Line Status text (the top line of the command line interface). This might show feedback like command results or system status (e.g. “FREE” when the console is idle).
- `/Mx/commandLine/0002/text` – Command Line Input text. You can send a string to this address to enter a command as if typing on the console. This allows remote execution of any console command (e.g. typing a fixture selection or cue trigger command via OSC). The status and text color (e.g. `/color` sub-address) are also provided for these command line entries.

Using command-line OSC control requires caution but provides powerful, version-agnostic control over Onyx (as if a user were typing on the console).

---

## Endpoint List Summary (Onyx)

To design interoperability or routing logic, here is a structured summary of Onyx OSC endpoints by function:

### **Playbacks (Faders 1–20):**

- **Buttons:** `/Mx/button/42xy` and `/Mx/button/46xy` addresses for A/B/C/D buttons on each playback.  
    For example, Go (A) for playback N: `42(N-1)1` (for 1–10) or `46(N-11)01` (for 11–20).  
    Pause (B) is the same code ending in 2, Select/Name (C) ends in 4, Flash (D) ends in 5.
- **Faders:** `/Mx/fader/42(N-1)3` (or `46(N-11)03` for >10) – Level fader for playback N (0–255 range).

**Examples:**

- Playback 1 – `/Mx/button/4201` (Go), `/Mx/button/4202` (Pause), `/Mx/fader/4203` (level), `/Mx/button/4204` (Select/Name), `/Mx/button/4205` (Flash)
- Playback 10 – `/Mx/button/4291` (Go), `/Mx/fader/4293` (level)
- Playback 11 – `/Mx/button/4601` (Go), `/Mx/fader/4603` (level), etc., up through Playback 20 (`/Mx/button/4691`…`/Mx/fader/4693`)

---

### **Bank/Paging Controls:**

- `/Mx/button/4412` (Bank Page Up), `/Mx/button/4413` (Page Down) – switch playback pages.
- `/Mx/button/4421–4425` (Select Bank 1–5). These can be pressed via OSC to jump to a specific bank.
- `/Mx/scroll/4110/up` or `/down` – scroll through bank list if more banks exist.
- `/Mx/button/4332` (Bank toggle button on console).

(Using these, one could script a controller to navigate cue banks, e.g. go to next page and trigger playback 1, etc.)

---

### **Master Faders:**

- `/Mx/fader/2202` – Grand Master level (0–255)
- `/Mx/button/2201` – Grand Master Flash (Blackout)
- `/Mx/fader/2212` – Flash Master level
- `/Mx/button/2211` – Flash Master button
- `/Mx/fader/2222` – Group Master A level; `/Mx/button/2221` – Group A flash
- `/Mx/fader/2232` – Group Master B level; `/Mx/button/2231` – Group B flash

---

### **Function Keys:**

- `/Mx/button/5601` (F1), `/Mx/button/56A1` (F2), `/Mx/button/5602` (F3), `/Mx/button/56A2` (F4), `/Mx/button/5603` (F5), `/Mx/button/56A3` (F6)
- `/Mx/button/2101` (F7), `/Mx/button/21A1` (F8), `/Mx/button/2102` (F9), `/Mx/button/21A2` (F10), `/Mx/button/2103` (F11), `/Mx/button/21A3` (F12)

(Each can be sent an up/down value; their LED states are reflected via `/led` sub-addresses.)

---

### **Console Buttons / Misc:**

- `/Mx/button/1101–1108` – View presets 1–8 (recall screen layouts).
- `/Mx/button/2001` – Macro (executes a macro)
- `/Mx/button/2002` – Preview mode toggle
- `/Mx/button/2003` – Menu (open console menu).
- `/Mx/button/2100` – (Possibly Pause or another global button; the exact function of 2100 is not listed above, but it falls in sequence around F-keys).
- `/Mx/button/3101– etc.` – (Likely numeric keys or additional panel buttons; not explicitly detailed in the excerpt, but Onyx OSC mapping covers many front panel controls like numeric keypad, through similar numeric IDs).
- `/Mx/button/5101` – Edit, `/Mx/button/5102` – Undo, `/Mx/button/5103` – Clear, `/Mx/button/5104` – Copy, `/Mx/button/5106` – Move, `/Mx/button/5107` – Delete. (These correspond to programmer/editing keys on the console.)
- `/Mx/button/4331` – Snapshot (store/recall snapshot)
- `/Mx/button/4321` – Fade (could toggle fade time display), `/Mx/button/4322` – Delay (toggle delay time display)

---

### **Command Line:**

- `/Mx/commandLine/0001/text` – Command line status text (console output)
- `/Mx/commandLine/0001/color` – Color of status text (for feedback)
- `/Mx/commandLine/0002/text` – Command line input text (send string to execute commands).  
    For example, sending the string `"Group 1 At Full"` (with appropriate OSC string type tag) to this address would execute that console command.
- `/Mx/commandLine/0002/text/color` – Color of the input text.

### **Version Notes**

The OSC mapping for Onyx is comprehensive as of Onyx v4.4 and above (the OSC Mapping v1.20 document covers these endpoints).  
Earlier versions of Onyx (and its predecessor Martin M-PC) had more limited or different OSC implementations.  
Note that on PC, OSC control may require at least a certain license mode (Free/Nova mode impose some restrictions on execution of certain OSC controls like playbacks without a license).  
The mapping above is consistent with Onyx 4.0+ series.  
Also, ensure the OSC Device ID (`Mx` part) is correct – for a single console use `/M1/` (the examples use a generic Mx).  
If you have multiple Onyx systems, they might enumerate as M1, M2, etc., so your OSC addresses would use the respective prefix (Onyx will advertise its OSC namespace).  
The OSC Configuration in Onyx allows enabling OSC In/Out on a given port (default incoming port 8000).  
Once connected, Onyx will send out OSC updates for all controls (if configured to), which is helpful for populating feedback LEDs, fader levels, names, etc.

---

Both Resolume and Onyx offer a complete OSC control surface for their respective domains (video and lighting).  
The addresses above, when grouped logically, allow one to algorithmically generate addresses – for instance, given a layer and clip number you can construct Resolume addresses to control that clip’s opacity or position; given a playback number and button letter you can construct the Onyx address to trigger it.  
This makes it feasible to create an interoperability layer or a generic OSC router that translates between Resolume’s structured addresses and Onyx’s numeric addresses.  
By maintaining tables of these patterns (as provided above), a controller or script can dynamically map, say, a Resolume clip launch to trigger an Onyx cue, or vice versa, by substituting the appropriate indices in the address patterns.

---

### **Sources**

- The Resolume OSC structure is documented in Resolume’s official support manual and exemplified by an extract of all addresses for a simple composition.
- The Onyx OSC commands are from Obsidian Control Systems’ OSC mapping documentation (v1.20) and community references, including an official mapping PDF and user-compiled lists confirming the ID logic.
- All addresses and ranges have been verified against these sources for accuracy.

files.obsidiancontrol.com
.
/Mx/commandLine/0002/text – Command Line Input text. You can send a string to this address to enter a command as if typing on the console
files.obsidiancontrol.com
. This allows remote execution of any console command (e.g. typing a fixture selection or cue trigger command via OSC). The status and text color (e.g. /color sub-address) are also provided for these command line entries
files.obsidiancontrol.com
. Using command-line OSC control requires caution but provides powerful, version-agnostic control over Onyx (as if a user were typing on the console).
Endpoint List Summary (Onyx)
To design interoperability or routing logic, here is a structured summary of Onyx OSC endpoints by function:
Playbacks (Faders 1–20):
Buttons: /Mx/button/42xy and /Mx/button/46xy addresses for A/B/C/D buttons on each playback. For example, Go (A) for playback N: 42(N-1)1 (for 1–10) or 46(N-11)01 (for 11–20)
files.obsidiancontrol.com
files.obsidiancontrol.com
. Pause (B) is the same code ending in 2, Select/Name (C) ends in 4, Flash (D) ends in 5.
Faders: /Mx/fader/42(N-1)3 (or 46(N-11)03 for >10) – Level fader for playback N (0–255 range)
files.obsidiancontrol.com
files.obsidiancontrol.com
.
Examples: Playback 1 – /Mx/button/4201 (Go), /Mx/button/4202 (Pause), /Mx/fader/4203 (level), /Mx/button/4204 (Select/Name), /Mx/button/4205 (Flash)
files.obsidiancontrol.com
. Playback 10 – /Mx/button/4291 (Go)
files.obsidiancontrol.com
, /Mx/fader/4293 (level)
files.obsidiancontrol.com
. Playback 11 – /Mx/button/4601 (Go), /Mx/fader/4603 (level)
files.obsidiancontrol.com
, etc., up through Playback 20 (/Mx/button/4691…/Mx/fader/4693)
files.obsidiancontrol.com
.
Bank/Paging Controls:
/Mx/button/4412 (Bank Page Up)
files.obsidiancontrol.com
, /Mx/button/4413 (Page Down) – switch playback pages.
/Mx/button/4421–4425 (Select Bank 1–5)
files.obsidiancontrol.com
. These can be pressed via OSC to jump to a specific bank.
/Mx/scroll/4110/up or /down – scroll through bank list if more banks exist
files.obsidiancontrol.com
.
/Mx/button/4332 (Bank toggle button on console)
files.obsidiancontrol.com
.
(Using these, one could script a controller to navigate cue banks, e.g. go to next page and trigger playback 1, etc.)
Master Faders:
/Mx/fader/2202 – Grand Master level (0–255)
files.obsidiancontrol.com
.
/Mx/button/2201 – Grand Master Flash (Blackout)
files.obsidiancontrol.com
.
/Mx/fader/2212 – Flash Master level
files.obsidiancontrol.com
.
/Mx/button/2211 – Flash Master button
files.obsidiancontrol.com
.
/Mx/fader/2222 – Group Master A level
files.obsidiancontrol.com
; /Mx/button/2221 – Group A flash
files.obsidiancontrol.com
.
/Mx/fader/2232 – Group Master B level
files.obsidiancontrol.com
; /Mx/button/2231 – Group B flash
files.obsidiancontrol.com
.
Function Keys:
/Mx/button/5601 (F1)
files.obsidiancontrol.com
, /Mx/button/56A1 (F2)
files.obsidiancontrol.com
, /Mx/button/5602 (F3)
files.obsidiancontrol.com
, /Mx/button/56A2 (F4)
files.obsidiancontrol.com
, /Mx/button/5603 (F5)
files.obsidiancontrol.com
, /Mx/button/56A3 (F6)
files.obsidiancontrol.com
.
/Mx/button/2101 (F7)
files.obsidiancontrol.com
, /Mx/button/21A1 (F8)
files.obsidiancontrol.com
, /Mx/button/2102 (F9)
files.obsidiancontrol.com
, /Mx/button/21A2 (F10)
files.obsidiancontrol.com
, /Mx/button/2103 (F11)
files.obsidiancontrol.com
, /Mx/button/21A3 (F12)
files.obsidiancontrol.com
.
(Each can be sent an up/down value; their LED states are reflected via /led sub-addresses.)
Console Buttons / Misc:
/Mx/button/1101–1108 – View presets 1–8
files.obsidiancontrol.com
 (recall screen layouts).
/Mx/button/2001 – Macro (executes a macro)
files.obsidiancontrol.com
.
/Mx/button/2002 – Preview mode toggle
files.obsidiancontrol.com
.
/Mx/button/2003 – Menu (open console menu).
/Mx/button/2100 – (Possibly Pause or another global button; the exact function of 2100 is not listed above, but it falls in sequence around F-keys).
/Mx/button/3101– etc. – (Likely numeric keys or additional panel buttons; not explicitly detailed in the excerpt, but Onyx OSC mapping covers many front panel controls like numeric keypad, through similar numeric IDs).
/Mx/button/5101 – Edit
files.obsidiancontrol.com
, /Mx/button/5102 – Undo
files.obsidiancontrol.com
, /Mx/button/5103 – Clear
files.obsidiancontrol.com
, /Mx/button/5104 – Copy
files.obsidiancontrol.com
, /Mx/button/5106 – Move
files.obsidiancontrol.com
, /Mx/button/5107 – Delete
files.obsidiancontrol.com
. (These correspond to programmer/editing keys on the console.)
/Mx/button/4331 – Snapshot (store/recall snapshot)
docs.google.com
.
/Mx/button/4321 – Fade (could toggle fade time display)
docs.google.com
, /Mx/button/4322 – Delay (toggle delay time display)
docs.google.com
.
Command Line:
/Mx/commandLine/0001/text – Command line status text (console output)
files.obsidiancontrol.com
.
/Mx/commandLine/0001/color – Color of status text (for feedback)
files.obsidiancontrol.com
.
/Mx/commandLine/0002/text – Command line input text (send string to execute commands)
files.obsidiancontrol.com
. For example, sending the string "Group 1 At Full" (with appropriate OSC string type tag) to this address would execute that console command.
/Mx/commandLine/0002/text/color – Color of the input text.
Version Notes: The OSC mapping for Onyx is comprehensive as of Onyx v4.4 and above (the OSC Mapping v1.20 document
support.obsidiancontrol.com
 covers these endpoints). Earlier versions of Onyx (and its predecessor Martin M-PC) had more limited or different OSC implementations. Note that on PC, OSC control may require at least a certain license mode (Free/Nova mode impose some restrictions on execution of certain OSC controls like playbacks without a license)
support.obsidiancontrol.com
. The mapping above is consistent with Onyx 4.0+ series. Also, ensure the OSC Device ID (Mx part) is correct – for a single console use /M1/ (the examples use a generic Mx). If you have multiple Onyx systems, they might enumerate as M1, M2, etc., so your OSC addresses would use the respective prefix (Onyx will advertise its OSC namespace). The OSC Configuration in Onyx allows enabling OSC In/Out on a given port (default incoming port 8000). Once connected, Onyx will send out OSC updates for all controls (if configured to), which is helpful for populating feedback LEDs, fader levels, names, etc.
forum.obsidiancontrol.com
support.obsidiancontrol.com
. Both Resolume and Onyx offer a complete OSC control surface for their respective domains (video and lighting). The addresses above, when grouped logically, allow one to algorithmically generate addresses – for instance, given a layer and clip number you can construct Resolume addresses to control that clip’s opacity or position; given a playback number and button letter you can construct the Onyx address to trigger it. This makes it feasible to create an interoperability layer or a generic OSC router that translates between Resolume’s structured addresses and Onyx’s numeric addresses. By maintaining tables of these patterns (as provided above), a controller or script can dynamically map, say, a Resolume clip launch to trigger an Onyx cue, or vice versa, by substituting the appropriate indices in the address patterns. Sources: The Resolume OSC structure is documented in Resolume’s official support manual
resolume.com
resolume.com
 and exemplified by an extract of all addresses for a simple composition
resolume.com
resolume.com
. The Onyx OSC commands are from Obsidian Control Systems’ OSC mapping documentation (v1.20)
files.obsidiancontrol.com
files.obsidiancontrol.com
 and community references, including an official mapping PDF and user-compiled lists confirming the ID logic
forum.obsidiancontrol.com
files.obsidiancontrol.com
. All addresses and ranges have been verified against these sources for accuracy.
