from __future__ import annotations
import random
import time
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich import box
from ui.widgets import section_header


# ── Dining Philosophers ────────────────────────────────────────────────────
STATES = ["Thinking", "Hungry", "Eating"]
STATE_STYLE = {
    "Thinking": "dim cyan",
    "Hungry":   "bold yellow",
    "Eating":   "bold green",
}

def dining_philosophers(console: Console, n: int = 5, steps: int = 20,
                        animate: bool = True) -> None:
    section_header(console, "Dining Philosophers Problem", f"{n} philosophers")
    forks  = [False] * n
    states = ["Thinking"] * n

    def can_eat(i: int) -> bool:
        left, right = i, (i + 1) % n
        return states[i] == "Hungry" and not forks[left] and not forks[right]

    def pick_up(i: int) -> None:
        forks[i] = True
        forks[(i + 1) % n] = True
        states[i] = "Eating"

    def put_down(i: int) -> None:
        forks[i] = False
        forks[(i + 1) % n] = False
        states[i] = "Thinking"

    def render() -> Table:
        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True,
                      title=f"Step {step}/{steps}")
        table.add_column("Philosopher", style="bold")
        table.add_column("State",       justify="center")
        table.add_column("Left Fork",   justify="center")
        table.add_column("Right Fork",  justify="center")
        for i in range(n):
            left_fork  = "🍴 HELD" if forks[i] and states[i] == "Eating" else ("🍴 USED" if forks[i] else "○ free")
            right_fork = ("🍴 HELD" if forks[(i+1)%n] and states[i] == "Eating"
                          else ("🍴 USED" if forks[(i+1)%n] else "○ free"))
            state_str  = states[i]
            style      = STATE_STYLE.get(states[i], "white")
            table.add_row(
                f"P{i} (Phil {i})",
                Text(state_str, style=style),
                left_fork, right_fork
            )
        return table

    for step in range(1, steps + 1):
        i = random.randint(0, n - 1)
        if states[i] == "Thinking":
            states[i] = "Hungry"
        elif states[i] == "Hungry":
            if can_eat(i):
                pick_up(i)
        elif states[i] == "Eating":
            put_down(i)

        if animate:
            console.clear()
            console.print()
            console.print(render())
            fork_str = "  Forks: " + "  ".join(
                f"F{j}:[bold green]HELD[/bold green]" if forks[j] else f"F{j}:[dim]free[/dim]"
                for j in range(n)
            )
            console.print(fork_str)
            time.sleep(0.35)
        else:
            console.print(render())

    console.print()
    console.print("  [green]Simulation complete. Press Enter to continue.[/green]")
    input()


# ── Producer-Consumer ──────────────────────────────────────────────────────
def producer_consumer(console: Console, buffer_size: int = 5,
                      producers: int = 2, consumers: int = 2,
                      steps: int = 20) -> None:
    section_header(console, "Producer-Consumer Problem",
                   f"Buffer={buffer_size}, Producers={producers}, Consumers={consumers}")

    buffer: list[int | None] = [None] * buffer_size
    item_counter = [0]
    log_entries: list[str] = []
    mutex  = True
    empty  = buffer_size
    full   = 0

    def render_buffer() -> Text:
        t = Text("  Buffer: [")
        for slot in buffer:
            if slot is None:
                t.append("  _ ", style="dim white on grey19")
            else:
                t.append(f" {slot:>2} ", style="bold white on blue")
        t.append("]")
        t.append(f"  empty={empty}  full={full}  ", style="dim")
        return t

    for step in range(1, steps + 1):
        action = random.choice(["produce"] * producers + ["consume"] * consumers)
        actor_id = random.randint(0, producers - 1 if action == "produce" else consumers - 1)
        actor = f"Producer-{actor_id}" if action == "produce" else f"Consumer-{actor_id}"

        if action == "produce":
            if empty > 0:
                idx = buffer.index(None)
                item_counter[0] += 1
                buffer[idx] = item_counter[0]
                empty -= 1
                full  += 1
                log_entries.append(
                    f"  [bold green]Step {step:>2}[/bold green]  {actor:<14} PRODUCED item=[bold]{item_counter[0]}[/bold] → slot {idx}"
                )
            else:
                log_entries.append(
                    f"  [bold yellow]Step {step:>2}[/bold yellow]  {actor:<14} [yellow]WAITING (buffer full)[/yellow]"
                )
        else:
            filled_slots = [i for i, s in enumerate(buffer) if s is not None]
            if filled_slots:
                idx  = filled_slots[0]
                item = buffer[idx]
                buffer[idx] = None
                empty += 1
                full  -= 1
                log_entries.append(
                    f"  [bold cyan]Step {step:>2}[/bold cyan]  {actor:<14} CONSUMED item=[bold]{item}[/bold] from slot {idx}"
                )
            else:
                log_entries.append(
                    f"  [bold yellow]Step {step:>2}[/bold yellow]  {actor:<14} [yellow]WAITING (buffer empty)[/yellow]"
                )

        console.print(render_buffer())
        console.print(log_entries[-1])
        time.sleep(0.15)

    console.print()


