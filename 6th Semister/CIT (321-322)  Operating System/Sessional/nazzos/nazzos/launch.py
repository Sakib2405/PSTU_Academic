#!/usr/bin/env python3
"""
nazzos Launcher — opens the app in a new terminal window automatically.
Double-click this file or run: python launch.py
"""
import subprocess
import sys
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable
MAIN   = os.path.join(HERE, "main.py")

TERMINALS = [
    # command, [args to run a command inside it]
    ("konsole",       ["konsole", "-e"]),
    ("gnome-terminal",["gnome-terminal", "--"]),
    ("xfce4-terminal",["xfce4-terminal", "-e"]),
    ("xterm",         ["xterm", "-e"]),
    ("lxterminal",    ["lxterminal", "-e"]),
    ("mate-terminal", ["mate-terminal", "-e"]),
    ("tilix",         ["tilix", "-e"]),
    ("kitty",         ["kitty"]),
    ("alacritty",     ["alacritty", "-e"]),
    ("wezterm",       ["wezterm", "start", "--"]),
]

def find_terminal():
    for name, cmd in TERMINALS:
        if shutil.which(name):
            return cmd
    return None

def main():
    term = find_terminal()
    if term is None:
        print("No supported terminal found. Run directly: python main.py")
        sys.exit(1)

    cmd = term + [PYTHON, MAIN]
    subprocess.Popen(cmd, cwd=HERE)

if __name__ == "__main__":
    main()
