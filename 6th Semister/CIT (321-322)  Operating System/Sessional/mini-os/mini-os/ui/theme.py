from rich.style import Style
from rich.theme import Theme

NAZZOS_THEME = Theme({
    "banner":       "bold bright_green",
    "prompt":       "bold cyan",
    "success":      "bold green",
    "error":        "bold red",
    "warning":      "bold yellow",
    "info":         "bold cyan",
    "header":       "bold white on dark_blue",
    "subheader":    "bold bright_cyan",
    "dim":          "dim white",
    "gantt.p1":     "bold white on blue",
    "gantt.p2":     "bold white on red",
    "gantt.p3":     "bold white on green",
    "gantt.p4":     "bold white on magenta",
    "gantt.p5":     "bold white on yellow",
    "gantt.p6":     "bold white on cyan",
    "gantt.idle":   "dim white on dark_green",
    "mem.free":     "dim white on grey23",
    "mem.p1":       "bold white on blue",
    "mem.p2":       "bold white on red",
    "mem.p3":       "bold white on green",
    "mem.p4":       "bold white on magenta",
    "mem.p5":       "bold white on yellow",
    "mem.p6":       "bold white on dark_cyan",
    "mem.p7":       "bold white on dark_orange",
    "mem.p8":       "bold white on purple",
    "safe":         "bold bright_green",
    "unsafe":       "bold bright_red",
    "thinking":     "dim cyan",
    "hungry":       "bold yellow",
    "eating":       "bold green",
    "file":         "bright_white",
    "dir":          "bold bright_blue",
    "panel.border": "bright_cyan",
})

PROCESS_COLORS = [
    "blue", "red", "green", "magenta", "yellow",
    "cyan", "dark_orange", "purple", "dark_red", "dark_green"
]

GANTT_STYLES = [
    "bold white on blue",
    "bold white on red",
    "bold white on green",
    "bold white on magenta",
    "bold black on yellow",
    "bold black on cyan",
    "bold white on dark_orange",
    "bold white on purple",
]

MEM_STYLES = [
    "bold white on blue",
    "bold white on red",
    "bold white on green",
    "bold white on magenta",
    "bold black on yellow",
    "bold black on cyan",
    "bold white on dark_orange",
    "bold white on purple",
    "bold white on dark_red",
    "bold white on dark_green",
]

def get_process_style(index: int) -> str:
    return GANTT_STYLES[index % len(GANTT_STYLES)]

def get_mem_style(index: int) -> str:
    return MEM_STYLES[index % len(MEM_STYLES)]
