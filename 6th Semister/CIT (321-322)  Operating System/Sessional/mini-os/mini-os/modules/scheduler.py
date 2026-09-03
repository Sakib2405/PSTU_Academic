from __future__ import annotations
import copy
from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from ui.widgets import section_header, print_gantt, bar_chart
from ui.theme import get_process_style


@dataclass
class Process:
    name: str
    burst: int
    arrival: int = 0
    priority: int = 0
    remaining: int = field(init=False)

    def __post_init__(self):
        self.remaining = self.burst


@dataclass
class Result:
    name: str
    arrival: int
    burst: int
    start: int
    finish: int
    waiting: int
    turnaround: int
    response: int


class Scheduler:
    def __init__(self):
        self.processes: list[Process] = []

    def add(self, name: str, burst: int, arrival: int = 0, priority: int = 0) -> str:
        if any(p.name == name for p in self.processes):
            return f"[red]Process '{name}' already exists.[/red]"
        self.processes.append(Process(name, burst, arrival, priority))
        return f"[green]Added process [bold]{name}[/bold] (burst={burst}, arrival={arrival}, priority={priority})[/green]"

    def list_processes(self, console: Console) -> None:
        if not self.processes:
            console.print("  [yellow]No processes. Use: sched add <name> --burst=N[/yellow]")
            return
        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Process", style="bold bright_white")
        table.add_column("Burst", justify="center")
        table.add_column("Arrival", justify="center")
        table.add_column("Priority", justify="center")
        for p in self.processes:
            table.add_row(p.name, str(p.burst), str(p.arrival), str(p.priority))
        console.print(table)

    def clear(self) -> str:
        self.processes.clear()
        return "[green]Process list cleared.[/green]"

    def _print_results(self, console: Console, algo_name: str,
                       results: list[Result], timeline: list[tuple]) -> None:
        section_header(console, f"Scheduler — {algo_name}")
        print_gantt(console, timeline, timeline[-1][2] if timeline else 0, animate=True)

        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        for col in ["Process", "Arrival", "Burst", "Start", "Finish", "Waiting", "Turnaround", "Response"]:
            table.add_column(col, justify="center")

        total_wt = total_tat = total_rt = 0
        for r in results:
            style = get_process_style(list({x.name for x in results}).index(r.name))
            table.add_row(
                r.name, str(r.arrival), str(r.burst),
                str(r.start), str(r.finish),
                str(r.waiting), str(r.turnaround), str(r.response),
                style=style
            )
            total_wt  += r.waiting
            total_tat += r.turnaround
            total_rt  += r.response

        n = len(results)
        console.print(table)
        end_time = max(r.finish for r in results)
        busy     = sum(r.burst for r in results)
        cpu_util = (busy / end_time * 100) if end_time else 0
        throughput = n / end_time if end_time else 0

        stats = Table(box=box.SIMPLE, border_style="dim")
        stats.add_column("Metric", style="bold cyan")
        stats.add_column("Value",  style="bold white")
        stats.add_row("Avg Waiting Time",     f"{total_wt/n:.2f}")
        stats.add_row("Avg Turnaround Time",  f"{total_tat/n:.2f}")
        stats.add_row("Avg Response Time",    f"{total_rt/n:.2f}")
        stats.add_row("CPU Utilization",      f"{cpu_util:.1f}%")
        stats.add_row("Throughput",           f"{throughput:.3f} proc/unit")
        console.print(stats)

    # ── FCFS ──────────────────────────────────────────────────────────────
    def fcfs(self, console: Console) -> list[Result]:
        procs = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        results, timeline = [], []
        for p in procs:
            if time < p.arrival:
                timeline.append(("IDLE", time, p.arrival))
                time = p.arrival
            start = time
            time += p.burst
            wt  = start - p.arrival
            tat = time - p.arrival
            results.append(Result(p.name, p.arrival, p.burst, start, time, wt, tat, wt))
            timeline.append((p.name, start, time))
        self._print_results(console, "FCFS (First Come First Served)", results, timeline)
        return results

    # ── SJF non-preemptive ────────────────────────────────────────────────
    def sjf(self, console: Console) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        done, results, timeline = [], [], []
        time = 0
        while len(done) < len(procs):
            ready = [p for p in procs if p.arrival <= time and p.name not in done]
            if not ready:
                next_arr = min(p.arrival for p in procs if p.name not in done)
                timeline.append(("IDLE", time, next_arr))
                time = next_arr
                continue
            p = min(ready, key=lambda x: x.burst)
            start = time
            time += p.burst
            wt  = start - p.arrival
            tat = time - p.arrival
            results.append(Result(p.name, p.arrival, p.burst, start, time, wt, tat, wt))
            timeline.append((p.name, start, time))
            done.append(p.name)
        self._print_results(console, "SJF (Shortest Job First, Non-Preemptive)", results, timeline)
        return results

    # ── SRTF preemptive SJF ───────────────────────────────────────────────
    def srtf(self, console: Console) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        for p in procs:
            p.remaining = p.burst
        n = len(procs)
        time = 0
        done = 0
        start_time: dict[str, int | None] = {p.name: None for p in procs}
        finish_time: dict[str, int] = {}
        timeline: list[tuple] = []
        prev_name = None

        while done < n:
            ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
            if not ready:
                time += 1
                continue
            p = min(ready, key=lambda x: x.remaining)
            if start_time[p.name] is None:
                start_time[p.name] = time
            if prev_name != p.name:
                if timeline and timeline[-1][0] == p.name:
                    pass
                timeline.append((p.name, time, time + 1))
            else:
                last = timeline[-1]
                timeline[-1] = (last[0], last[1], last[2] + 1)
            p.remaining -= 1
            prev_name = p.name
            time += 1
            if p.remaining == 0:
                finish_time[p.name] = time
                done += 1

        results = []
        for p in procs:
            ft  = finish_time[p.name]
            st  = start_time[p.name]
            wt  = ft - p.arrival - p.burst
            tat = ft - p.arrival
            results.append(Result(p.name, p.arrival, p.burst, st, ft, wt, tat, st - p.arrival))
        self._print_results(console, "SRTF (Shortest Remaining Time First, Preemptive)", results, timeline)
        return results

    # ── Round Robin ───────────────────────────────────────────────────────
    def round_robin(self, console: Console, quantum: int = 2) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        for p in procs:
            p.remaining = p.burst
        n = len(procs)
        time = 0
        queue: list[Process] = []
        done_names: set[str] = set()
        start_time: dict[str, int | None] = {p.name: None for p in procs}
        finish_time: dict[str, int] = {}
        timeline: list[tuple] = []
        arrived = set()

        sorted_procs = sorted(procs, key=lambda p: p.arrival)
        idx = 0

        while len(done_names) < n:
            while idx < n and sorted_procs[idx].arrival <= time:
                if sorted_procs[idx].name not in arrived:
                    queue.append(sorted_procs[idx])
                    arrived.add(sorted_procs[idx].name)
                idx += 1

            if not queue:
                if idx < n:
                    time = sorted_procs[idx].arrival
                    continue
                break

            p = queue.pop(0)
            if start_time[p.name] is None:
                start_time[p.name] = time

            run = min(quantum, p.remaining)
            timeline.append((p.name, time, time + run))
            time += run
            p.remaining -= run

            while idx < n and sorted_procs[idx].arrival <= time:
                if sorted_procs[idx].name not in arrived:
                    queue.append(sorted_procs[idx])
                    arrived.add(sorted_procs[idx].name)
                idx += 1

            if p.remaining > 0:
                queue.append(p)
            else:
                finish_time[p.name] = time
                done_names.add(p.name)

        results = []
        for p in procs:
            ft  = finish_time.get(p.name, time)
            st  = start_time.get(p.name, p.arrival)
            wt  = ft - p.arrival - p.burst
            tat = ft - p.arrival
            results.append(Result(p.name, p.arrival, p.burst, st, ft, wt, tat, st - p.arrival))
        self._print_results(console, f"Round Robin (Quantum={quantum})", results, timeline)
        return results

    # ── Priority non-preemptive ────────────────────────────────────────────
    def priority(self, console: Console) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        done, results, timeline = [], [], []
        time = 0
        while len(done) < len(procs):
            ready = [p for p in procs if p.arrival <= time and p.name not in done]
            if not ready:
                next_arr = min(p.arrival for p in procs if p.name not in done)
                timeline.append(("IDLE", time, next_arr))
                time = next_arr
                continue
            p = min(ready, key=lambda x: x.priority)
            start = time
            time += p.burst
            wt  = start - p.arrival
            tat = time - p.arrival
            results.append(Result(p.name, p.arrival, p.burst, start, time, wt, tat, wt))
            timeline.append((p.name, start, time))
            done.append(p.name)
        self._print_results(console, "Priority Scheduling (Non-Preemptive, lower=higher)", results, timeline)
        return results

    # ── MLFQ (3 queues) ───────────────────────────────────────────────────
    def mlfq(self, console: Console, q1: int = 2, q2: int = 4) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        for p in procs:
            p.remaining = p.burst
        n = len(procs)
        queues: list[list[Process]] = [[], [], []]
        time = 0
        done_names: set[str] = set()
        start_time: dict[str, int | None] = {p.name: None for p in procs}
        finish_time: dict[str, int] = {}
        timeline: list[tuple] = []
        arrived: set[str] = set()
        quantums = [q1, q2, 0]

        sorted_procs = sorted(procs, key=lambda p: p.arrival)

        def enqueue_arrivals():
            for sp in sorted_procs:
                if sp.arrival <= time and sp.name not in arrived and sp.name not in done_names:
                    queues[0].append(sp)
                    arrived.add(sp.name)

        enqueue_arrivals()

        while len(done_names) < n:
            ran = False
            for qi, q in enumerate(queues):
                if not q:
                    continue
                p = q.pop(0)
                if start_time[p.name] is None:
                    start_time[p.name] = time

                if qi < 2:
                    run = min(quantums[qi], p.remaining)
                else:
                    run = p.remaining

                timeline.append((p.name, time, time + run))
                time += run
                p.remaining -= run
                enqueue_arrivals()

                if p.remaining > 0:
                    next_q = min(qi + 1, 2)
                    queues[next_q].append(p)
                else:
                    finish_time[p.name] = time
                    done_names.add(p.name)
                ran = True
                break

            if not ran:
                time += 1
                enqueue_arrivals()

        results = []
        for p in procs:
            ft  = finish_time.get(p.name, time)
            st  = start_time.get(p.name, p.arrival)
            wt  = ft - p.arrival - p.burst
            tat = ft - p.arrival
            results.append(Result(p.name, p.arrival, p.burst, st, ft, wt, tat, st - p.arrival))
        self._print_results(console, f"MLFQ (Q1={q1}, Q2={q2}, Q3=FCFS)", results, timeline)
        return results

    # ── Compare all ───────────────────────────────────────────────────────
    def compare(self, console: Console, quantum: int = 2) -> None:
        if not self.processes:
            console.print("[yellow]No processes to compare.[/yellow]")
            return

        section_header(console, "Algorithm Comparison", "All scheduling algorithms on same process set")

        algos = [
            ("FCFS",          lambda: self._run_silent_fcfs()),
            ("SJF",           lambda: self._run_silent_sjf()),
            ("SRTF",          lambda: self._run_silent_srtf()),
            (f"RR (Q={quantum})", lambda: self._run_silent_rr(quantum)),
            ("Priority",      lambda: self._run_silent_priority()),
            (f"MLFQ",         lambda: self._run_silent_mlfq()),
        ]

        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Algorithm", style="bold bright_cyan", min_width=14)
        table.add_column("Avg Wait",     justify="center")
        table.add_column("Avg TAT",      justify="center")
        table.add_column("Avg Response", justify="center")
        table.add_column("CPU Util%",    justify="center")
        table.add_column("Throughput",   justify="center")

        for name, fn in algos:
            res = fn()
            if not res:
                continue
            n  = len(res)
            aw = sum(r.waiting     for r in res) / n
            at = sum(r.turnaround  for r in res) / n
            ar = sum(r.response    for r in res) / n
            et = max(r.finish for r in res)
            bu = sum(r.burst  for r in res)
            cu = bu / et * 100 if et else 0
            tp = n / et if et else 0
            table.add_row(name, f"{aw:.2f}", f"{at:.2f}", f"{ar:.2f}",
                          f"{cu:.1f}%", f"{tp:.3f}")

        console.print(table)
        console.print()

    # ── Silent runners (for compare) ──────────────────────────────────────
    def _run_silent_fcfs(self) -> list[Result]:
        procs = sorted(self.processes, key=lambda p: p.arrival)
        time, results = 0, []
        for p in procs:
            if time < p.arrival:
                time = p.arrival
            start = time
            time += p.burst
            results.append(Result(p.name, p.arrival, p.burst, start, time,
                                  start - p.arrival, time - p.arrival, start - p.arrival))
        return results

    def _run_silent_sjf(self) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        done, results, time = [], [], 0
        while len(done) < len(procs):
            ready = [p for p in procs if p.arrival <= time and p.name not in done]
            if not ready:
                time = min(p.arrival for p in procs if p.name not in done)
                continue
            p = min(ready, key=lambda x: x.burst)
            start = time; time += p.burst
            results.append(Result(p.name, p.arrival, p.burst, start, time,
                                  start - p.arrival, time - p.arrival, start - p.arrival))
            done.append(p.name)
        return results

    def _run_silent_srtf(self) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        for p in procs:
            p.remaining = p.burst
        n = len(procs)
        time = done = 0
        start_time: dict[str, int | None] = {p.name: None for p in procs}
        finish_time: dict[str, int] = {}
        while done < n:
            ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
            if not ready:
                time += 1; continue
            p = min(ready, key=lambda x: x.remaining)
            if start_time[p.name] is None:
                start_time[p.name] = time
            p.remaining -= 1; time += 1
            if p.remaining == 0:
                finish_time[p.name] = time; done += 1
        results = []
        for p in procs:
            ft = finish_time[p.name]; st = start_time[p.name]
            results.append(Result(p.name, p.arrival, p.burst, st, ft,
                                  ft - p.arrival - p.burst, ft - p.arrival, st - p.arrival))
        return results

    def _run_silent_rr(self, quantum: int) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        for p in procs:
            p.remaining = p.burst
        n = len(procs); time = 0; queue = []
        done_names: set[str] = set()
        start_time: dict[str, int | None] = {p.name: None for p in procs}
        finish_time: dict[str, int] = {}
        arrived: set[str] = set()
        sorted_procs = sorted(procs, key=lambda p: p.arrival)
        idx = 0
        while len(done_names) < n:
            while idx < n and sorted_procs[idx].arrival <= time:
                if sorted_procs[idx].name not in arrived:
                    queue.append(sorted_procs[idx]); arrived.add(sorted_procs[idx].name)
                idx += 1
            if not queue:
                if idx < n: time = sorted_procs[idx].arrival
                continue
            p = queue.pop(0)
            if start_time[p.name] is None: start_time[p.name] = time
            run = min(quantum, p.remaining); time += run; p.remaining -= run
            while idx < n and sorted_procs[idx].arrival <= time:
                if sorted_procs[idx].name not in arrived:
                    queue.append(sorted_procs[idx]); arrived.add(sorted_procs[idx].name)
                idx += 1
            if p.remaining > 0: queue.append(p)
            else: finish_time[p.name] = time; done_names.add(p.name)
        results = []
        for p in procs:
            ft = finish_time.get(p.name, time); st = start_time.get(p.name, p.arrival)
            results.append(Result(p.name, p.arrival, p.burst, st, ft,
                                  ft - p.arrival - p.burst, ft - p.arrival, st - p.arrival))
        return results

    def _run_silent_priority(self) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        done, results, time = [], [], 0
        while len(done) < len(procs):
            ready = [p for p in procs if p.arrival <= time and p.name not in done]
            if not ready:
                time = min(p.arrival for p in procs if p.name not in done)
                continue
            p = min(ready, key=lambda x: x.priority)
            start = time; time += p.burst
            results.append(Result(p.name, p.arrival, p.burst, start, time,
                                  start - p.arrival, time - p.arrival, start - p.arrival))
            done.append(p.name)
        return results

    def _run_silent_mlfq(self) -> list[Result]:
        procs = [copy.copy(p) for p in self.processes]
        for p in procs:
            p.remaining = p.burst
        n = len(procs); queues: list[list[Process]] = [[], [], []]
        time = 0; done_names: set[str] = set()
        start_time: dict[str, int | None] = {p.name: None for p in procs}
        finish_time: dict[str, int] = {}
        arrived: set[str] = set()
        quantums = [2, 4, 0]
        sorted_procs = sorted(procs, key=lambda p: p.arrival)
        def enq():
            for sp in sorted_procs:
                if sp.arrival <= time and sp.name not in arrived and sp.name not in done_names:
                    queues[0].append(sp); arrived.add(sp.name)
        enq()
        while len(done_names) < n:
            ran = False
            for qi, q in enumerate(queues):
                if not q: continue
                p = q.pop(0)
                if start_time[p.name] is None: start_time[p.name] = time
                run = min(quantums[qi], p.remaining) if qi < 2 else p.remaining
                time += run; p.remaining -= run; enq()
                if p.remaining > 0: queues[min(qi+1,2)].append(p)
                else: finish_time[p.name] = time; done_names.add(p.name)
                ran = True; break
            if not ran: time += 1; enq()
        results = []
        for p in procs:
            ft = finish_time.get(p.name, time); st = start_time.get(p.name, p.arrival)
            results.append(Result(p.name, p.arrival, p.burst, st, ft,
                                  ft - p.arrival - p.burst, ft - p.arrival, st - p.arrival))
        return results


