# TouchDesigner Show Control

**Overview:**
This repository hosts a fully code-driven show control framework built in TouchDesigner, designed to route and transform OSC signals across a wide range of AV systems—including lighting desks, laser controllers, MIDI devices, and Resolume—using a unified, modular, and version-controlled approach.

**Key Features:**

* **Code-First Architecture:** All logic is implemented in Python scripts and DATs, enabling robust customization and seamless integration with VSCode and GitHub.
* **Central OSC API Hub:** A single JSON-based configuration defines generic inputs, outputs, and routing rules. Modular mapping files translate generic outputs into software-specific OSC addresses.
* **Dynamic Address Builder UI:** Operators construct OSC addresses in real time via intuitive dropdowns and numeric fields within TD, abstracting away low-level address syntax.
* **Version-Controlled Components:** Core network logic (OSC I/O, UI panels) is packaged as external `.tox` components and editable Text DATs, ensuring reproducibility and easy collaboration.
* **AI-Assisted Development:** OpenAI Codex (via VSCode GitHub integration) powers code generation, documentation, and iterative enhancements, acting as your personal development team.

**Repository Structure:**

```bash
project-root/
├── .github/                  # CI/CD pipeline definitions
├── assets/                   # Media assets (textures, UI graphics)
├── src/                      # Core code and configuration
│   ├── DATs/                 # Editable Text DAT scripts (callbacks, templates)
│   ├── scripts/              # Python modules (osc_helpers.py, ui_helpers.py)
│   ├── osc_patterns.json     # Generic OSC endpoint templates
│   ├── resolume_mapping.json # Resolume-specific address mappings
│   └── laser_mapping.json    # Laser-specific address mappings
├── showcontrol.toe           # Main TouchDesigner project file
├── README.md                 # This overview and usage guide
└── .gitignore
```

<<<<<<< HEAD
<!-- Example configs live in `config/routing_map.json`, `config/input_aliases.json`, and `config/endpoints.json`. -->
=======
## Getting Started

1. **Clone & Open:**

   ```bash
   git clone <repo-url>
   cd touchdesigner-showcontrol
   code .
   ```

2. **Edit Configs & Code:**

   * Update JSON patterns and mapping files in `src/`.
   * Modify Python modules in `src/scripts/` and Text DATs in `src/DATs/` using VSCode.
3. **Load in TD & Sync:**

   * Open `showcontrol.toe` in TouchDesigner.
   * Ensure Text DATs point to the `src/DATs/*.txt` files and have “Keep in sync” enabled.
4. **Test & Iterate:**

   * Trigger OSC inputs, build addresses in the UI, and verify routing via OSC Out DAT.
   * Use **Alt+R** to refresh DATs after changes.
5. **Leverage Codex:**

   * Use GitHub Copilot/Codex in VSCode to generate, refine, and document code and JSON schemas.

---

**Keep this README up to date as the project evolves to ensure maximum clarity for both human collaborators and AI assistants.**
>>>>>>> main
