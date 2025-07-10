# Assets

This folder contains media used by TouchDesigner, including images, textures,
logos, and sample recordings for testing or previews.

Subfolders:

- `images/` – UI mockups, stage reference shots, textures, and logos
- `test_inputs/` – recorded signal files or dummy control sequences

Device‑specific show files or example project files should live in their own
subdirectories here. For instance, the root README describes building a
standard Onyx show file with predetermined OSC and DMX endpoints. When that
template is created, place it under `onyx_showfile_template/` so all
collaborators can load the same configuration.

No large binaries are included yet to keep the repository lightweight.

<!-- Example configs live in `config/routing_map.json`, `config/input_aliases.json`, and `config/endpoints.json`. -->
