from __future__ import annotations
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box
from ui.widgets import section_header


class DeadlockDetector:
    def __init__(self):
        self.processes:  list[str] = []
        self.resources:  list[str] = []
        self.allocation: dict[str, dict[str, int]] = {}
        self.maximum:    dict[str, dict[str, int]] = {}
        self.available:  dict[str, int] = {}

    def init(self, processes: list[str], resources: list[str]) -> str:
        self.processes = processes
        self.resources = resources
        self.allocation = {p: {r: 0 for r in resources} for p in processes}
        self.maximum    = {p: {r: 0 for r in resources} for p in processes}
        self.available  = {r: 0 for r in resources}
        return (f"[green]Initialized: {len(processes)} processes "
                f"({', '.join(processes)}), "
                f"{len(resources)} resources ({', '.join(resources)})[/green]")

    def set_max(self, process: str, values: list[int]) -> str:
        if process not in self.processes:
            return f"[red]Process '{process}' not found.[/red]"
        for i, r in enumerate(self.resources):
            self.maximum[process][r] = values[i] if i < len(values) else 0
        return f"[green]Max set for {process}: {dict(zip(self.resources, values))}[/green]"

    def set_alloc(self, process: str, values: list[int]) -> str:
        if process not in self.processes:
            return f"[red]Process '{process}' not found.[/red]"
        for i, r in enumerate(self.resources):
            self.allocation[process][r] = values[i] if i < len(values) else 0
        return f"[green]Allocation set for {process}: {dict(zip(self.resources, values))}[/green]"

    def set_available(self, values: list[int]) -> str:
        for i, r in enumerate(self.resources):
            self.available[r] = values[i] if i < len(values) else 0
        return f"[green]Available: {self.available}[/green]"

    def request(self, console: Console, process: str, values: list[int]) -> None:
        if process not in self.processes:
            console.print(f"[red]Process '{process}' not found.[/red]")
            return
        req = dict(zip(self.resources, values))
        need = {r: self.maximum[process][r] - self.allocation[process][r]
                for r in self.resources}

        console.print(f"\n  [cyan]Request by {process}: {req}[/cyan]")
        for r in self.resources:
            if req.get(r, 0) > need[r]:
                console.print(f"  [red]✗ Request exceeds maximum need for {r}! Denied.[/red]")
                return
            if req.get(r, 0) > self.available.get(r, 0):
                console.print(f"  [yellow]⏳ {process} must wait — {r} not available.[/yellow]")
                return

        for r in self.resources:
            self.available[r]           -= req.get(r, 0)
            self.allocation[process][r] += req.get(r, 0)

        console.print(f"  [green]✓ Resources tentatively granted to {process}.[/green]")
        self.check(console)

    def _need(self) -> dict[str, dict[str, int]]:
        return {
            p: {r: self.maximum[p][r] - self.allocation[p][r] for r in self.resources}
            for p in self.processes
        }

    def show_matrices(self, console: Console) -> None:
        section_header(console, "Banker's Algorithm — State Matrices")
        need = self._need()

        for title, data in [("Allocation", self.allocation),
                             ("Maximum",    self.maximum),
                             ("Need",       need)]:
            table = Table(title=title, box=box.ROUNDED, border_style="bright_cyan",
                          header_style="bold white on dark_blue", show_lines=True)
            table.add_column("Process", style="bold bright_cyan")
            for r in self.resources:
                table.add_column(r, justify="center")
            for p in self.processes:
                table.add_row(p, *[str(data[p][r]) for r in self.resources])
            console.print(table)

        avail_table = Table(title="Available", box=box.ROUNDED,
                            border_style="bright_cyan",
                            header_style="bold white on dark_blue")
        for r in self.resources:
            avail_table.add_column(r, justify="center")
        avail_table.add_row(*[str(self.available[r]) for r in self.resources])
        console.print(avail_table)
        console.print()

    def check(self, console: Console) -> None:
        if not self.processes:
            console.print("[yellow]No processes initialized. Use: deadlock init[/yellow]")
            return
        section_header(console, "Banker's Algorithm — Safety Check")
        self.show_matrices(console)

        need      = self._need()
        work      = dict(self.available)
        finish    = {p: False for p in self.processes}
        safe_seq  = []
        steps     = []

        max_iter = len(self.processes) * 2
        for _ in range(max_iter):
            found = False
            for p in self.processes:
                if not finish[p]:
                    can_run = all(need[p][r] <= work[r] for r in self.resources)
                    if can_run:
                        step_info = {
                            "process": p,
                            "need":    {r: need[p][r] for r in self.resources},
                            "work_before": dict(work),
                        }
                        for r in self.resources:
                            work[r] += self.allocation[p][r]
                        finish[p] = True
                        safe_seq.append(p)
                        step_info["work_after"] = dict(work)
                        steps.append(step_info)
                        found = True
                        break
            if not found:
                break

        if all(finish.values()):
            console.print(f"  [bold bright_green]✓ SAFE STATE DETECTED[/bold bright_green]\n")
            console.print(f"  [bold]Safe Sequence:[/bold] ", end="")
            for i, p in enumerate(safe_seq):
                style = "bold bright_green"
                console.print(f"[{style}]{p}[/{style}]", end="")
                if i < len(safe_seq) - 1:
                    console.print(" → ", end="")
            console.print("\n")

            step_table = Table(box=box.ROUNDED, border_style="bright_cyan",
                               header_style="bold white on dark_blue", show_lines=True,
                               title="Safety Algorithm Steps")
            step_table.add_column("Step", justify="center")
            step_table.add_column("Process", style="bold bright_cyan")
            step_table.add_column("Need", justify="center")
            step_table.add_column("Work Before", justify="center")
            step_table.add_column("Work After",  justify="center")
            for i, s in enumerate(steps):
                need_str  = str(list(s["need"].values()))
                wb_str    = str(list(s["work_before"].values()))
                wa_str    = str(list(s["work_after"].values()))
                step_table.add_row(str(i+1), s["process"], need_str, wb_str, wa_str)
            console.print(step_table)
        else:
            deadlocked = [p for p, f in finish.items() if not f]
            console.print(f"  [bold bright_red]✗ UNSAFE STATE — DEADLOCK DETECTED![/bold bright_red]\n")
            console.print(f"  [red]Deadlocked processes: {', '.join(deadlocked)}[/red]")
            console.print()
            self._suggest_recovery(console, deadlocked)

        console.print()

    def _suggest_recovery(self, console: Console, deadlocked: list[str]) -> None:
        console.print("  [bold yellow]── Recovery Options ──────────────────────────────[/bold yellow]")
        console.print("  [yellow]Option 1: Process Termination[/yellow]")
        for p in deadlocked:
            freed = self.allocation[p]
            console.print(f"    Kill [bold]{p}[/bold] → frees {freed}")
        console.print()
        console.print("  [yellow]Option 2: Resource Preemption[/yellow]")
        for p in deadlocked:
            console.print(f"    Preempt resources from [bold]{p}[/bold] and roll back its state")
        console.print()
        best = min(deadlocked,
                   key=lambda p: sum(self.allocation[p].values()))
        console.print(f"  [bold green]Recommendation:[/bold green] Terminate [bold]{best}[/bold] "
                      f"(lowest resource hold) to break deadlock.")
        console.print()

    def rag(self, console: Console) -> None:
        section_header(console, "Resource Allocation Graph (RAG)")
        console.print("  [dim]Arrows: P→R = request, R→P = assignment[/dim]\n")

        for p in self.processes:
            need = {r: self.maximum[p][r] - self.allocation[p][r]
                    for r in self.resources}
            requests  = [r for r in self.resources if need[r] > 0]
            holds     = [r for r in self.resources if self.allocation[p][r] > 0]

            row = Text()
            row.append(f"  [{p}]", style="bold bright_cyan")
            if holds:
                row.append(" ← holds ← ", style="dim")
                row.append(", ".join(f"[{r}]" for r in holds), style="bold bright_green")
            if requests:
                row.append("  requesting → ", style="dim yellow")
                row.append(", ".join(f"[{r}]" for r in requests), style="bold yellow")
            console.print(row)

        console.print()
        console.print("  [bold cyan]Resources:[/bold cyan]")
        for r in self.resources:
            holders = [p for p in self.processes if self.allocation[p][r] > 0]
            avail   = self.available.get(r, 0)
            row = Text(f"  [{r}]", style="bold bright_green")
            row.append(f" (avail={avail})", style="dim")
            if holders:
                row.append(" → assigned to: ", style="dim")
                row.append(", ".join(holders), style="bold bright_cyan")
            console.print(row)
        console.print()

    def recover(self, console: Console) -> None:
        section_header(console, "Deadlock Recovery")
        need   = self._need()
        work   = dict(self.available)
        finish = {p: False for p in self.processes}
        for _ in range(len(self.processes) * 2):
            for p in self.processes:
                if not finish[p] and all(need[p][r] <= work[r] for r in self.resources):
                    for r in self.resources:
                        work[r] += self.allocation[p][r]
                    finish[p] = True
        deadlocked = [p for p, f in finish.items() if not f]
        if not deadlocked:
            console.print("  [green]No deadlock detected. System is in a safe state.[/green]")
            return
        self._suggest_recovery(console, deadlocked)


