from __future__ import annotations

from time import sleep

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def play_boot(console: Console) -> None:
    console.clear()
    console.print()
    console.print(
        Panel(
            Text("nazzos booting...", style="bold bright_white"),
            border_style="bright_cyan",
            title="[bold bright_cyan]nazzos[/bold bright_cyan]",
        )
    )
    sleep(0.4)
    console.clear()