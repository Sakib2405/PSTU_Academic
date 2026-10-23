class LearnModule:
	def __init__(self) -> None:
		self.lessons = ["Intro to Linux", "File Permissions", "Shell Basics"]

	def list(self):
		return list(self.lessons)


def handle_learn(args, learn: LearnModule, console) -> None:
	if not args:
		console.print("[info]Learn: available commands: list[/info]")
		return
	cmd = args[0]
	if cmd == "list":
		for i, lesson in enumerate(learn.list(), 1):
			console.print(f"  {i}. {lesson}")
	else:
		console.print(f"[info]learn: unknown command: {cmd}[/info]")
