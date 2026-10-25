from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time


def play_boot(console: Console) -> None:
    console.print(Panel(Text("nazzos — Interactive OS Simulator", justify="center", style="title"), border_style="bright_cyan"))
    console.print("[accent]Initializing subsystems...[/accent]")
    subsystems = [
        "Scheduler",
        "Memory Manager",
        "Virtual FS",
        "Disk Scheduler",
        "Deadlock Detector",
        "Dashboard",
        "Learning Module",
    ]
    for s in subsystems:
        console.print(f"  [info]-[/info] {s} [dim]ready[/dim]")
        time.sleep(0.03)
    console.print("\n[success]Boot complete. Welcome![/success]\n")
