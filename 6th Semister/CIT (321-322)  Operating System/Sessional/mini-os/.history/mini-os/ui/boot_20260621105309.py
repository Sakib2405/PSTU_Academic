import time
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.align import Align

LOGO = r"""
 ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███████╗
 ████╗ ████║██║████╗  ██║██║██╔═══██╗██╔════╝
 ██╔████╔██║██║██╔██╗ ██║██║██║   ██║███████╗
 ██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║╚════██║
 ██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝███████║
 ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
"""

SUBTITLE = "Interactive OS Simulator | v1.0.0"
TAGLINE  = "Scheduler • Memory • FileSystem • Disk • Deadlock • Sync"

BOOT_MESSAGES = [
    ("[  0.000000] nazzos kernel loading...",                      0.08),
    ("[  0.012345] Initializing CPU scheduler subsystem...",       0.07),
    ("[  0.034812] Memory management unit online (16 MB)",         0.07),
    ("[  0.058901] Virtual file system mounted at /",              0.06),
    ("[  0.082345] Disk I/O scheduler initialized (SCAN mode)",    0.07),
    ("[  0.101234] Deadlock detection engine: Banker's Algorithm", 0.07),
    ("[  0.123456] Synchronization primitives loaded",             0.06),
    ("[  0.145678] Loading process table...",                      0.07),
    ("[  0.167890] Terminal driver initialized (tty0)",            0.06),
    ("[  0.189012] Network stack: skipped (standalone mode)",      0.06),
    ("[  0.201234] All subsystems online.",                        0.08),
    ("[  0.210000] Starting nazzos shell...",                      0.10),
]


def play_boot(console: Console) -> None:
    console.clear()

    logo_text = Text(LOGO, style="bold bright_green")
    sub_text  = Text(SUBTITLE, style="bold cyan", justify="center")
    tag_text  = Text(TAGLINE,  style="dim white",  justify="center")

    console.print(Align.center(logo_text))
    console.print(Align.center(sub_text))
    console.print(Align.center(tag_text))
    console.print()

    for msg, delay in BOOT_MESSAGES:
        if "online" in msg or "mounted" in msg or "initialized" in msg:
            color = "bright_green"
        elif "skipped" in msg:
            color = "yellow"
        elif "Starting" in msg:
            color = "bold bright_cyan"
        else:
            color = "green"
        console.print(f"  {msg}", style=color)
        time.sleep(delay)

    console.print()

    with Progress(
        TextColumn("  [bold cyan]Booting kernel"),
        BarColumn(bar_width=40, style="green", complete_style="bright_green"),
        TextColumn("[bold white]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("boot", total=100)
        for i in range(100):
            time.sleep(0.018)
            progress.advance(task, 1)

    console.print()
    console.print("  [bold bright_green]✓ Boot complete. Type [bold cyan]help[/bold cyan] to get started.[/bold bright_green]")
    console.print()
    time.sleep(0.4)