def handle_deadlock(args: list[str], dl: DeadlockDetector,
                    console: Console) -> None:
    if not args:
        console.print("[yellow]Usage: deadlock <init|max|alloc|available|request|check|rag|recover>[/yellow]")
        return
    sub = args[0]

    if sub == "init":
        params = _parse_flags(args[1:])
        procs  = params.get("processes", "P0,P1,P2").split(",")
        res    = params.get("resources", "R0,R1,R2").split(",")
        console.print(dl.init(procs, res))

    elif sub == "max":
        if len(args) < 2:
            console.print("[yellow]Usage: deadlock max <process> <v1> <v2> ...[/yellow]")
            return
        p = args[1]
        vals = [int(x) for x in args[2:] if not x.startswith("--")]
        console.print(dl.set_max(p, vals))

    elif sub == "alloc":
        if len(args) < 2:
            console.print("[yellow]Usage: deadlock alloc <process> <v1> <v2> ...[/yellow]")
            return
        p = args[1]
        vals = [int(x) for x in args[2:] if not x.startswith("--")]
        console.print(dl.set_alloc(p, vals))

    elif sub == "available":
        vals = [int(x) for x in args[1:] if not x.startswith("--")]
        console.print(dl.set_available(vals))

    elif sub == "request":
        if len(args) < 2:
            console.print("[yellow]Usage: deadlock request <process> <v1> <v2> ...[/yellow]")
            return
        p = args[1]
        vals = [int(x) for x in args[2:] if not x.startswith("--")]
        dl.request(console, p, vals)

    elif sub == "check":
        dl.check(console)

    elif sub == "rag":
        dl.rag(console)

    elif sub == "recover":
        dl.recover(console)

    elif sub == "show":
        dl.show_matrices(console)

    else:
        console.print(f"[red]Unknown deadlock subcommand: {sub}[/red]")


def _parse_flags(tokens: list[str]) -> dict[str, str]:
    result = {}
    for t in tokens:
        if t.startswith("--") and "=" in t:
            k, v = t[2:].split("=", 1)
            result[k] = v
    return result
