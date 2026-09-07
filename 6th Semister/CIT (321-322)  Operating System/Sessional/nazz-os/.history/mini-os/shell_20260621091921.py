from __future__ import annotations
import subprocess
import shutil
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box

from modules.scheduler  import Scheduler,        handle_sched
from modules.memory     import MemoryManager,    handle_mem
from modules.filesystem import VirtualFS,        handle_fs
from modules.disk       import DiskScheduler,    handle_disk
from modules.deadlock   import DeadlockDetector, handle_deadlock
from modules.sync       import handle_sync
from modules.dashboard  import run_dashboard
from modules.learn      import LearnModule,      handle_learn

COMMANDS = [
    "sched", "mem", "fs", "disk", "deadlock", "sync",
    "dashboard", "dash", "learn", "help", "clear", "exit", "quit",
]

SUBCOMMANDS = {
    "sched":    ["add", "list", "run", "compare", "clear",
                 "--algo=fcfs", "--algo=sjf", "--algo=srtf",
                 "--algo=rr", "--algo=priority", "--algo=mlfq",
                 "--burst=", "--arrival=", "--priority=", "--quantum="],
    "mem":      ["init", "alloc", "free", "show", "pagefault", "compare", "buddy",
                 "--frames=", "--pages=", "--algo=firstfit", "--algo=bestfit",
                 "--algo=worstfit", "--algo=fifo", "--algo=lru",
                 "--algo=optimal", "--algo=clock", "--ref=", "--size="],
    "fs":       ["pwd", "cd", "ls", "tree", "mkdir", "touch", "rm", "rmdir",
                 "cat", "write", "chmod", "stat", "inode", "fat", "find"],
    "disk":     ["init", "add", "run", "compare", "clear",
                 "--algo=fcfs", "--algo=sstf", "--algo=scan",
                 "--algo=cscan", "--algo=look", "--algo=clook",
                 "--tracks=", "--head="],
    "deadlock": ["init", "max", "alloc", "available", "request",
                 "check", "rag", "recover", "show",
                 "--processes=", "--resources="],
    "sync":     ["dining", "producer", "reader", "semaphore",
                 "--philosophers=", "--buffers=", "--producers=",
                 "--consumers=", "--readers=", "--writers=",
                 "--steps=", "--initial=", "--animate"],
}

HELP_TEXT = {
    "sched": {
        "desc": "Process Scheduling — FCFS, SJF, SRTF, Round Robin, Priority, MLFQ",
        "cmds": [
            ("sched add <name> [--burst=N] [--arrival=N] [--priority=N]", "Add a process"),
            ("sched list",                                                 "List all processes"),
            ("sched run --algo=<fcfs|sjf|srtf|rr|priority|mlfq> [--quantum=N]",
             "Run scheduling algorithm"),
            ("sched compare [--quantum=N]",                                "Compare all algorithms"),
            ("sched clear",                                                "Clear process list"),
        ]
    },
    "mem": {
        "desc": "Memory Management — Paging, Page Replacement, Buddy System",
        "cmds": [
            ("mem init [--frames=N]",                                      "Initialize memory"),
            ("mem alloc <name> [--pages=N] [--algo=firstfit|bestfit|worstfit]", "Allocate frames"),
            ("mem free <name>",                                            "Free process memory"),
            ("mem show",                                                   "Show frame grid"),
            ("mem pagefault --algo=<fifo|lru|optimal|clock> [--frames=N] [--ref=1,2,3,...]",
             "Page replacement simulation"),
            ("mem compare [--frames=N] [--ref=...]",                       "Compare all page algos"),
            ("mem buddy --size=N",                                         "Buddy system allocator"),
        ]
    },
    "fs": {
        "desc": "Virtual File System — Inodes, FAT, Permissions",
        "cmds": [
            ("fs pwd / fs cd <path>",   "Print/change working directory"),
            ("fs ls [path]",            "List directory contents"),
            ("fs tree [path]",          "Show directory tree"),
            ("fs mkdir / fs touch / fs rm <path>", "Create/remove files and dirs"),
            ("fs cat <path>",           "Print file contents"),
            ("fs write <path> <content>", "Write to file"),
            ("fs chmod <path> <mode>",  "Change permissions (e.g. 755)"),
            ("fs stat <path>",          "Show inode info"),
            ("fs inode",                "Show full inode table"),
            ("fs fat <path>",           "Show FAT cluster chain"),
            ("fs find <name>",          "Search for file"),
        ]
    },
    "disk": {
        "desc": "Disk Scheduling — FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK",
        "cmds": [
            ("disk init [--tracks=N] [--head=N]", "Initialize disk"),
            ("disk add <track1> [track2 ...]",     "Add track requests"),
            ("disk run --algo=<fcfs|sstf|scan|cscan|look|clook>", "Run algorithm"),
            ("disk compare",                        "Compare all algorithms"),
            ("disk clear",                          "Clear request queue"),
        ]
    },
    "deadlock": {
        "desc": "Deadlock Detection & Recovery — Banker's Algorithm, RAG",
        "cmds": [
            ("deadlock init --processes=P0,P1,P2 --resources=R0,R1,R2", "Initialize"),
            ("deadlock max <process> <v1> <v2> ...",   "Set maximum demand"),
            ("deadlock alloc <process> <v1> <v2> ...", "Set current allocation"),
            ("deadlock available <v1> <v2> ...",        "Set available resources"),
            ("deadlock request <process> <v1> <v2> ...", "Request resources"),
            ("deadlock check",  "Run Banker's safety algorithm"),
            ("deadlock rag",    "Show Resource Allocation Graph"),
            ("deadlock recover","Suggest recovery from deadlock"),
        ]
    },
    "sync": {
        "desc": "Synchronization — Dining Philosophers, Producer-Consumer, Reader-Writer",
        "cmds": [
            ("sync dining [--philosophers=N] [--steps=N] [--animate]", "Dining Philosophers"),
            ("sync producer [--buffers=N] [--producers=N] [--consumers=N] [--steps=N]",
             "Producer-Consumer"),
            ("sync reader [--readers=N] [--writers=N] [--steps=N]", "Reader-Writer"),
            ("sync semaphore [--initial=N] [--steps=N]",             "Semaphore demo"),
        ]
    },
    "dashboard": {
        "desc": "Live 4-panel system dashboard",
        "cmds": [
            ("dashboard  (or: dash)", "Show live system dashboard (Ctrl+C to exit)"),
        ]
    },
}


