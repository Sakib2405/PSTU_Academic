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


def handle_fs(args, fs: VirtualFS, console: Console) -> None:
	if not args:
		console.print("[info]fs: missing command. Type 'help' for usage.[/info]")
		return
	cmd = args[0]
	if cmd == "pwd":
		console.print(fs.pwd())
	elif cmd == "cd":
		path = args[1] if len(args) > 1 else "/"
		res = fs.cd(path)
		if res:
			console.print(res)
	elif cmd == "ls":
		path = args[1] if len(args) > 1 else "."
		fs.ls(console, path)
	elif cmd == "tree":
		path = args[1] if len(args) > 1 else "/"
		fs.tree(console, path)
	elif cmd == "mkdir":
		if len(args) < 2:
			console.print("[red]Usage: fs mkdir <path>[/red]")
		else:
			console.print(fs.mkdir(args[1]))
	elif cmd == "touch":
		if len(args) < 2:
			console.print("[red]Usage: fs touch <path>[/red]")
		else:
			console.print(fs.touch(args[1]))
	elif cmd == "cat":
		if len(args) < 2:
			console.print("[red]Usage: fs cat <path>[/red]")
		else:
			node = fs._resolve(args[1])
			if node is None:
				console.print(f"[red]cat: {args[1]}: No such file or directory[/red]")
			elif node.is_dir:
				console.print(f"[red]cat: {args[1]}: Is a directory[/red]")
			else:
				console.print(node.content)
	else:
		console.print(f"[info]fs: command not implemented: {cmd}[/info]")