# ── Reader-Writer ──────────────────────────────────────────────────────────
def reader_writer(console: Console, readers: int = 3,
                  writers: int = 2, steps: int = 15) -> None:
    section_header(console, "Reader-Writer Problem",
                   f"Readers={readers}, Writers={writers}")

    reader_count = [0]
    write_lock   = [False]
    shared_data  = ["Initial data v0"]
    version      = [0]

    for step in range(1, steps + 1):
        action = random.choice(["read"] * readers + ["write"] * writers)
        actor_id = random.randint(0, (readers if action == "read" else writers) - 1)
        actor = f"Reader-{actor_id}" if action == "read" else f"Writer-{actor_id}"

        if action == "read":
            if not write_lock[0]:
                reader_count[0] += 1
                status = f"[green]READING[/green] data: '{shared_data[0]}'"
                time.sleep(0.08)
                reader_count[0] -= 1
            else:
                status = "[yellow]WAITING (write in progress)[/yellow]"
        else:
            if not write_lock[0] and reader_count[0] == 0:
                write_lock[0] = True
                version[0] += 1
                shared_data[0] = f"Updated data v{version[0]}"
                status = f"[bold magenta]WRITING[/bold magenta] → '{shared_data[0]}'"
                time.sleep(0.1)
                write_lock[0] = False
            else:
                status = "[yellow]WAITING (readers active or another writer)[/yellow]"

        row = Text(f"  Step {step:>2}  {actor:<12}  ")
        row.append(status)
        row.append(f"  [dim]readers={reader_count[0]}  lock={write_lock[0]}[/dim]")
        console.print(row)
        time.sleep(0.12)

    console.print()


# ── Semaphore Demo ─────────────────────────────────────────────────────────
def semaphore_demo(console: Console, initial: int = 1, steps: int = 10) -> None:
    section_header(console, "Semaphore Demo", f"Initial value: {initial}")
    sem = [initial]
    processes = [f"P{i}" for i in range(4)]

    table = Table(box=box.ROUNDED, border_style="bright_cyan",
                  header_style="bold white on dark_blue", show_lines=True)
    table.add_column("Step", justify="center")
    table.add_column("Process", justify="center")
    table.add_column("Operation", justify="center")
    table.add_column("Sem Value", justify="center")
    table.add_column("Result", justify="center")

    for step in range(1, steps + 1):
        p   = random.choice(processes)
        op  = random.choice(["wait(P)", "signal(V)"])
        before = sem[0]
        if op == "wait(P)":
            if sem[0] > 0:
                sem[0] -= 1
                result = Text("✓ Entered CS", style="bold green")
            else:
                result = Text("⏳ Blocked", style="bold yellow")
        else:
            sem[0] += 1
            result = Text("✓ Released", style="bold cyan")

        table.add_row(
            str(step), p, op,
            Text(str(sem[0]), style="bold bright_white"),
            result
        )
        time.sleep(0.05)

    console.print(table)
    console.print()


def handle_sync(args: list[str], console: Console) -> None:
    if not args:
        console.print("[yellow]Usage: sync <dining|producer|reader|semaphore>[/yellow]")
        return
    sub = args[0]

    def get_param(key, default):
        for a in args[1:]:
            if a.startswith(f"--{key}="):
                return int(a.split("=", 1)[1])
        return default

    if sub == "dining":
        n       = get_param("philosophers", 5)
        steps   = get_param("steps", 20)
        animate = "--animate" in args
        dining_philosophers(console, n, steps, animate)

    elif sub == "producer":
        buf  = get_param("buffers",   5)
        prod = get_param("producers", 2)
        cons = get_param("consumers", 2)
        steps = get_param("steps",   20)
        producer_consumer(console, buf, prod, cons, steps)

    elif sub == "reader":
        r     = get_param("readers", 3)
        w     = get_param("writers", 2)
        steps = get_param("steps",  15)
        reader_writer(console, r, w, steps)

    elif sub == "semaphore":
        initial = get_param("initial", 1)
        steps   = get_param("steps",  10)
        semaphore_demo(console, initial, steps)

    else:
        console.print(f"[red]Unknown sync subcommand: {sub}[/red]")
