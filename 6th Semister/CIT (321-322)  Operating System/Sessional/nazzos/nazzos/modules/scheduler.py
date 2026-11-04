from typing import List, Dict


class Scheduler:
    def __init__(self) -> None:
        self._procs: List[Dict] = []

    def add(self, name: str, **kwargs) -> None:
        self._procs.append({"name": name, **kwargs})

    def list(self) -> List[Dict]:
        return list(self._procs)


def handle_sched(args, sched: Scheduler, console) -> None:
    console.print("[info]Scheduler placeholder: basic commands not implemented.[/info]")
    if args and args[0] == "list":
        for p in sched.list():
            console.print(f"  - {p.get('name')}")
