# 🎛️ ShowControl: Modular, Code-Driven, Cross-Platform Live Control Hub

---

## 🚀 Purpose & Vision

ShowControl is an open, code-first, modular show control system built on TouchDesigner but designed for **collaborative, team-based development in VS Code**. It serves as the signal hub for:

- **Lighting consoles** (Onyx, grandMA, etc.)
- **Media servers** (Resolume, VJ software)
- **Laser controllers** (Pangolin QuickShow, Beyond)
- **MIDI devices** (Launchpad, Akai, DIY gear)
- **Any OSC/MIDI/DMX/NDI-capable device**

**The goal:**  
To allow *live, flexible routing* of control signals between any combination of these devices and applications, using a single point of configuration, mapping, and management.

---

## 🧬 Core Philosophy

- **Everything that can be coded, should be coded.**  
  Logic, mappings, device definitions, and signal normalization all live in Python DATs and JSON config files. TouchDesigner is the execution host, but the "real work" is done in versioned source.

- **Device COMPs are microservices.**  
  Each platform (Onyx, Resolume, MIDI) gets its own self-contained COMP with Python DATs for handling input, output, pattern-matching, and data normalization.

- **Routing is operator-centric and UI-driven.**  
  The `project1` COMP provides a UI matrix for assigning and re-assigning control paths at runtime—no need to rewire TouchDesigner, just change the routing in the UI.

- **Incoming and outgoing control are first-class citizens.**  
  Any device can both control and be controlled. The system is not just "TD → other," but also "other → TD → anything else."

---

## 🏗️ High-Level Architecture

### 1. `project1` COMP: The Routing Hub

- **Inputs:** Receives *already-normalized* (named, 0-1 ranged) control signals from all device COMPs.
- **UI:** Lets operators assign these signals to destination parameters on any output device or software.
- **Outputs:** Dispatches control signals to device COMPs, tagged with their destination, for protocol-specific formatting and delivery.
- **MIDI OUT support:** Can route out MIDI to software/hardware as easily as OSC/DMX.
- **Handles both directions:** Incoming control (from external sources) and outgoing (from cues, UI, etc.) all flow through this hub.

---

### 2. Device COMPs: Platform-Specific I/O

#### Example: `onyx` COMP

- **Inputs:**
  - **DMX IN**: Reads DMX channels from Onyx for live state and signal sync.
  - **OSC IN**: Accepts commands from external OSC controllers/software.
  - **NDI IN**: Optionally processes NDI video/metadata for effect sync or automation.
- **Outputs:**
  - **OSC OUT**: Sends control changes or exposes Onyx state as OSC endpoints.
  - **DMX OUT**: Can output DMX to physical or virtual universes (for merging/bridging).
- **Normalization:** Every input signal is converted to a clean, named event and normalized range (`fader_1`, 0–1, etc.).
- **Pattern Matching:** Uses JSON to map control names to OSC addresses, DMX channels, or UI fields.

#### Example: `midi_in` and `midi_out` COMPs

- **`midi_in`:** Handles multiple controller types, uses pattern files to name and normalize controls, emits clean signals for routing.
- **`midi_out`:** Accepts normalized signals, maps to CC/Note numbers, and sends to the desired MIDI device or software.

#### Example: `resolume`, `pangolin`, etc

- Each manages all in/out for its software, with all endpoints defined in JSON.

---

## 🔁 Data and Signal Flow (Summary)

```
[Hardware/Software IN: MIDI, OSC, DMX, NDI]
       ↓
[Device COMP: signal normalization & naming]
       ↓
[project1 COMP: routing & UI matrix]
       ↓
[Device COMP: output mapping & protocol formatting]
       ↓
[Hardware/Software OUT: OSC, DMX, MIDI, etc.]
```

### Example Flows

- **Artist triggers MIDI fader:**  
  `midi_in` normalizes → `project1` routes → `onyx` COMP maps and sends OSC → Onyx playback fader moves

- **Lighting desk triggers DMX channel:**  
  `onyx` COMP reads DMX IN → normalizes and names → `project1` routes to `resolume` → Resolume layer opacity changes

- **TD cue triggers outgoing MIDI:**  
  UI or script triggers named event → `project1` routes to `midi_out` → MIDI note sent to VJ software

---

## 🗂 Directory Layout (Standardized)

