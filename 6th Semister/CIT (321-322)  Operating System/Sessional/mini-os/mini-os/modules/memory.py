from __future__ import annotations
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box
from ui.widgets import section_header, print_mem_grid, bar_chart
from ui.theme import get_mem_style


class MemoryManager:
    def __init__(self, total_frames: int = 16):
        self.total  = total_frames
        self.frames: list[str | None] = [None] * total_frames
        self.proc_index: dict[str, int] = {}
        self._color_idx = 0

    def _assign_color(self, name: str) -> None:
        if name not in self.proc_index:
            self.proc_index[name] = self._color_idx
            self._color_idx += 1

    def init(self, total: int) -> str:
        self.total  = total
        self.frames = [None] * total
        self.proc_index.clear()
        self._color_idx = 0
        return f"[green]Memory initialized: {total} frames.[/green]"

    def alloc(self, name: str, pages: int, algo: str = "firstfit") -> str:
        self._assign_color(name)
        free_blocks = self._free_blocks()
        chosen = None
        if algo == "firstfit":
            for start, length in free_blocks:
                if length >= pages:
                    chosen = start; break
        elif algo == "bestfit":
            valid = [(s, l) for s, l in free_blocks if l >= pages]
            if valid:
                chosen = min(valid, key=lambda x: x[1])[0]
        elif algo == "worstfit":
            valid = [(s, l) for s, l in free_blocks if l >= pages]
            if valid:
                chosen = max(valid, key=lambda x: x[1])[0]
        else:
            return f"[red]Unknown algo: {algo}. Use firstfit|bestfit|worstfit[/red]"

        if chosen is None:
            return f"[red]Not enough contiguous frames for {name} ({pages} pages needed).[/red]"

        for i in range(chosen, chosen + pages):
            self.frames[i] = name
        return f"[green]Allocated {pages} frames to [bold]{name}[/bold] (algo={algo}, start={chosen})[/green]"

    def free(self, name: str) -> str:
        if name not in [f for f in self.frames if f]:
            return f"[red]Process '{name}' not found in memory.[/red]"
        count = sum(1 for f in self.frames if f == name)
        self.frames = [None if f == name else f for f in self.frames]
        return f"[green]Freed {count} frames from {name}.[/green]"

    def show(self, console: Console) -> None:
        section_header(console, "Memory Frame Map")
        print_mem_grid(console, self.frames, self.total, self.proc_index)
        used  = sum(1 for f in self.frames if f is not None)
        free  = self.total - used
        frag  = self._fragmentation()
        table = Table(box=box.SIMPLE, border_style="dim")
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value",  style="bold white")
        table.add_row("Total Frames", str(self.total))
        table.add_row("Used",         str(used))
        table.add_row("Free",         str(free))
        table.add_row("Fragmentation", f"{frag:.1f}%")
        console.print(table)

    def _free_blocks(self) -> list[tuple[int, int]]:
        blocks, i = [], 0
        while i < self.total:
            if self.frames[i] is None:
                start = i
                while i < self.total and self.frames[i] is None:
                    i += 1
                blocks.append((start, i - start))
            else:
                i += 1
        return blocks

    def _fragmentation(self) -> float:
        blocks = self._free_blocks()
        if not blocks:
            return 0.0
        largest = max(l for _, l in blocks)
        total_free = sum(l for _, l in blocks)
        return (1 - largest / total_free) * 100 if total_free else 0.0

    # ── Page Replacement ─────────────────────────────────────────────────
    def page_fault_sim(self, console: Console, ref_string: list[int],
                       num_frames: int, algo: str) -> None:
        section_header(console, f"Page Replacement — {algo.upper()}",
                       f"Frames={num_frames}, References={len(ref_string)}")
        if   algo == "fifo":    faults, history = self._fifo(ref_string, num_frames)
        elif algo == "lru":     faults, history = self._lru(ref_string, num_frames)
        elif algo == "optimal": faults, history = self._optimal(ref_string, num_frames)
        elif algo == "clock":   faults, history = self._clock(ref_string, num_frames)
        else:
            console.print(f"[red]Unknown algo: {algo}. Use fifo|lru|optimal|clock[/red]")
            return

        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Ref", justify="center", style="bold")
        for i in range(num_frames):
            table.add_column(f"F{i}", justify="center")
        table.add_column("Fault?", justify="center")

        for ref, frames_snap, fault in history:
            row = [str(ref)]
            for i in range(num_frames):
                if i < len(frames_snap) and frames_snap[i] is not None:
                    row.append(str(frames_snap[i]))
                else:
                    row.append("—")
            row.append("[red]✗ FAULT[/red]" if fault else "[green]✓ HIT[/green]")
            table.add_row(*row)

        console.print(table)
        hits = len(ref_string) - faults
        console.print(f"\n  [bold]Page Faults:[/bold] [red]{faults}[/red]  |  "
                      f"[bold]Hits:[/bold] [green]{hits}[/green]  |  "
                      f"[bold]Hit Ratio:[/bold] {hits/len(ref_string)*100:.1f}%\n")

    def compare_page_algos(self, console: Console, ref_string: list[int],
                           num_frames: int) -> None:
        section_header(console, "Page Replacement Comparison",
                       f"Frames={num_frames}, Ref string length={len(ref_string)}")
        algos = ["fifo", "lru", "optimal", "clock"]
        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Algorithm", style="bold bright_cyan")
        table.add_column("Page Faults", justify="center")
        table.add_column("Hits",        justify="center")
        table.add_column("Hit Ratio",   justify="center")

        for algo in algos:
            if   algo == "fifo":    faults, _ = self._fifo(ref_string, num_frames)
            elif algo == "lru":     faults, _ = self._lru(ref_string, num_frames)
            elif algo == "optimal": faults, _ = self._optimal(ref_string, num_frames)
            elif algo == "clock":   faults, _ = self._clock(ref_string, num_frames)
            hits = len(ref_string) - faults
            table.add_row(algo.upper(), str(faults), str(hits),
                          f"{hits/len(ref_string)*100:.1f}%")
        console.print(table)
        console.print()

    def _fifo(self, refs: list[int], nf: int):
        frames: list[int | None] = [None] * nf
        queue: list[int] = []
        faults = 0
        history = []
        for ref in refs:
            fault = ref not in [f for f in frames if f is not None]
            if fault:
                faults += 1
                if len(queue) < nf:
                    for i in range(nf):
                        if frames[i] is None:
                            frames[i] = ref; break
                else:
                    old = queue.pop(0)
                    idx = frames.index(old)
                    frames[idx] = ref
                queue.append(ref)
            history.append((ref, list(frames), fault))
        return faults, history

    def _lru(self, refs: list[int], nf: int):
        frames: list[int | None] = [None] * nf
        used_order: list[int] = []
        faults = 0
        history = []
        for ref in refs:
            fault = ref not in [f for f in frames if f is not None]
            if fault:
                faults += 1
                if None in frames:
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    lru_page = next(p for p in used_order if p in frames)
                    idx = frames.index(lru_page)
                    frames[idx] = ref
            if ref in used_order:
                used_order.remove(ref)
            used_order.append(ref)
            history.append((ref, list(frames), fault))
        return faults, history

    def _optimal(self, refs: list[int], nf: int):
        frames: list[int | None] = [None] * nf
        faults = 0
        history = []
        for i, ref in enumerate(refs):
            fault = ref not in [f for f in frames if f is not None]
            if fault:
                faults += 1
                if None in frames:
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    future = refs[i+1:]
                    farthest = -1
                    replace_idx = 0
                    for fi, page in enumerate(frames):
                        if page not in future:
                            replace_idx = fi; break
                        next_use = future.index(page)
                        if next_use > farthest:
                            farthest = next_use; replace_idx = fi
                    frames[replace_idx] = ref
            history.append((ref, list(frames), fault))
        return faults, history

    def _clock(self, refs: list[int], nf: int):
        frames: list[int | None] = [None] * nf
        ref_bits = [0] * nf
        pointer  = 0
        faults   = 0
        history  = []
        for ref in refs:
            fault = ref not in [f for f in frames if f is not None]
            if fault:
                faults += 1
                while True:
                    if frames[pointer] is None:
                        frames[pointer] = ref
                        ref_bits[pointer] = 1
                        pointer = (pointer + 1) % nf
                        break
                    if ref_bits[pointer] == 0:
                        frames[pointer] = ref
                        ref_bits[pointer] = 1
                        pointer = (pointer + 1) % nf
                        break
                    ref_bits[pointer] = 0
                    pointer = (pointer + 1) % nf
            else:
                idx = frames.index(ref)
                ref_bits[idx] = 1
            history.append((ref, list(frames), fault))
        return faults, history

    # ── Buddy System ──────────────────────────────────────────────────────
    def buddy_show(self, console: Console, size: int) -> None:
        section_header(console, "Buddy System Allocator", f"Requested size: {size}")
        total = 1
        while total < size:
            total *= 2
        console.print(f"  [cyan]Allocating {size} units → block size = [bold]{total}[/bold] (next power of 2)[/cyan]")
        console.print()
        self._print_buddy_tree(console, total, size, 0)
        console.print()

    def _print_buddy_tree(self, console: Console, block: int, needed: int,
                          depth: int, prefix: str = "") -> None:
        indent = "  " + "  " * depth
        if block == 1 or block <= needed:
            style = "bold green" if block >= needed else "dim"
            console.print(f"{indent}[{style}]◉ Block({block})[/{style}] [green]← ALLOCATED[/green]" if block >= needed
                          else f"{indent}[dim]◎ Block({block})[/dim]")
            return
        half = block // 2
        console.print(f"{indent}[cyan]○ Block({block})[/cyan]")
        console.print(f"{indent}├── [left buddy]")
        self._print_buddy_tree(console, half, needed, depth + 1)
        console.print(f"{indent}└── [right buddy — free]")
        console.print(f"{indent}    [dim]◎ Block({half}) — free[/dim]")


