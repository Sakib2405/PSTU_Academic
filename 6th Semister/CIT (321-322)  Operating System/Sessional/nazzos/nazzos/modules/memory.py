class MemoryManager:
    def __init__(self) -> None:
        self._allocs = {}

    def info(self):
        return {"allocs": len(self._allocs)}


def handle_mem(args, mem: MemoryManager, console) -> None:
    console.print("[info]Memory placeholder: detailed memory ops not implemented.[/info]")
    if args and args[0] == "show":
        console.print(f"  Allocations: {mem.info()['allocs']}")
