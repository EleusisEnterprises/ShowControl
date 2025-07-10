# 📡 TouchDesigner Show Control System

**An open modular AV signal router for live shows and installations.**

This project is a TouchDesigner-based show control framework designed to route and manage control signals between AV devices, software, and controllers. It allows you to ingest data from multiple sources like MIDI controllers, lighting consoles, or VJ software, and send it to multiple destinations such as Resolume, laser systems, Unreal Engine, or lighting software.

The system uses **OSC as the base protocol**, features a **simple UI for mapping controls**, and stores all logic, signal routing, and configuration in external files for easy version control and collaboration.

---

## 🔧 Features (Phase 1)

- Receive OSC and MIDI input
- Assign friendly names to raw signal channels
- Route signals to labeled destinations (with optional scaling)
- Send processed OSC messages to external software or devices
- Live-editable routing map stored as JSON
- Git-tracked structure with modular Python logic

---

## 🎯 Future Plans (Phase 2+)

- Drag-and-drop matrix routing UI
- Stage image → 3D mesh converter for projection mapping
- Procedural texture generation
- AI-assisted stage tracing
- Show presets and performance profiles
- Plugin support for custom routing logic

---

## 🛠️ Project Structure

```bash
├── td-project.toe              # TouchDesigner project file
├── src/                        # Python logic for routing, signal parsing, UI
├── config/                     # Routing maps, signal aliases, endpoint configs
├── config/presets/             # Show profiles and saved signal maps
├── ui/                         # Reusable UI components (.tox)
├── assets/                     # Images, test input data, support files
├── requirements.txt            # External Python dependencies (if needed)
├── .gitignore                  # Ignore logs, backups, etc.
└── README.md                   # You're here!
```

<!-- Example configs live in `config/routing_map.json`, `config/input_aliases.json`, and `config/endpoints.json`. -->