def handle_sched(args: list[str], sched: Scheduler, console: Console) -> None:
    if not args:
        console.print("[yellow]Usage: sched <add|list|run|compare|clear>[/yellow]")
        return

    sub = args[0]

    if sub == "add":
        if len(args) < 2:
            console.print("[yellow]Usage: sched add <name> [--burst=N] [--arrival=N] [--priority=N][/yellow]")
            return
        name = args[1]
        params = _parse_flags(args[2:])
        burst    = int(params.get("burst",    4))
        arrival  = int(params.get("arrival",  0))
        priority = int(params.get("priority", 0))
        console.print(sched.add(name, burst, arrival, priority))

    elif sub == "list":
        sched.list_processes(console)

    elif sub == "clear":
        console.print(sched.clear())

    elif sub == "run":
        if not sched.processes:
            console.print("[yellow]No processes. Add with: sched add <name> --burst=N[/yellow]")
            return
        params = _parse_flags(args[1:])
        algo   = params.get("algo", "fcfs").lower()
        quantum = int(params.get("quantum", 2))
        if   algo == "fcfs":     sched.fcfs(console)
        elif algo == "sjf":      sched.sjf(console)
        elif algo == "srtf":     sched.srtf(console)
        elif algo == "rr":       sched.round_robin(console, quantum)
        elif algo == "priority": sched.priority(console)
        elif algo == "mlfq":     sched.mlfq(console)
        else:
            console.print(f"[red]Unknown algorithm: {algo}. Options: fcfs|sjf|srtf|rr|priority|mlfq[/red]")

    elif sub == "compare":
        params  = _parse_flags(args[1:])
        quantum = int(params.get("quantum", 2))
        sched.compare(console, quantum)

    else:
        console.print(f"[red]Unknown sched subcommand: {sub}[/red]")


def _parse_flags(tokens: list[str]) -> dict[str, str]:
    result = {}
    for t in tokens:
        if t.startswith("--") and "=" in t:
            k, v = t[2:].split("=", 1)
            result[k] = v
    return result