def handle_mem(args: list[str], mem: MemoryManager, console: Console) -> None:
    if not args:
        console.print("[yellow]Usage: mem <init|alloc|free|show|pagefault|compare|buddy>[/yellow]")
        return
    sub = args[0]

    if sub == "init":
        params = _parse_flags(args[1:])
        total  = int(params.get("frames", 16))
        console.print(mem.init(total))

    elif sub == "alloc":
        if len(args) < 2:
            console.print("[yellow]Usage: mem alloc <name> [--pages=N] [--algo=firstfit|bestfit|worstfit][/yellow]")
            return
        name   = args[1]
        params = _parse_flags(args[2:])
        pages  = int(params.get("pages", 2))
        algo   = params.get("algo", "firstfit")
        console.print(mem.alloc(name, pages, algo))

    elif sub == "free":
        if len(args) < 2:
            console.print("[yellow]Usage: mem free <name>[/yellow]")
            return
        console.print(mem.free(args[1]))

    elif sub == "show":
        mem.show(console)

    elif sub == "pagefault":
        params = _parse_flags(args[1:])
        ref_raw = params.get("ref", "1,2,3,4,1,2,5,1,2,3,4,5")
        ref_str = [int(x) for x in ref_raw.split(",")]
        nf      = int(params.get("frames", 3))
        algo    = params.get("algo", "fifo")
        mem.page_fault_sim(console, ref_str, nf, algo)

    elif sub == "compare":
        params  = _parse_flags(args[1:])
        ref_raw = params.get("ref", "1,2,3,4,1,2,5,1,2,3,4,5")
        ref_str = [int(x) for x in ref_raw.split(",")]
        nf      = int(params.get("frames", 3))
        mem.compare_page_algos(console, ref_str, nf)

    elif sub == "buddy":
        params = _parse_flags(args[1:])
        size   = int(params.get("size", 6))
        mem.buddy_show(console, size)

    else:
        console.print(f"[red]Unknown mem subcommand: {sub}[/red]")


def _parse_flags(tokens: list[str]) -> dict[str, str]:
    result = {}
    for t in tokens:
        if t.startswith("--") and "=" in t:
            k, v = t[2:].split("=", 1)
            result[k] = v
    return result
