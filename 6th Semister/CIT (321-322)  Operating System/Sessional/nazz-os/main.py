#!/usr/bin/env python3
"""
Launcher: run the inner `nazz-os/main.py` when executed from the repo root.

Usage:
    python main.py
"""
from pathlib import Path
import runpy
import sys

HERE = Path(__file__).parent
INNER = HERE / "nazz-os" / "main.py"

if not INNER.exists():
    sys.stderr.write(f"Error: expected {INNER} to exist but it does not.\n")
    sys.exit(1)

# Ensure inner package directories are importable (so `import ui` works)
sys.path.insert(0, str(HERE / "nazz-os"))

runpy.run_path(str(INNER), run_name="__main__")
