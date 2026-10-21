import time
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box
from ui.theme import get_process_style, get_mem_style


def section_header(console: Console, title: str, subtitle: str = "") -> None:
    t = Text()
    t.append(f" ◆ {title} ", style="bold bright_cyan")
    if subtitle:
        t.append(f"— {subtitle}", style="dim white")
    console.print()
    console.print(Panel(t, border_style="bright_cyan", padding=(0, 1)))


def print_gantt(console: Console, timeline: list[tuple], total_time: int,
                animate: bool = True) -> None:
    """
    timeline: list of (process_name, start, end) tuples
    """
    proc_index: dict[str, int] = {}
    idx = 0

    gantt_top    = Text()
    gantt_middle = Text()
    gantt_bottom = Text()
    time_row     = Text()

    gantt_top.append("┌")
    gantt_bottom.append("└")

    time_marks: list[int] = []
    current = 0

    for name, start, end in timeline:
        if name not in proc_index:
            proc_index[name] = idx
            idx += 1
        style = get_process_style(proc_index[name]) if name != "IDLE" else "dim white on grey15"
        width = max((end - start) * 3, len(name) + 2)
        label = name.center(width)

        gantt_top.append("─" * (width) + "┬")
        gantt_middle.append(f" {label} │", style=style)
        gantt_bottom.append("─" * (width) + "┴")
        time_marks.append((current, str(start)))
        current += width + 1

    time_marks.append((current, str(total_time)))

    console.print()
    if animate:
        console.print("  [bold cyan]Gantt Chart:[/bold cyan]")
        for name, start, end in timeline:
            style = get_process_style(proc_index[name]) if name != "IDLE" else "dim white on grey15"
            width = max((end - start) * 3, len(name) + 2)
            bar = Text(f" {'[' + name + ']':^{width}} ", style=style)
            console.print(f"  t={start:>3}–{end:<3}  ", end="")
            console.print(bar)
            time.sleep(0.12)
    else:
        console.print("  [bold cyan]Gantt Chart:[/bold cyan]")
        row = Text("  ")
        for name, start, end in timeline:
            style = get_process_style(proc_index[name]) if name != "IDLE" else "dim white on grey15"
            width = max((end - start) * 3, len(name) + 2)
            row.append(f" {name:^{width}} ", style=style)
        console.print(row)

    time_str = "  "
    prev = 0
    for pos, mark in time_marks:
        time_str += " " * (pos - prev) + mark
        prev = pos + len(mark)
    console.print(f"[dim]{time_str}[/dim]")
    console.print()


def print_mem_grid(console: Console, frames: list, total: int,
                   proc_index: dict[str, int]) -> None:
    cols_per_row = 8
    rows = (total + cols_per_row - 1) // cols_per_row

    console.print("  [bold cyan]Memory Frame Map:[/bold cyan]")
    for r in range(rows):
        row_text = Text("  ")
        for c in range(cols_per_row):
            fi = r * cols_per_row + c
            if fi >= total:
                break
            name = frames[fi]
            if name is None:
                row_text.append(f"[{fi:02d}]", style="dim white on grey19")
            else:
                style = get_mem_style(proc_index.get(name, 0))
                label = f"{name[:2]:^4}"
                row_text.append(f"[{label}]", style=style)
        console.print(row_text)
    console.print()


def print_matrix_table(console: Console, title: str,
                       headers: list[str], rows: list[list]) -> None:
    table = Table(title=title, box=box.ROUNDED, border_style="bright_cyan",
                  header_style="bold bright_white on dark_blue", show_lines=True)
    for h in headers:
        table.add_column(h, justify="center")
    for row in rows:
        table.add_row(*[str(x) for x in row])
    console.print(table)
    console.print()


def bar_chart(console: Console, title: str, data: list[tuple[str, float]],
              max_width: int = 30, color: str = "bright_green") -> None:
    console.print(f"  [bold cyan]{title}[/bold cyan]")
    max_val = max(v for _, v in data) if data else 1
    for label, val in data:
        filled = int((val / max_val) * max_width) if max_val else 0
        bar = "█" * filled + "░" * (max_width - filled)
        console.print(f"  {label:>12}  [{color}]{bar}[/{color}]  {val:.2f}")
    console.print()