def print_help(console: Console, topic: str = "") -> None:
    if topic and topic in HELP_TEXT:
        info = HELP_TEXT[topic]
        console.print()
        console.print(Panel(
            Text(info["desc"], style="bold bright_white"),
            title=f"[bold bright_cyan]Help: {topic}[/bold bright_cyan]",
            border_style="bright_cyan"
        ))
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        table.add_column("Command",     style="bold bright_cyan", min_width=55)
        table.add_column("Description", style="dim white")
        for cmd, desc in info["cmds"]:
            table.add_row(cmd, desc)
        console.print(table)
        console.print()
        return

    console.print()
        console.print(Panel(
            Text("NazzOS — Interactive OS Simulator", style="bold bright_white"),
            subtitle="[dim]Type 'help <module>' for detailed usage[/dim]",
            border_style="bright_cyan"
        ))
    table = Table(box=box.ROUNDED, border_style="bright_cyan",
                  header_style="bold white on dark_blue", show_lines=True)
    table.add_column("Module",      style="bold bright_cyan", min_width=12)
    table.add_column("Description", style="white")
    table.add_column("Algorithms / Features", style="dim white")

    modules = [
        ("sched",    "Process Scheduling",    "FCFS, SJF, SRTF, RR, Priority, MLFQ"),
        ("mem",      "Memory Management",     "Paging, FIFO/LRU/Optimal/Clock, Buddy System"),
        ("fs",       "Virtual File System",   "Inodes, FAT, Permissions, Tree View"),
        ("disk",     "Disk Scheduling",       "FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK"),
        ("deadlock", "Deadlock Detection",    "Banker's Algorithm, RAG, Recovery"),
        ("sync",     "Synchronization",       "Dining Philosophers, Producer-Consumer, Reader-Writer"),
        ("dashboard","Live Dashboard",        "Real-time system monitor (Ctrl+C to exit)"),
        ("learn",    "Linux Learning Center", "Lessons, practice challenges, quiz, cheatsheet"),
        ("clear",    "Clear screen",          "—"),
        ("exit",     "Exit NazzOS",           "—"),
    ]
    for mod, desc, algos in modules:
        table.add_row(mod, desc, algos)
    console.print(table)
    console.print()


def make_completer() -> WordCompleter:
    words = list(COMMANDS)
    for subs in SUBCOMMANDS.values():
        words.extend(subs)
    return WordCompleter(words, ignore_case=True)


PT_STYLE = Style.from_dict({
    "prompt":         "ansicyan bold",
    "prompt.bracket": "ansibrightcyan",
})


def _run_system_cmd(raw: str, console: Console) -> None:
    cmd = raw.split()[0]
    if not shutil.which(cmd):
            console.print(f"  [red]Command not found: '{cmd}'. Type [bold]help[/bold] for NazzOS commands.[/red]")
        return
    try:
        result = subprocess.run(raw, shell=True, text=True,
                                capture_output=True)
        if result.stdout:
            console.print(result.stdout, end="")
        if result.stderr:
            console.print(result.stderr, end="", style="red")
    except Exception as e:
        console.print(f"  [red]{e}[/red]")


def run_shell(console: Console) -> None:
    sched  = Scheduler()
    mem    = MemoryManager()
    fs     = VirtualFS()
    disk   = DiskScheduler()
    dl     = DeadlockDetector()
    learn  = LearnModule()

    session: PromptSession = PromptSession(
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        completer=make_completer(),
        style=PT_STYLE,
        complete_while_typing=True,
    )

    while True:
        try:
            cwd    = fs.cwd_path
            prompt = f"NazzOS [{cwd}]> "
            raw    = session.prompt(prompt)
        except KeyboardInterrupt:
            console.print("\n  [dim]Use 'exit' to quit.[/dim]")
            continue
        except EOFError:
            break

        raw = raw.strip()
        if not raw:
            continue

        parts = raw.split()
        cmd   = parts[0].lower()
        args  = parts[1:]

        if cmd in ("exit", "quit"):
            console.print("\n  [bold bright_green]Shutting down NazzOS. Goodbye![/bold bright_green]\n")
            break

        elif cmd == "clear":
            console.clear()

        elif cmd == "help":
            topic = args[0] if args else ""
            print_help(console, topic)

        elif cmd == "sched":
            handle_sched(args, sched, console)

        elif cmd == "mem":
            handle_mem(args, mem, console)

        elif cmd == "fs":
            result = handle_fs(args, fs, console)

        elif cmd == "disk":
            handle_disk(args, disk, console)

        elif cmd == "deadlock":
            handle_deadlock(args, dl, console)

        elif cmd == "sync":
            handle_sync(args, console)

        elif cmd in ("dashboard", "dash"):
            run_dashboard(console, fs)

        elif cmd == "learn":
            handle_learn(args, learn, console)

        else:
            _run_system_cmd(raw, console)
