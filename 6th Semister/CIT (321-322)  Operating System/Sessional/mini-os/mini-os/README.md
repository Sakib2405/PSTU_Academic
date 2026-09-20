# nazzos — Interactive OS Simulator

This repository is a small, educational OS simulator (formerly `mini-os`) adapted and renamed to `nazzos`.

## Project Overview

- **Name:** nazzos
- **Description:** Interactive terminal-based OS simulator demonstrating simple scheduler, memory, filesystem, disk, deadlock, and sync subsystems.
- **Language:** Python 3
- **UI:** rich + prompt_toolkit

## Prerequisites

- Python 3.10+ (or 3.8+ in many environments)
- pip

Install the Python dependencies (example):

```bash
python -m pip install -r requirements.txt
```

If there is no `requirements.txt`, install these packages:

```bash
python -m pip install rich prompt-toolkit psutil
```

## Run (inner copy)

Start the simulator from the inner project folder (the one containing `main.py` and the `ui`/`modules` packages):

```bash
cd path/to/mini-os/mini-os
python main.py
```

When the program boots you should see the ASCII banner and a prompt like:

```
nazzos [/]> 
```

Use `help` inside the simulator to see available commands. Use `exit` to quit.

## Run (new `nazzos` package copy)

If you copied or created a top-level `nazzos` package (e.g. `Sessional/nazzos/nazzos`), run from that folder:

```bash
cd path/to/Sessional/nazzos/nazzos
python main.py
```

Note: the code performs imports like `from ui.theme import NAZZOS_THEME` and `from modules.filesystem import VirtualFS`. For imports to work, run `python main.py` from the package root where `ui/` and `modules/` are sibling directories of `main.py`.

## Renames and important notes

- The UI theme constant was renamed from `MINIOS_THEME` to `NAZZOS_THEME` in `ui/theme.py`. Update any custom code that referenced the old name.
- The desktop entry `MiniOS.desktop` was replaced/renamed to `nazzos.desktop`. If you use the desktop file, verify the `Exec` path points to your Python interpreter and project location.
- Many user-facing strings have been updated to read `nazzos` instead of `MiniOS`.

## Cleaning up old history and references

There are `.history` files under the workspace that may contain old snapshots with `MINIOS` references. To remove them:

```bash
rm -r .history
# or delete specific files in your editor / file explorer on Windows
```

Be careful: only delete `.history` if you don't need the saved snapshots.

## Troubleshooting

- ImportError: If you see `ModuleNotFoundError` for `ui` or `modules`, ensure you ran `python main.py` from the project folder that contains those packages.
- Theme or symbol errors: If code mentions `MINIOS_THEME`, replace it with `NAZZOS_THEME` or update imports accordingly.
- Missing dependencies: install `rich`, `prompt-toolkit`, and `psutil`.

## File map (important files)

- `main.py` — launcher / entrypoint for the simulator
- `launch.py` — helper launcher script
- `shell.py` — REPL-style shell implementation
- `ui/boot.py` — boot banner, subtitle, and boot messages
- `ui/theme.py` — theme constants (now `NAZZOS_THEME`)
- `modules/filesystem.py` — in-memory virtual FS implementation
- `nazzos.desktop` — desktop entry (if present)

## Next steps and suggestions

- If you want to permanently rename the repository directory from `mini-os` → `nazzos`, do so at the filesystem level and then update any absolute paths in `nazzos.desktop` or other scripts.
- Optionally remove the original `mini-os` copy after verifying the `nazzos` copy boots and behaves correctly.

## License

This project contains school/educational code. No license file provided — ask the original author if you need licensing details before redistribution.

---

If you want, I can:
- run `python main.py` from your `Sessional/nazzos/nazzos` folder and verify startup, or
- update the `requirements.txt` file and add a short `CONTRIBUTING.md`.
