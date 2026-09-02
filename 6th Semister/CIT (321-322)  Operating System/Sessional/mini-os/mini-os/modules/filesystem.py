from __future__ import annotations
import time as _time
from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich import box
from ui.widgets import section_header


@dataclass
class INode:
    inode_id: int
    name: str
    is_dir: bool
    content: str = ""
    permissions: str = "rw-r--r--"
    owner: str = "user"
    size: int = 0
    links: int = 1
    created: float = field(default_factory=_time.time)
    modified: float = field(default_factory=_time.time)
    children: dict[str, "INode"] = field(default_factory=dict)
    fat_clusters: list[int] = field(default_factory=list)
    _next_cluster: int = 0

    def __post_init__(self):
        if self.is_dir:
            self.permissions = "rwxr-xr-x"
        self.size = len(self.content)
        if not self.is_dir and self.content:
            num_clusters = max(1, (self.size + 511) // 512)
            self.fat_clusters = list(range(self._next_cluster,
                                           self._next_cluster + num_clusters))


class VirtualFS:
    def __init__(self):
        self._inode_counter = 0
        self.root = self._make_node("/", is_dir=True)
        self.root.permissions = "rwxr-xr-x"
        self.cwd_path = "/"
        self._cwd: INode = self.root
        self._cluster_counter = 2
        self._all_inodes: dict[int, INode] = {0: self.root}
        self._populate_default()

    def _make_node(self, name: str, is_dir: bool, content: str = "") -> INode:
        node = INode(
            inode_id=self._inode_counter,
            name=name,
            is_dir=is_dir,
            content=content,
            size=len(content),
        )
        self._inode_counter += 1
        return node

    def _populate_default(self):
        for d in ["home", "etc", "tmp", "bin", "var"]:
            self._mkdir_node(self.root, d)
        home = self.root.children["home"]
        self._mkdir_node(home, "user")
        user = home.children["user"]
        self._touch_node(user, "readme.txt",
                 "Welcome to nazzos!\nType 'help' to see available commands.")
        self._mkdir_node(user, "projects")
        etc = self.root.children["etc"]
        self._touch_node(etc, "os.conf",
                         "[kernel]\nscheduler=RR\nquantum=2\n\n[memory]\nframes=16\nalgo=firstfit")
        self._touch_node(etc, "hosts",
                         "127.0.0.1  localhost\n::1        localhost")

    def _mkdir_node(self, parent: INode, name: str) -> INode:
        node = self._make_node(name, is_dir=True)
        parent.children[name] = node
        self._all_inodes[node.inode_id] = node
        return node

    def _touch_node(self, parent: INode, name: str, content: str = "") -> INode:
        node = self._make_node(name, is_dir=False, content=content)
        num_clusters = max(1, (node.size + 511) // 512)
        node.fat_clusters = list(range(self._cluster_counter,
                                       self._cluster_counter + num_clusters))
        self._cluster_counter += num_clusters
        parent.children[name] = node
        self._all_inodes[node.inode_id] = node
        return node

    def _resolve(self, path: str) -> INode | None:
        if path == "/":
            return self.root
        parts = [p for p in path.strip("/").split("/") if p]
        node  = self.root if path.startswith("/") else self._cwd
        for part in parts:
            if part == "..":
                node = self._parent_of(node) or self.root
            elif part == ".":
                continue
            elif part in node.children:
                node = node.children[part]
            else:
                return None
        return node

    def _parent_of(self, node: INode) -> INode | None:
        def search(current: INode) -> INode | None:
            for child in current.children.values():
                if child is node:
                    return current
                found = search(child)
                if found:
                    return found
            return None
        return search(self.root)

    def _abs_path(self, node: INode) -> str:
        if node is self.root:
            return "/"
        parts = []
        current = node
        while current is not self.root:
            parts.append(current.name)
            current = self._parent_of(current) or self.root
        return "/" + "/".join(reversed(parts))

    # ── Commands ──────────────────────────────────────────────────────────
    def pwd(self) -> str:
        return self.cwd_path

    def cd(self, path: str) -> str:
        node = self._resolve(path)
        if node is None:
            return f"[red]cd: {path}: No such file or directory[/red]"
        if not node.is_dir:
            return f"[red]cd: {path}: Not a directory[/red]"
        self._cwd    = node
        self.cwd_path = self._abs_path(node)
        return ""

    def ls(self, console: Console, path: str = ".") -> None:
        node = self._resolve(path) if path != "." else self._cwd
        if node is None:
            console.print(f"[red]ls: {path}: No such file or directory[/red]")
            return
        if not node.is_dir:
            self._print_file_row(console, node)
            return

        table = Table(box=box.SIMPLE_HEAVY, border_style="bright_cyan",
                      header_style="bold white", show_header=True)
        table.add_column("Permissions")
        table.add_column("Links", justify="center")
        table.add_column("Owner")
        table.add_column("Size", justify="right")
        table.add_column("Modified")
        table.add_column("Name")

        for child in sorted(node.children.values(),
                             key=lambda n: (not n.is_dir, n.name)):
            mod_str = _time.strftime("%b %d %H:%M", _time.localtime(child.modified))
            name_str = (Text(f"📁 {child.name}/", style="bold bright_blue")
                        if child.is_dir
                        else Text(f"📄 {child.name}", style="bright_white"))
            table.add_row(
                child.permissions,
                str(child.links),
                child.owner,
                str(child.size) if not child.is_dir else "—",
                mod_str,
                name_str,
            )
        console.print(table)

    def _print_file_row(self, console: Console, node: INode) -> None:
        console.print(f"  {node.permissions}  {node.owner}  {node.size}B  {node.name}")

    def tree(self, console: Console, path: str = "/") -> None:
        node = self._resolve(path)
        if node is None:
            console.print(f"[red]tree: {path}: No such file or directory[/red]")
            return
        rich_tree = Tree(
            Text(f"📁 {node.name}/", style="bold bright_blue") if node.is_dir
            else Text(f"📄 {node.name}", style="bright_white"),
            guide_style="bright_cyan"
        )
        self._build_tree(rich_tree, node)
        console.print(rich_tree)

    def _build_tree(self, tree_node: Tree, fs_node: INode) -> None:
        for child in sorted(fs_node.children.values(),
                             key=lambda n: (not n.is_dir, n.name)):
            if child.is_dir:
                label = Text(f"📁 {child.name}/", style="bold bright_blue")
                branch = tree_node.add(label)
                self._build_tree(branch, child)
            else:
                label = Text(f"📄 {child.name}  ", style="bright_white")
                label.append(f"[{child.size}B]", style="dim")
                tree_node.add(label)

    def mkdir(self, path: str) -> str:
        parts = path.rstrip("/").rsplit("/", 1)
        if len(parts) == 1:
            parent, name = self._cwd, parts[0]
        else:
            parent_path, name = parts
            parent = self._resolve(parent_path or "/")
        if parent is None:
            return f"[red]mkdir: {path}: Parent directory not found[/red]"
        if name in parent.children:
            return f"[red]mkdir: {name}: Already exists[/red]"
        self._mkdir_node(parent, name)
        return f"[green]Directory created: {path}[/green]"

    def touch(self, path: str) -> str:
        parts = path.rstrip("/").rsplit("/", 1)
        if len(parts) == 1:
            parent, name = self._cwd, parts[0]
        else:
            parent_path, name = parts
            parent = self._resolve(parent_path or "/")
        if parent is None:
            return f"[red]touch: {path}: Parent directory not found[/red]"
        if name in parent.children:
            parent.children[name].modified = _time.time()
            return f"[green]Updated timestamp: {name}[/green]"
        self._touch_node(parent, name)
        return f"[green]Created: {path}[/green]"

    def write(self, path: str, content: str) -> str:
        node = self._resolve(path)
        if node is None:
            self.touch(path)
            node = self._resolve(path)
        if node.is_dir:
            return f"[red]write: {path}: Is a directory[/red]"
        node.content  = content
        node.size     = len(content)
        node.modified = _time.time()
        num_clusters  = max(1, (node.size + 511) // 512)
        node.fat_clusters = list(range(self._cluster_counter,
                                       self._cluster_counter + num_clusters))
        self._cluster_counter += num_clusters
        return f"[green]Written {node.size} bytes to {path}[/green]"

    def cat(self, path: str) -> str:
        node = self._resolve(path)
        if node is None:
            return f"[red]cat: {path}: No such file[/red]"
        if node.is_dir:
            return f"[red]cat: {path}: Is a directory[/red]"
        return node.content if node.content else "(empty file)"

    def rm(self, path: str) -> str:
        parts = path.rstrip("/").rsplit("/", 1)
        if len(parts) == 1:
            parent, name = self._cwd, parts[0]
        else:
            parent_path, name = parts
            parent = self._resolve(parent_path or "/")
        if parent is None or name not in parent.children:
            return f"[red]rm: {path}: No such file[/red]"
        node = parent.children[name]
        if node.is_dir and node.children:
            return f"[red]rm: {path}: Directory not empty. Use 'fs rmdir'[/red]"
        del parent.children[name]
        return f"[green]Removed: {path}[/green]"

    def chmod(self, path: str, mode: str) -> str:
        node = self._resolve(path)
        if node is None:
            return f"[red]chmod: {path}: No such file[/red]"
        if len(mode) == 3 and mode.isdigit():
            perm_map = {
                "0": "---", "1": "--x", "2": "-w-", "3": "-wx",
                "4": "r--", "5": "r-x", "6": "rw-", "7": "rwx"
            }
            node.permissions = "".join(perm_map[c] for c in mode)
        else:
            node.permissions = mode
        return f"[green]Changed permissions of {path} to {node.permissions}[/green]"

    def stat(self, console: Console, path: str) -> None:
        node = self._resolve(path)
        if node is None:
            console.print(f"[red]stat: {path}: No such file[/red]")
            return
        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True,
                      title=f"Stat: {path}")
        table.add_column("Field",  style="bold cyan")
        table.add_column("Value",  style="white")
        table.add_row("Inode",       str(node.inode_id))
        table.add_row("Name",        node.name)
        table.add_row("Type",        "Directory" if node.is_dir else "Regular File")
        table.add_row("Size",        f"{node.size} bytes")
        table.add_row("Permissions", node.permissions)
        table.add_row("Owner",       node.owner)
        table.add_row("Links",       str(node.links))
        table.add_row("Created",     _time.strftime("%Y-%m-%d %H:%M:%S",
                                     _time.localtime(node.created)))
        table.add_row("Modified",    _time.strftime("%Y-%m-%d %H:%M:%S",
                                     _time.localtime(node.modified)))
        if not node.is_dir:
            table.add_row("FAT Clusters", "→ ".join(str(c) for c in node.fat_clusters))
        console.print(table)

    def inode_table(self, console: Console) -> None:
        section_header(console, "Inode Table")
        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        for col in ["Inode", "Name", "Type", "Size", "Perms", "Links", "Clusters"]:
            table.add_column(col, justify="center")
        for inode_id, node in sorted(self._all_inodes.items()):
            if node.is_dir:
                name_str = Text(f"📁 {node.name}", style="bold bright_blue")
                type_str = "DIR"
                clusters = "—"
            else:
                name_str = Text(f"📄 {node.name}", style="bright_white")
                type_str = "FILE"
                clusters = "→".join(str(c) for c in node.fat_clusters) if node.fat_clusters else "—"
            table.add_row(str(inode_id), name_str, type_str,
                          str(node.size), node.permissions,
                          str(node.links), clusters)
        console.print(table)

    def fat_view(self, console: Console, path: str) -> None:
        node = self._resolve(path)
        if node is None:
            console.print(f"[red]fat: {path}: No such file[/red]")
            return
        if node.is_dir:
            console.print(f"[red]fat: {path}: Is a directory[/red]")
            return
        section_header(console, "FAT Cluster Chain", path)
        if not node.fat_clusters:
            console.print("  [yellow](No clusters allocated)[/yellow]")
            return
        chain = " → ".join(
            f"[bold bright_cyan]{c}[/bold bright_cyan]" for c in node.fat_clusters
        )
        chain += " → [dim]EOF[/dim]"
        console.print(f"  {chain}")
        console.print(f"\n  [dim]Each cluster = 512 bytes | Total clusters: {len(node.fat_clusters)}[/dim]\n")

    def find(self, console: Console, name: str) -> None:
        results = []
        self._find_recursive(self.root, name, "/", results)
        if not results:
            console.print(f"  [yellow]No files found matching '{name}'[/yellow]")
            return
        for path in results:
            console.print(f"  [bright_white]{path}[/bright_white]")

    def _find_recursive(self, node: INode, name: str,
                        current_path: str, results: list[str]) -> None:
        for child_name, child in node.children.items():
            child_path = (current_path.rstrip("/") + "/" + child_name)
            if name.lower() in child_name.lower():
                results.append(child_path)
            if child.is_dir:
                self._find_recursive(child, name, child_path, results)


def handle_fs(args: list[str], fs: VirtualFS, console: Console) -> tuple[str, str]:
    if not args:
        console.print("[yellow]Usage: fs <pwd|cd|ls|tree|mkdir|touch|rm|cat|write|chmod|stat|inode|fat|find>[/yellow]")
        return fs.cwd_path, ""

    sub = args[0]

    if sub == "pwd":
        console.print(f"  [bright_white]{fs.pwd()}[/bright_white]")
    elif sub == "cd":
        path = args[1] if len(args) > 1 else "/"
        msg = fs.cd(path)
        if msg:
            console.print(msg)
    elif sub == "ls":
        path = args[1] if len(args) > 1 else "."
        fs.ls(console, path)
    elif sub == "tree":
        path = args[1] if len(args) > 1 else "/"
        fs.tree(console, path)
    elif sub == "mkdir":
        if len(args) < 2:
            console.print("[yellow]Usage: fs mkdir <path>[/yellow]");
        else:
            console.print(fs.mkdir(args[1]))
    elif sub == "touch":
        if len(args) < 2:
            console.print("[yellow]Usage: fs touch <path>[/yellow]")
        else:
            console.print(fs.touch(args[1]))
    elif sub == "rm":
        if len(args) < 2:
            console.print("[yellow]Usage: fs rm <path>[/yellow]")
        else:
            console.print(fs.rm(args[1]))
    elif sub == "rmdir":
        if len(args) < 2:
            console.print("[yellow]Usage: fs rmdir <path>[/yellow]")
        else:
            console.print(fs.rm(args[1]))
    elif sub == "cat":
        if len(args) < 2:
            console.print("[yellow]Usage: fs cat <path>[/yellow]")
        else:
            console.print(fs.cat(args[1]))
    elif sub == "write":
        if len(args) < 3:
            console.print("[yellow]Usage: fs write <path> <content>[/yellow]")
        else:
            console.print(fs.write(args[1], " ".join(args[2:])))
    elif sub == "chmod":
        if len(args) < 3:
            console.print("[yellow]Usage: fs chmod <path> <mode>[/yellow]")
        else:
            console.print(fs.chmod(args[1], args[2]))
    elif sub == "stat":
        if len(args) < 2:
            console.print("[yellow]Usage: fs stat <path>[/yellow]")
        else:
            fs.stat(console, args[1])
    elif sub == "inode":
        fs.inode_table(console)
    elif sub == "fat":
        if len(args) < 2:
            console.print("[yellow]Usage: fs fat <path>[/yellow]")
        else:
            fs.fat_view(console, args[1])
    elif sub == "find":
        if len(args) < 2:
            console.print("[yellow]Usage: fs find <name>[/yellow]")
        else:
            fs.find(console, args[1])
    else:
        console.print(f"[red]Unknown fs subcommand: {sub}[/red]")

    return fs.cwd_path, ""
