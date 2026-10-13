from __future__ import annotations
import time
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from ui.widgets import section_header


class DiskScheduler:
    def __init__(self, total_tracks: int = 200, head: int = 53):
        self.total  = total_tracks
        self.head   = head
        self.queue: list[int] = []

    def init(self, total: int, head: int) -> str:
        self.total = total
        self.head  = head
        self.queue = []
        return f"[green]Disk initialized: {total} tracks, head at {head}[/green]"

    def add(self, tracks: list[int]) -> str:
        self.queue.extend(tracks)
        return f"[green]Added tracks: {tracks}[/green]"

    def clear(self) -> str:
        self.queue.clear()
        return "[green]Disk queue cleared.[/green]"

    def run(self, console: Console, algo: str) -> None:
        if not self.queue:
            console.print("[yellow]No track requests. Use: disk add <track> [track ...][/yellow]")
            return
        algo = algo.lower()
        if   algo == "fcfs":   seq, dist = self._fcfs()
        elif algo == "sstf":   seq, dist = self._sstf()
        elif algo == "scan":   seq, dist = self._scan()
        elif algo == "cscan":  seq, dist = self._cscan()
        elif algo == "look":   seq, dist = self._look()
        elif algo == "clook":  seq, dist = self._clook()
        else:
            console.print(f"[red]Unknown algo: {algo}. Use fcfs|sstf|scan|cscan|look|clook[/red]")
            return
        self._display(console, algo.upper(), seq, dist)

    def compare(self, console: Console) -> None:
        if not self.queue:
            console.print("[yellow]No track requests.[/yellow]")
            return
        section_header(console, "Disk Scheduling Comparison")
        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Algorithm", style="bold bright_cyan")
        table.add_column("Seek Sequence", style="dim white")
        table.add_column("Total Seek", justify="center")
        table.add_column("Avg Seek",   justify="center")

        algos = [
            ("FCFS",   self._fcfs),
            ("SSTF",   self._sstf),
            ("SCAN",   self._scan),
            ("C-SCAN", self._cscan),
            ("LOOK",   self._look),
            ("C-LOOK", self._clook),
        ]
        for name, fn in algos:
            seq, dist = fn()
            avg = dist / len(seq) if seq else 0
            table.add_row(name, " → ".join(str(t) for t in seq),
                          str(dist), f"{avg:.1f}")
        console.print(table)
        console.print()

    def _display(self, console: Console, algo: str,
                 seq: list[int], dist: int) -> None:
        section_header(console, f"Disk Scheduling — {algo}",
                       f"Initial head: {self.head} | Tracks: {self.total}")

        console.print("  [bold cyan]Seek Sequence:[/bold cyan]")
        self._animate_head(console, seq)

        console.print()
        table = Table(box=box.SIMPLE, border_style="dim")
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value",  style="bold white")
        table.add_row("Seek Sequence",    " → ".join(str(t) for t in seq))
        table.add_row("Total Seek Distance", str(dist))
        table.add_row("Avg Seek/Request",    f"{dist/len(seq):.1f}" if seq else "0")
        console.print(table)
        console.print()

    def _animate_head(self, console: Console, seq: list[int]) -> None:
        WIDTH = 60
        prev = self.head
        for track in seq:
            pos = int(track / self.total * WIDTH)
            bar = [" "] * WIDTH
            bar[pos] = "▲"
            bar_str  = "".join(bar)
            move     = abs(track - prev)
            direction = "→" if track > prev else "←"
            prev_pos = int(prev / self.total * WIDTH)

            if track > prev:
                for i in range(prev_pos, pos):
                    bar[i] = "─"
            else:
                for i in range(pos, prev_pos):
                    bar[i] = "─"
            bar[pos] = "▲"
            bar_str = "".join(bar)

            row = Text()
            row.append(f"  [{track:>3}] ", style="bold bright_cyan")
            row.append("│", style="dim")
            for ch in bar_str:
                if ch == "▲":
                    row.append(ch, style="bold bright_green")
                elif ch == "─":
                    row.append(ch, style="bright_yellow")
                else:
                    row.append(ch, style="dim")
            row.append("│", style="dim")
            row.append(f"  {direction} {move} tracks", style="dim yellow")
            console.print(row)
            time.sleep(0.08)
            prev = track

        console.print(f"  {'0':^4}{'':^{WIDTH//2}}{'':^{WIDTH//2}}{self.total}")

    # ── Algorithms ─────────────────────────────────────────────────────────
    def _fcfs(self) -> tuple[list[int], int]:
        seq  = list(self.queue)
        dist = sum(abs(seq[i] - seq[i-1]) for i in range(1, len(seq)))
        dist += abs(self.head - seq[0]) if seq else 0
        return seq, dist

    def _sstf(self) -> tuple[list[int], int]:
        remaining = list(self.queue)
        head, seq, dist = self.head, [], 0
        while remaining:
            closest = min(remaining, key=lambda t: abs(t - head))
            dist += abs(closest - head)
            head  = closest
            seq.append(closest)
            remaining.remove(closest)
        return seq, dist

    def _scan(self) -> tuple[list[int], int]:
        requests = sorted(self.queue)
        left  = [r for r in requests if r <= self.head]
        right = [r for r in requests if r  > self.head]
        seq   = list(reversed(left)) + right
        head  = self.head
        dist  = 0
        for t in seq:
            dist += abs(t - head)
            head  = t
        return seq, dist

    def _cscan(self) -> tuple[list[int], int]:
        requests = sorted(self.queue)
        right = [r for r in requests if r >= self.head]
        left  = [r for r in requests if r <  self.head]
        seq   = right + left
        head  = self.head
        dist  = 0
        if right:
            dist += abs(right[-1] - head)
            dist += self.total - right[-1]
            if left:
                dist += left[-1]
        for t in seq:
            pass
        head = self.head
        dist = 0
        for t in seq:
            dist += abs(t - head)
            head = t
        return seq, dist

    def _look(self) -> tuple[list[int], int]:
        requests = sorted(self.queue)
        left  = [r for r in requests if r <= self.head]
        right = [r for r in requests if r  > self.head]
        seq   = list(reversed(left)) + right
        head  = self.head
        dist  = 0
        for t in seq:
            dist += abs(t - head)
            head  = t
        return seq, dist

    def _clook(self) -> tuple[list[int], int]:
        requests = sorted(self.queue)
        right = [r for r in requests if r >= self.head]
        left  = [r for r in requests if r <  self.head]
        seq   = right + left
        head  = self.head
        dist  = 0
        for t in seq:
            dist += abs(t - head)
            head  = t
        return seq, dist