```
src/
├── OPs/
│   ├── Router/
│   │   ├── osc_in.py
│   │   ├── osc_out.py
│   │   ├── routing_engine.py
│   ├── midi_in/
│   │   ├── midi_to_osc.py  
│   ├── onyx/
│   │   ├── ndi_to_onyx.py
│   │   ├── dmx_from_onyx.py
│   │   ├── dmx_to_osc.py
│   │   ├── osc_from_onyx.py
│   │   ├── osc_to_onyx.py
├── patterns/
│   ├── midi/
│   │   ├── apc40_patterns.json
│   │   └── apc_mini_patterns.json
│   ├── onyx/
│   │   ├── onyx_osc_patterns.json
│   │   ├── onyx_dmx_patterns.json
│   │   └── onyx_exposed_patterns.json
│   ├── resolume_patterns.json
│   ├── pangolin/
│   │   ├── quickshow_patterns.json
│   │   └── beyond_patterns.json
```

---

## 🧩 Pattern & Mapping Philosophy

- **Every device has its own pattern JSONs.**  
  These define the mapping between named controls (`fader_1`, `button_A`) and the protocol details (OSC address, DMX channel, MIDI CC, etc.).
- **All normalization logic in Python DATs.**  
  Easy to edit, version, and document.
- **Device COMPs should be able to hot-swap pattern files.**  
  For example, `midi_in` can switch between Akai and Launchpad mappings on the fly.

---

## 🗺️ Routing and UI Details

- **Operator UI lives in `project1`.**  
  Grid or dropdown UI lets user map normalized controls to any available endpoint on any connected device/software.
- **All assignments are saved as JSON routing configs.**  
  These are versioned and reloadable at runtime.
- **Any input can be routed to any output.**  
  Want a MIDI fader to control both a lighting and a media parameter? Just assign it.

---

## 🛠️ Example Implementation Notes

- **All device COMPs should expose Python functions like `emit_signal(name, value)`** for internal integration.
- **Routing logic in `project1/router.py` should support direction tags:**
  - `"incoming"` (external → system)
  - `"outgoing"` (system → external)
  - `"bidirectional"` (e.g., OSC feedback)
- **DMX and OSC range mapping is handled at the device COMP.**  
  Always send 0–1 normalized values from/to the hub.

---

## 🧪 Testing and DevOps (Codex Context)

- **All logic lives in `src/` and can be worked on, tested, and versioned in VS Code.**
- **Use `test_router.py` to simulate input and check routing logic.**
- **TouchDesigner `.toe` is only for UI and operator interface; no heavy logic buried in networks.**
- **Signal flows can be simulated with fake MIDI/OSC/DMX input scripts for headless development.**

---

## 🏗️ Building for Lighting Consoles (Onyx etc.)

- **Standardize your workflow:**
  - Build a dedicated Onyx showfile with pre-defined OSC and DMX endpoints for integration.
  - Only those endpoints are managed by the device COMP.
  - Document the exact showfile config and include it in `/assets/onyx_showfile_template/`.

- **Patterns in `/patterns/onyx/onyx_patterns.json`** define what can be controlled/exposed.

---

## 📝 Dev Task List (Sample)

### Core

- [ ] Refine and document all routing logic in `project1/router.py`
- [ ] Implement `midi_out.py` for full MIDI-to-software routing
- [ ] Normalize all device input in their respective DATs

### UI & Config

- [ ] Expand project1 routing UI to handle new device COMPs
- [ ] Build JSON config loaders/savers for routing assignments

### Device-Specific

- [ ] Finalize Onyx showfile and matching patterns
- [ ] Write/expand pattern JSONs for each device

### Testing

- [ ] Build/fix test scripts for headless data routing
- [ ] Add log/print/debug outputs to all major signal flows

---

## 💬 Community, Teamwork, and Evolution

- All contributions happen in VS Code, via Git, in `src/`.
- **DAT scripts and JSON patterns** are the source of truth.
- Keep PRs clean and scoped—one device, one fix, one feature at a time.
- Document everything—add new README files to any complex directory.

---

## 🏁 The Endgame

A truly modular, cross-platform, code-managed live control matrix that lets your team (or any operator) route, map, override, and automate their entire show’s signals from a single source of truth—*with no more TouchDesigner spaghetti!*

---

**For any further questions, add a new issue or update this README as the system grows. Happy coding and live control!**
