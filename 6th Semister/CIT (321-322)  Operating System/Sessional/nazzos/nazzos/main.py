#!/usr/bin/env python3
"""
nazzos — Interactive Terminal OS Simulator
Run: python main.py
"""
import sys
from rich.console import Console
from ui.theme import NAZZOS_THEME
from ui.boot  import play_boot
from shell    import run_shell


def main() -> None:
    console = Console(theme=NAZZOS_THEME)
    try:
        play_boot(console)
        run_shell(console)
    except KeyboardInterrupt:
        console.print("\n\n  [bold bright_green]nazzos terminated. Goodbye![/bold bright_green]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
