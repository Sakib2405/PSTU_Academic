from __future__ import annotations
import time
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import BarColumn, Progress, TextColumn
from rich.tree import Tree
from rich import box
from modules.filesystem import VirtualFS


def _cpu_bar(pct: float, width: int = 20) -> Text:
    filled = int(pct / 100 * width)
    bar    = "█" * filled + "░" * (width - filled)
    color  = "bright_green" if pct < 60 else ("yellow" if pct < 85 else "red")
    t = Text()
    t.append(f"[{bar}] ", style=color)
    t.append(f"{pct:5.1f}%", style="bold white")
    return t


def _make_process_panel() -> Panel:
    table = Table(box=box.SIMPLE, show_header=True,
                  header_style="bold white", expand=True)
    table.add_column("PID",     width=7, justify="right")
    table.add_column("Name",    width=16)
    table.add_column("CPU%",    width=7, justify="right")
    table.add_column("MEM%",    width=7, justify="right")
    table.add_column("Status",  width=10)

    procs = sorted(psutil.process_iter(["pid", "name", "cpu_percent",
                                        "memory_percent", "status"]),
                   key=lambda p: p.info.get("cpu_percent") or 0, reverse=True)[:12]

    for p in procs:
        info   = p.info
        status = info.get("status", "?")
        color  = "green" if status == "running" else ("yellow" if status == "sleeping" else "dim")
        cpu    = info.get("cpu_percent") or 0.0
        mem    = info.get("memory_percent") or 0.0
        table.add_row(
            str(info.get("pid", "?")),
            (info.get("name") or "?")[:15],
            f"{cpu:.1f}",
            f"{mem:.1f}",
            Text(status[:9], style=color),
        )
    return Panel(table, title="[bold bright_cyan]⚡ Live Processes[/bold bright_cyan]",
                 border_style="bright_cyan", padding=(0, 1))


def _make_memory_panel() -> Panel:
    vm   = psutil.virtual_memory()
    swap = psutil.swap_memory()

    lines = Text()
    lines.append("  RAM  ", style="bold cyan")
    lines.append(_cpu_bar(vm.percent))
    lines.append(f"\n  {vm.used // 1024**2} MB / {vm.total // 1024**2} MB\n\n", style="dim")

    lines.append("  SWAP ", style="bold magenta")
    lines.append(_cpu_bar(swap.percent))
    lines.append(f"\n  {swap.used // 1024**2} MB / {swap.total // 1024**2} MB\n\n", style="dim")

    cpu_pcts = psutil.cpu_percent(percpu=True)
    lines.append("  CPU Cores:\n", style="bold yellow")
    for i, pct in enumerate(cpu_pcts[:8]):
        lines.append(f"  Core {i}: ")
        lines.append(_cpu_bar(pct, width=12))
        lines.append("\n")

    return Panel(lines, title="[bold bright_cyan]💾 System Memory & CPU[/bold bright_cyan]",
                 border_style="bright_cyan", padding=(0, 1))


def _make_fs_panel(fs: VirtualFS) -> Panel:
    tree = Tree(Text("📁 /", style="bold bright_blue"), guide_style="bright_cyan")

    def add_children(t_node, fs_node, depth=0):
        if depth > 2:
            return
        for name, child in list(fs_node.children.items())[:6]:
            if child.is_dir:
                label = Text(f"📁 {name}/", style="bold bright_blue")
                branch = t_node.add(label)
                add_children(branch, child, depth + 1)
            else:
                label = Text(f"📄 {name}", style="bright_white")
                t_node.add(label)

    add_children(tree, fs.root)
    return Panel(tree, title="[bold bright_cyan]📂 Virtual File System[/bold bright_cyan]",
                 border_style="bright_cyan", padding=(0, 1))


def _make_info_panel(elapsed: int) -> Panel:
    t = Text()
    t.append("  nazzos Dashboard\n", style="bold bright_green")
    t.append(f"  Uptime: {elapsed}s\n", style="dim")
    t.append("  Press [bold cyan]Ctrl+C[/bold cyan] to exit\n\n", style="dim")

    disk = psutil.disk_usage("/")
    t.append("  Disk Usage:\n", style="bold yellow")
    t.append(_cpu_bar(disk.percent))
    t.append(f"\n  {disk.used // 1024**3} GB / {disk.total // 1024**3} GB\n\n", style="dim")

    net = psutil.net_io_counters()
    t.append("  Network:\n", style="bold magenta")
    t.append(f"  ↑ Sent: {net.bytes_sent // 1024**2} MB\n", style="green")
    t.append(f"  ↓ Recv: {net.bytes_recv // 1024**2} MB\n", style="cyan")

    return Panel(t, title="[bold bright_cyan]ℹ System Info[/bold bright_cyan]",
                 border_style="bright_cyan", padding=(0, 1))


def run_dashboard(console: Console, fs: VirtualFS) -> None:
    console.print("\n  [bold cyan]Starting live dashboard... Press Ctrl+C to exit.[/bold cyan]\n")
    time.sleep(0.5)

    start = time.time()
    try:
        with Live(console=console, refresh_per_second=1, screen=True) as live:
            while True:
                elapsed = int(time.time() - start)
                layout  = Layout()
                layout.split_column(
                    Layout(name="top",    ratio=3),
                    Layout(name="bottom", ratio=2),
                )
                layout["top"].split_row(
                    Layout(name="procs", ratio=3),
                    Layout(name="mem",   ratio=2),
                )
                layout["bottom"].split_row(
                    Layout(name="fs",   ratio=2),
                    Layout(name="info", ratio=2),
                )
                layout["procs"].update(_make_process_panel())
                layout["mem"].update(_make_memory_panel())
                layout["fs"].update(_make_fs_panel(fs))
                layout["info"].update(_make_info_panel(elapsed))
                live.update(layout)
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n  [yellow]Dashboard closed.[/yellow]\n")
