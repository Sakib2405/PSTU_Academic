from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def section_header(console: Console, title: str) -> None:
    console.print(Panel(Text(title, style="title"), border_style="bright_cyan"))
