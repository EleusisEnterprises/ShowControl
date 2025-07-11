# ShowControl: Modular Code-Driven Signal Routing for Live Shows

---

## 🎯 Vision

ShowControl is a next-generation, code-first platform for managing, routing, and transforming real-time control signals across the worlds of lighting, video, lasers, and MIDI devices. It is designed from the ground up to allow anyone—show operators, artists, coders—to wire together their ideal hybrid AV control system using modern, maintainable software practices.

---

## 🚀 What Is It?

ShowControl replaces the “spaghetti” of traditional TouchDesigner (and similar) setups with a **central signal routing brain**.
All devices—lighting consoles, media servers, MIDI controllers, laser software—connect to this hub through standardized “device COMPs.”
Each device COMP normalizes its own incoming and outgoing data, converting hardware/protocol specifics into simple, named controls with values normalized to a standard range (usually 0–1).

All routing and mapping between controls and destinations is handled by a **central Routing COMP**, driven by Python scripts and a live operator GUI.
This means show control is:

- **Configurable at runtime** (assign any input to any output on the fly)
- **Version controlled** (all logic in Python scripts and JSON configs)
- **Scalable** (add/remove devices as your show evolves)
- **Collaborative** (develop and manage in VS Code, not just in TouchDesigner)

---

## 🏗️ System Overview

- **Device COMPs** (e.g., Onyx, Resolume, APCmini, Quickshow):
  Each handles *all* in/out for a given device or software—MIDI, OSC, DMX, NDI, etc.
  Converts “raw” signals to named and normalized controls, and vice versa.

- **Scripts COMP/Directory**:
  All reusable Python logic is centralized here (OSC helpers, DMX converters, routing engine, etc.) for easy access and zero duplication.

- **Routing COMP** (project1):
  The heart of the system. Collects all pre-converted controls from every device, presents them to the operator via a GUI, and dispatches signals to the proper outputs.
  Handles both incoming external control (e.g., from a lighting desk or artist controller) and outgoing show cues.

- **Operator GUI**:
  Provides real-time patching—reassign any fader, button, or control to any destination.
  All assignments are stored as versionable JSON files for persistence and teamwork.

---

## 🔄 Signal Flow (Example)

1. **A MIDI controller fader is moved**
   → The relevant Device COMP converts and normalizes it to a control signal:
   `("fader_1", 0.63)`

2. **Signal arrives at the Routing COMP**
   → The GUI shows this as an available control for assignment
   → Operator maps it to (for example) "Resolume Layer 1 Opacity"

3. **Routing COMP dispatches to Resolume Device COMP**
   → Resolume Device COMP formats and sends the proper OSC message out

4. **Or, the reverse:**
   An OSC message from Quickshow or DMX value from Onyx comes in, is normalized and renamed, and can be mapped to control any other device or even sent back out as MIDI.

---

## ⚡ Key Features

- **Any-to-any routing:** Patch any input (fader, button, cue, DMX channel, OSC endpoint, MIDI CC) to any output, at any time.
- **True modularity:** Each device or protocol gets its own isolated, reusable COMP and pattern files.
- **All logic in code:** Maintain and expand your system in VS Code with proper version control and code review.
- **Operator-focused:** Live GUI for on-the-fly control mapping and assignment—no more show-stopping rewires.
- **Extensible:** Add new hardware, software, or protocols by simply creating a new device COMP and mapping patterns.
- **Collaborative:** Designed for teams, with clear division between UI, routing, and device logic.

---

## 🗂️ Repo Structure (Recommended)
- `src/` – Core application modules
- `config/` – Runtime configuration and presets
- `assets/` – Reference diagrams and documentation
- `tests/` – Automated unit tests

---

## 🛠️ Basic Setup

1. Clone this repository and open it in VS Code or your editor of choice.
2. (Optional) Create a virtual environment and install dependencies:
   `pip install -r requirements.txt`
3. Use the modules inside `src/` within your TouchDesigner project or other Python environment to build out your show-control pipeline.
4. Add device-specific configuration in `config/` and keep diagrams or notes in `assets/` as your system evolves.