def handle_disk(args: list[str], disk: DiskScheduler, console: Console) -> None:
    if not args:
        console.print("[yellow]Usage: disk <init|add|run|compare|clear>[/yellow]")
        return
    sub = args[0]

    if sub == "init":
        params = _parse_flags(args[1:])
        total  = int(params.get("tracks", 200))
        head   = int(params.get("head",   53))
        console.print(disk.init(total, head))

    elif sub == "add":
        tracks = []
        for a in args[1:]:
            if not a.startswith("--"):
                try:
                    tracks.append(int(a))
                except ValueError:
                    pass
        if tracks:
            console.print(disk.add(tracks))
        else:
            console.print("[yellow]Usage: disk add <track1> [track2 ...][/yellow]")

    elif sub == "run":
        params = _parse_flags(args[1:])
        algo   = params.get("algo", "fcfs")
        disk.run(console, algo)

    elif sub == "compare":
        disk.compare(console)

    elif sub == "clear":
        console.print(disk.clear())

    else:
        console.print(f"[red]Unknown disk subcommand: {sub}[/red]")


def _parse_flags(tokens: list[str]) -> dict[str, str]:
    result = {}
    for t in tokens:
        if t.startswith("--") and "=" in t:
            k, v = t[2:].split("=", 1)
            result[k] = v
    return result
