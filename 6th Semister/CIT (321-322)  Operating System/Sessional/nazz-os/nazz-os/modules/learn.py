from __future__ import annotations
import subprocess
import shutil
import time
import random
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.rule import Rule
from rich import box
from ui.widgets import section_header

# ── Lesson Database ────────────────────────────────────────────────────────

LESSONS: dict[str, dict] = {

    "basic": {
        "title": "Basic Navigation",
        "icon":  "🗺",
        "commands": [
            {
                "cmd":     "pwd",
                "title":   "Print Working Directory",
                "desc":    "Shows your current location in the filesystem.",
                "example": "pwd",
                "output":  "/home/user",
                "tip":     "Always know where you are before doing anything!",
            },
            {
                "cmd":     "ls",
                "title":   "List Directory Contents",
                "desc":    "Shows files and folders in the current directory.",
                "example": "ls -la",
                "output":  "drwxr-xr-x  user  home/\n-rw-r--r--  user  file.txt",
                "tip":     "'-l' = long format, '-a' = show hidden files (starting with .)",
            },
            {
                "cmd":     "cd",
                "title":   "Change Directory",
                "desc":    "Navigate between directories.",
                "example": "cd /home/user\ncd ..        # go up one level\ncd ~         # go to home",
                "output":  "",
                "tip":     "'cd -' goes back to the previous directory you were in.",
            },
            {
                "cmd":     "mkdir",
                "title":   "Make Directory",
                "desc":    "Create a new folder.",
                "example": "mkdir myproject\nmkdir -p a/b/c   # create nested folders",
                "output":  "",
                "tip":     "Use '-p' to create parent directories automatically.",
            },
            {
                "cmd":     "rmdir",
                "title":   "Remove Directory",
                "desc":    "Delete an empty directory.",
                "example": "rmdir emptyfolder",
                "output":  "",
                "tip":     "Only works on empty directories. Use 'rm -rf' for non-empty (careful!).",
            },
            {
                "cmd":     "clear",
                "title":   "Clear Screen",
                "desc":    "Clear the terminal output.",
                "example": "clear",
                "output":  "",
                "tip":     "Shortcut: Ctrl+L also clears the screen.",
            },
        ],
    },

    "files": {
        "title": "File Operations",
        "icon":  "📄",
        "commands": [
            {
                "cmd":     "touch",
                "title":   "Create / Update File",
                "desc":    "Creates an empty file or updates a file's timestamp.",
                "example": "touch newfile.txt\ntouch file1.txt file2.txt",
                "output":  "",
                "tip":     "Useful for creating placeholder files quickly.",
            },
            {
                "cmd":     "cat",
                "title":   "Concatenate / Print File",
                "desc":    "Display file contents or combine files.",
                "example": "cat file.txt\ncat file1.txt file2.txt > combined.txt",
                "output":  "Hello, World!\nThis is line 2.",
                "tip":     "'cat -n' shows line numbers.",
            },
            {
                "cmd":     "cp",
                "title":   "Copy Files",
                "desc":    "Copy files or directories.",
                "example": "cp source.txt dest.txt\ncp -r folder/ backup/",
                "output":  "",
                "tip":     "'-r' (recursive) is needed to copy directories.",
            },
            {
                "cmd":     "mv",
                "title":   "Move / Rename Files",
                "desc":    "Move files or rename them.",
                "example": "mv old.txt new.txt      # rename\nmv file.txt /tmp/       # move",
                "output":  "",
                "tip":     "mv is also how you rename files in Linux!",
            },
            {
                "cmd":     "rm",
                "title":   "Remove Files",
                "desc":    "Delete files and directories.",
                "example": "rm file.txt\nrm -rf folder/    # remove folder recursively",
                "output":  "",
                "tip":     "⚠ 'rm -rf /' is DANGEROUS — deletes everything! Always double-check.",
            },
            {
                "cmd":     "find",
                "title":   "Find Files",
                "desc":    "Search for files and directories.",
                "example": "find . -name '*.txt'\nfind /home -type f -size +1M",
                "output":  "./notes.txt\n./docs/readme.txt",
                "tip":     "Combine with -exec to run commands on found files.",
            },
            {
                "cmd":     "ln",
                "title":   "Create Links",
                "desc":    "Create hard or symbolic links.",
                "example": "ln -s /path/to/file shortcut",
                "output":  "",
                "tip":     "Symlinks (-s) are like shortcuts. Hard links share inode.",
            },
        ],
    },

    "text": {
        "title": "Text Processing",
        "icon":  "📝",
        "commands": [
            {
                "cmd":     "grep",
                "title":   "Search Text",
                "desc":    "Search for patterns in files or output.",
                "example": "grep 'error' log.txt\ngrep -r 'TODO' .\nps aux | grep python",
                "output":  "log.txt:ERROR: connection failed",
                "tip":     "'-i' = case insensitive, '-r' = recursive, '-n' = show line numbers.",
            },
            {
                "cmd":     "sort",
                "title":   "Sort Lines",
                "desc":    "Sort lines of text files.",
                "example": "sort names.txt\nsort -n numbers.txt   # numeric sort\nsort -r file.txt      # reverse",
                "output":  "Alice\nBob\nCharlie",
                "tip":     "Combine with 'uniq' to remove duplicate lines.",
            },
            {
                "cmd":     "wc",
                "title":   "Word Count",
                "desc":    "Count lines, words, and characters.",
                "example": "wc -l file.txt    # count lines\nwc -w file.txt    # count words",
                "output":  "  42  300  1800 file.txt",
                "tip":     "ls | wc -l counts the number of files in a directory!",
            },
            {
                "cmd":     "cut",
                "title":   "Cut Columns",
                "desc":    "Extract sections from lines of files.",
                "example": "cut -d',' -f1 data.csv\ncut -c1-5 file.txt",
                "output":  "Alice\nBob\nCharlie",
                "tip":     "'-d' sets delimiter, '-f' selects field number.",
            },
            {
                "cmd":     "sed",
                "title":   "Stream Editor",
                "desc":    "Find and replace text in streams.",
                "example": "sed 's/old/new/g' file.txt\nsed -i 's/foo/bar/g' file.txt",
                "output":  "This is the new text.",
                "tip":     "'-i' edits the file in-place. The 'g' flag replaces all occurrences.",
            },
            {
                "cmd":     "awk",
                "title":   "Text Processing Tool",
                "desc":    "Powerful text processing and data extraction.",
                "example": "awk '{print $1}' file.txt\nawk -F',' '{print $2}' data.csv",
                "output":  "Alice\nBob",
                "tip":     "awk is a mini programming language — very powerful for logs!",
            },
            {
                "cmd":     "head/tail",
                "title":   "View File Parts",
                "desc":    "Show beginning or end of files.",
                "example": "head -n 10 file.txt\ntail -n 20 log.txt\ntail -f log.txt   # follow live",
                "output":  "Line 1\nLine 2...",
                "tip":     "'tail -f' is amazing for watching log files in real time!",
            },
        ],
    },

    "permissions": {
        "title": "Permissions & Ownership",
        "icon":  "🔒",
        "commands": [
            {
                "cmd":     "chmod",
                "title":   "Change Permissions",
                "desc":    "Change file read/write/execute permissions.",
                "example": "chmod 755 script.sh\nchmod +x script.sh\nchmod u=rwx,g=rx,o=r file",
                "output":  "",
                "tip":     "755 = rwxr-xr-x | 644 = rw-r--r-- | 777 = rwxrwxrwx (avoid!)",
            },
            {
                "cmd":     "chown",
                "title":   "Change Ownership",
                "desc":    "Change file owner and group.",
                "example": "chown user:group file.txt\nchown -R user:group folder/",
                "output":  "",
                "tip":     "Requires sudo. '-R' applies recursively to all contents.",
            },
            {
                "cmd":     "sudo",
                "title":   "Superuser Do",
                "desc":    "Execute commands with root privileges.",
                "example": "sudo pacman -Syu\nsudo systemctl restart nginx",
                "output":  "",
                "tip":     "Never run 'sudo rm -rf /' — it will destroy your system!",
            },
            {
                "cmd":     "whoami / id",
                "title":   "Current User Info",
                "desc":    "Show current user and group information.",
                "example": "whoami\nid\ngroups",
                "output":  "sourav\nuid=1000(sourav) gid=1000(sourav)",
                "tip":     "'id' shows all group memberships — useful for permission debugging.",
            },
        ],
    },

    "process": {
        "title": "Process Management",
        "icon":  "⚡",
        "commands": [
            {
                "cmd":     "ps",
                "title":   "Process Status",
                "desc":    "Show running processes.",
                "example": "ps aux\nps aux | grep python",
                "output":  "USER  PID %CPU %MEM  COMMAND\nroot  1   0.0  0.1  /sbin/init",
                "tip":     "'ps aux' shows all processes. Pipe to grep to find specific ones.",
            },
            {
                "cmd":     "top / htop",
                "title":   "Interactive Process Viewer",
                "desc":    "Real-time view of running processes.",
                "example": "top\nhtop",
                "output":  "",
                "tip":     "Press 'q' to quit top. htop has a nicer interface (install separately).",
            },
            {
                "cmd":     "kill / killall",
                "title":   "Kill Processes",
                "desc":    "Send signals to processes to terminate them.",
                "example": "kill 1234         # kill by PID\nkillall firefox   # kill by name\nkill -9 1234      # force kill",
                "output":  "",
                "tip":     "kill -9 (SIGKILL) force-kills. First try kill -15 (SIGTERM) gracefully.",
            },
            {
                "cmd":     "jobs / bg / fg",
                "title":   "Job Control",
                "desc":    "Manage foreground and background processes.",
                "example": "sleep 100 &    # run in background\njobs           # list background jobs\nfg %1          # bring job 1 to foreground",
                "output":  "[1]+ Running  sleep 100",
                "tip":     "Ctrl+Z suspends a process. Then 'bg' to resume it in the background.",
            },
            {
                "cmd":     "nohup",
                "title":   "No Hang Up",
                "desc":    "Run command that survives terminal close.",
                "example": "nohup python server.py &",
                "output":  "nohup: ignoring input and appending output to 'nohup.out'",
                "tip":     "Output goes to nohup.out. Use for long-running server processes.",
            },
        ],
    },

    "system": {
        "title": "System Information",
        "icon":  "🖥",
        "commands": [
            {
                "cmd":     "uname",
                "title":   "System Information",
                "desc":    "Print system/kernel information.",
                "example": "uname -a\nuname -r    # kernel version only",
                "output":  "Linux arch 6.1.0 #1 SMP x86_64 GNU/Linux",
                "tip":     "'-a' shows all info: kernel, hostname, arch, date.",
            },
            {
                "cmd":     "df",
                "title":   "Disk Free Space",
                "desc":    "Show disk space usage of filesystems.",
                "example": "df -h\ndf -h /home",
                "output":  "Filesystem  Size  Used  Avail  Use%  Mounted on\n/dev/sda1   100G   45G    55G   45%   /",
                "tip":     "'-h' = human readable (KB, MB, GB instead of blocks).",
            },
            {
                "cmd":     "du",
                "title":   "Disk Usage",
                "desc":    "Show disk usage of files and directories.",
                "example": "du -sh *\ndu -sh /home/user",
                "output":  "4.2G  Documents\n1.1G  Downloads",
                "tip":     "'-s' = summary (total only), '-h' = human readable.",
            },
            {
                "cmd":     "free",
                "title":   "Memory Usage",
                "desc":    "Display RAM and swap usage.",
                "example": "free -h",
                "output":  "              total  used  free\nMem:           16Gi  8.2Gi  7.8Gi\nSwap:          8Gi   0B    8Gi",
                "tip":     "Check 'available' column — that's actually usable RAM.",
            },
            {
                "cmd":     "uptime",
                "title":   "System Uptime",
                "desc":    "Show how long the system has been running.",
                "example": "uptime",
                "output":  "21:00  up 2:35,  1 user,  load average: 0.45, 0.32, 0.28",
                "tip":     "Load average: 1-min, 5-min, 15-min CPU load. >1 per core = overloaded.",
            },
            {
                "cmd":     "lscpu / lsblk",
                "title":   "Hardware Info",
                "desc":    "List CPU and block device information.",
                "example": "lscpu\nlsblk",
                "output":  "Architecture: x86_64\nCPU(s):       8",
                "tip":     "lsblk shows all drives and partitions in a tree view.",
            },
        ],
    },

    "network": {
        "title": "Networking",
        "icon":  "🌐",
        "commands": [
            {
                "cmd":     "ping",
                "title":   "Ping",
                "desc":    "Test network connectivity to a host.",
                "example": "ping google.com\nping -c 4 8.8.8.8",
                "output":  "64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.4 ms",
                "tip":     "'-c N' sends exactly N packets. Ctrl+C to stop.",
            },
            {
                "cmd":     "curl",
                "title":   "Transfer Data",
                "desc":    "Transfer data from/to servers.",
                "example": "curl https://example.com\ncurl -O https://file.zip\ncurl -X POST -d 'data' url",
                "output":  "<!DOCTYPE html><html>...",
                "tip":     "curl is extremely powerful — supports HTTP, FTP, SFTP and more.",
            },
            {
                "cmd":     "wget",
                "title":   "Download Files",
                "desc":    "Download files from the internet.",
                "example": "wget https://example.com/file.zip\nwget -q --show-progress url",
                "output":  "file.zip  100%[======>] 25MB  2.1MB/s",
                "tip":     "'-q' = quiet mode, '--continue' resumes incomplete downloads.",
            },
            {
                "cmd":     "ip / ifconfig",
                "title":   "Network Interfaces",
                "desc":    "Show and configure network interfaces.",
                "example": "ip addr\nip route\nifconfig",
                "output":  "eth0: inet 192.168.1.100",
                "tip":     "'ip' is the modern replacement for 'ifconfig' on Linux.",
            },
            {
                "cmd":     "ss / netstat",
                "title":   "Socket Statistics",
                "desc":    "Display network connections and ports.",
                "example": "ss -tuln\nnetstat -an | grep LISTEN",
                "output":  "tcp  LISTEN  0.0.0.0:80",
                "tip":     "'ss -tuln' shows all listening TCP/UDP ports — great for security.",
            },
        ],
    },

    "pipes": {
        "title": "Pipes & Redirection",
        "icon":  "🔗",
        "commands": [
            {
                "cmd":     "|  (pipe)",
                "title":   "Pipe Output",
                "desc":    "Send output of one command as input to another.",
                "example": "ls -la | grep '.txt'\nps aux | grep python | wc -l\ncat file | sort | uniq",
                "output":  "notes.txt\nreport.txt",
                "tip":     "You can chain as many pipes as you want! This is the Linux superpower.",
            },
            {
                "cmd":     "> and >>",
                "title":   "Output Redirection",
                "desc":    "Redirect output to a file.",
                "example": "echo 'Hello' > file.txt     # overwrite\necho 'World' >> file.txt    # append\nls > filelist.txt",
                "output":  "",
                "tip":     "'>' overwrites the file. '>>' appends to it. Don't mix them up!",
            },
            {
                "cmd":     "< (input redirect)",
                "title":   "Input Redirection",
                "desc":    "Feed a file as input to a command.",
                "example": "sort < names.txt\nwc -l < file.txt",
                "output":  "42",
                "tip":     "Less commonly used but useful for commands that read from stdin.",
            },
            {
                "cmd":     "2> and 2>&1",
                "title":   "Error Redirection",
                "desc":    "Redirect error output (stderr).",
                "example": "command 2> errors.txt\ncommand > out.txt 2>&1\ncommand 2>/dev/null",
                "output":  "",
                "tip":     "'2>/dev/null' silences all errors. Very useful in scripts!",
            },
            {
                "cmd":     "tee",
                "title":   "Split Output",
                "desc":    "Write to file AND show on screen at the same time.",
                "example": "ls | tee filelist.txt\ncommand | tee -a log.txt",
                "output":  "Shows on screen AND saves to file",
                "tip":     "'-a' appends to existing file instead of overwriting.",
            },
            {
                "cmd":     "xargs",
                "title":   "Build Command Arguments",
                "desc":    "Pass piped input as arguments to another command.",
                "example": "find . -name '*.log' | xargs rm\ncat urls.txt | xargs wget",
                "output":  "",
                "tip":     "xargs + find is incredibly powerful for batch operations.",
            },
        ],
    },

    "advanced": {
        "title": "Advanced Commands",
        "icon":  "🚀",
        "commands": [
            {
                "cmd":     "systemctl",
                "title":   "Service Manager",
                "desc":    "Control systemd services (Arch Linux default).",
                "example": "systemctl start nginx\nsystemctl enable sshd\nsystemctl status bluetooth",
                "output":  "● nginx.service - A high performance web server\n   Active: active (running)",
                "tip":     "'enable' = start on boot. 'start' = start now. 'status' = check state.",
            },
            {
                "cmd":     "pacman",
                "title":   "Package Manager (Arch)",
                "desc":    "Install, update, remove packages on Arch Linux.",
                "example": "sudo pacman -S firefox    # install\nsudo pacman -Syu          # update all\nsudo pacman -R package    # remove",
                "output":  "resolving dependencies...\nPackages to install: firefox",
                "tip":     "'-Syu' = sync + update. Always run before installing new packages.",
            },
            {
                "cmd":     "crontab",
                "title":   "Schedule Tasks",
                "desc":    "Schedule commands to run automatically.",
                "example": "crontab -e              # edit cron jobs\n# Run every day at 2am:\n0 2 * * * /backup.sh",
                "output":  "",
                "tip":     "Format: minute hour day month weekday command. Use crontab.guru!",
            },
            {
                "cmd":     "ssh",
                "title":   "Secure Shell",
                "desc":    "Connect to remote computers securely.",
                "example": "ssh user@192.168.1.10\nssh -p 2222 user@server.com\nssh -i key.pem user@host",
                "output":  "Welcome to Ubuntu 22.04 LTS",
                "tip":     "Use SSH keys instead of passwords for better security.",
            },
            {
                "cmd":     "tar",
                "title":   "Archive Files",
                "desc":    "Create and extract tar archives.",
                "example": "tar -czf archive.tar.gz folder/   # create\ntar -xzf archive.tar.gz           # extract\ntar -tzf archive.tar.gz           # list",
                "output":  "folder/\nfolder/file1.txt",
                "tip":     "Remember: 'czf' = Create Zip File, 'xzf' = eXtract Zip File",
            },
            {
                "cmd":     "alias",
                "title":   "Create Shortcuts",
                "desc":    "Create shortcuts for long commands.",
                "example": "alias ll='ls -la'\nalias update='sudo pacman -Syu'\nalias ..='cd ..'",
                "output":  "",
                "tip":     "Add aliases to ~/.bashrc or ~/.zshrc to make them permanent.",
            },
        ],
    },
}

# ── Practice Challenges ────────────────────────────────────────────────────

CHALLENGES: list[dict] = [
    {
        "level": "Beginner",
        "task":  "Show the current directory you are in.",
        "hint":  "Think: Print Working Directory",
        "answers": ["pwd"],
    },
    {
        "level": "Beginner",
        "task":  "List all files including hidden ones in long format.",
        "hint":  "ls with -l and -a flags",
        "answers": ["ls -la", "ls -al", "ls -l -a", "ls -a -l"],
    },
    {
        "level": "Beginner",
        "task":  "Create a new directory called 'myproject'.",
        "hint":  "make directory",
        "answers": ["mkdir myproject"],
    },
    {
        "level": "Beginner",
        "task":  "Create an empty file called 'notes.txt'.",
        "hint":  "touch the file into existence",
        "answers": ["touch notes.txt"],
    },
    {
        "level": "Intermediate",
        "task":  "Find all .txt files in the current directory and subdirectories.",
        "hint":  "find command with -name flag",
        "answers": ["find . -name '*.txt'", 'find . -name "*.txt"'],
    },
    {
        "level": "Intermediate",
        "task":  "Count the number of lines in a file called 'data.txt'.",
        "hint":  "word count with lines flag",
        "answers": ["wc -l data.txt"],
    },
    {
        "level": "Intermediate",
        "task":  "Search for the word 'error' in a file called 'log.txt'.",
        "hint":  "global regular expression print",
        "answers": ["grep error log.txt", "grep 'error' log.txt"],
    },
    {
        "level": "Intermediate",
        "task":  "Show disk usage in human-readable format.",
        "hint":  "df with human-readable flag",
        "answers": ["df -h"],
    },
    {
        "level": "Advanced",
        "task":  "List all running processes and filter for 'python'.",
        "hint":  "ps aux piped to grep",
        "answers": ["ps aux | grep python"],
    },
    {
        "level": "Advanced",
        "task":  "Make a script 'run.sh' executable.",
        "hint":  "change mode, add execute permission",
        "answers": ["chmod +x run.sh", "chmod 755 run.sh"],
    },
    {
        "level": "Advanced",
        "task":  "Sort a file 'names.txt' and save the result to 'sorted.txt'.",
        "hint":  "sort with output redirection",
        "answers": ["sort names.txt > sorted.txt"],
    },
    {
        "level": "Advanced",
        "task":  "Show only the first 5 lines of 'bigfile.txt'.",
        "hint":  "head command with -n flag",
        "answers": ["head -n 5 bigfile.txt", "head -5 bigfile.txt"],
    },
]

# ── Quiz Questions ─────────────────────────────────────────────────────────

QUIZ: list[dict] = [
    {
        "q":       "Which command shows your current directory?",
        "options": ["ls", "pwd", "cd", "dir"],
        "answer":  1,
    },
    {
        "q":       "What does 'chmod 755 file' do?",
        "options": [
            "Deletes the file",
            "Makes owner rwx, group and others r-x",
            "Makes file hidden",
            "Renames the file",
        ],
        "answer":  1,
    },
    {
        "q":       "Which symbol redirects output to a file (overwrite)?",
        "options": [">>", "|", ">", "<"],
        "answer":  2,
    },
    {
        "q":       "What does 'grep -r' do?",
        "options": [
            "Search in reverse order",
            "Search recursively in all subdirectories",
            "Search with regex",
            "Search and replace",
        ],
        "answer":  1,
    },
    {
        "q":       "Which command shows RAM usage?",
        "options": ["df -h", "du -h", "free -h", "top -m"],
        "answer":  2,
    },
    {
        "q":       "What does 'kill -9' do?",
        "options": [
            "Gracefully stops a process",
            "Pauses a process",
            "Force-kills a process immediately",
            "Lists processes",
        ],
        "answer":  2,
    },
    {
        "q":       "In Arch Linux, which command installs a package?",
        "options": ["apt install", "yum install", "pacman -S", "brew install"],
        "answer":  2,
    },
    {
        "q":       "What does 'tail -f log.txt' do?",
        "options": [
            "Shows last 10 lines",
            "Follows the file in real-time (live view)",
            "Deletes the tail of the file",
            "Sorts by last modified",
        ],
        "answer":  1,
    },
    {
        "q":       "What does the pipe '|' operator do?",
        "options": [
            "Appends to a file",
            "Runs two commands in parallel",
            "Sends output of one command as input to another",
            "Redirects errors",
        ],
        "answer":  2,
    },
    {
        "q":       "Which command creates nested directories in one go?",
        "options": ["mkdir a/b/c", "mkdir -p a/b/c", "mkdirs a/b/c", "md a/b/c"],
        "answer":  1,
    },
]


# ── Renderer ───────────────────────────────────────────────────────────────

class LearnModule:
    def __init__(self):
        self.completed: set[str] = set()
        self.score: int = 0
        self.total_lessons = sum(len(v["commands"]) for v in LESSONS.values())

    def show_menu(self, console: Console) -> None:
        section_header(console, "Linux Learning Center",
                       "Basic → Advanced interactive guide")

        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Topic",       style="bold bright_cyan", min_width=10)
        table.add_column("Icon", justify="center", min_width=4)
        table.add_column("Title",       style="white", min_width=22)
        table.add_column("Commands",    justify="center")
        table.add_column("Progress",    justify="center")

        for key, data in LESSONS.items():
            done  = sum(1 for c in data["commands"]
                        if f"{key}.{c['cmd']}" in self.completed)
            total = len(data["commands"])
            pct   = done / total * 100 if total else 0
            bar   = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            prog  = Text()
            prog.append(f"[{bar}] ", style="bright_green" if pct == 100 else "yellow")
            prog.append(f"{done}/{total}", style="dim")
            table.add_row(key, data["icon"], data["title"], str(total), prog)

        console.print(table)
        console.print()
        console.print("  [dim]Commands: learn <topic> | learn practice | learn quiz | learn cheatsheet | learn progress[/dim]")
        console.print()

    def show_topic(self, console: Console, topic: str) -> None:
        if topic not in LESSONS:
            console.print(f"[red]Unknown topic '{topic}'. Available: {', '.join(LESSONS.keys())}[/red]")
            return

        data  = LESSONS[topic]
        cmds  = data["commands"]
        total = len(cmds)

        section_header(console, f"{data['icon']} {data['title']}",
                       f"{total} commands")

        for i, entry in enumerate(cmds, 1):
            self.completed.add(f"{topic}.{entry['cmd']}")

            console.print(Rule(f"[bold bright_cyan]{i}/{total} — {entry['cmd']}[/bold bright_cyan]",
                               style="bright_cyan"))
            console.print()

            title_t = Text()
            title_t.append(f"  {entry['title']}\n", style="bold bright_white")
            title_t.append(f"  {entry['desc']}", style="white")
            console.print(title_t)
            console.print()

            console.print("  [bold cyan]Example:[/bold cyan]")
            for line in entry["example"].split("\n"):
                console.print(f"  [bold bright_green]$[/bold bright_green] [bright_white]{line}[/bright_white]")

            if entry["output"]:
                console.print()
                console.print("  [bold cyan]Output:[/bold cyan]")
                console.print(
                    Panel(entry["output"], border_style="dim", padding=(0, 2))
                )

            console.print()
            console.print(f"  [bold yellow]💡 Tip:[/bold yellow] [yellow]{entry['tip']}[/yellow]")
            console.print()

            if i < total:
                try:
                    input("  [Press Enter for next command, Ctrl+C to stop] ")
                except (KeyboardInterrupt, EOFError):
                    console.print("\n  [yellow]Lesson paused.[/yellow]\n")
                    return

        console.print(f"\n  [bold bright_green]✓ Completed: {data['title']}![/bold bright_green]\n")

    def practice(self, console: Console, level: str = "all") -> None:
        section_header(console, "Practice Challenges", "Type the correct Linux command")

        if level == "beginner":
            pool = [c for c in CHALLENGES if c["level"] == "Beginner"]
        elif level == "intermediate":
            pool = [c for c in CHALLENGES if c["level"] == "Intermediate"]
        elif level == "advanced":
            pool = [c for c in CHALLENGES if c["level"] == "Advanced"]
        else:
            pool = CHALLENGES

        random.shuffle(pool)
        correct = wrong = 0

        for i, ch in enumerate(pool, 1):
            console.print()
            lvl_style = {"Beginner": "green", "Intermediate": "yellow", "Advanced": "red"}
            lvl_color = lvl_style.get(ch["level"], "white")
            console.print(f"  [{lvl_color}][{ch['level']}][/{lvl_color}]  "
                          f"[bold white]Challenge {i}/{len(pool)}:[/bold white]")
            console.print(f"  [bright_white]{ch['task']}[/bright_white]")
            console.print()

            try:
                ans = input("  $ ").strip()
            except (KeyboardInterrupt, EOFError):
                console.print("\n  [yellow]Practice stopped.[/yellow]")
                break

            if not ans:
                console.print("  [yellow]Skipped.[/yellow]")
                continue

            if any(ans.lower() == a.lower() for a in ch["answers"]):
                console.print("  [bold bright_green]✓ Correct![/bold bright_green]")
                correct += 1
                self.score += 10
            else:
                console.print(f"  [red]✗ Not quite.[/red]  "
                              f"[dim]Hint: {ch['hint']}[/dim]")
                console.print(f"  [dim]Answer: {ch['answers'][0]}[/dim]")
                wrong += 1

        console.print()
        total = correct + wrong
        if total > 0:
            pct = correct / total * 100
            console.print(f"  [bold]Score: {correct}/{total}  ({pct:.0f}%)[/bold]  "
                          f"[dim]+{correct*10} points[/dim]")
        console.print()

    def quiz(self, console: Console) -> None:
        section_header(console, "Linux Knowledge Quiz",
                       "Multiple choice — type the number of your answer")

        questions = random.sample(QUIZ, min(8, len(QUIZ)))
        correct = 0

        for i, q in enumerate(questions, 1):
            console.print()
            console.print(f"  [bold bright_cyan]Q{i}.[/bold bright_cyan] "
                          f"[bold white]{q['q']}[/bold white]")
            for j, opt in enumerate(q["options"]):
                console.print(f"    [cyan]{j}[/cyan]  {opt}")
            console.print()

            try:
                raw = input("  Answer (0/1/2/3): ").strip()
                ans = int(raw)
            except (ValueError, KeyboardInterrupt, EOFError):
                console.print("  [yellow]Skipped.[/yellow]")
                continue

            if ans == q["answer"]:
                console.print("  [bold bright_green]✓ Correct![/bold bright_green]")
                correct += 1
                self.score += 15
            else:
                console.print(f"  [red]✗ Wrong.[/red]  "
                              f"[dim]Correct answer: {q['answer']} — {q['options'][q['answer']]}[/dim]")

        console.print()
        pct = correct / len(questions) * 100
        grade = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "F"
        console.print(f"  [bold]Quiz Result: {correct}/{len(questions)}  "
                      f"({pct:.0f}%)  Grade: {grade}[/bold]")
        console.print()

    def cheatsheet(self, console: Console, filter_key: str = "") -> None:
        section_header(console, "Linux Command Cheatsheet",
                       "Quick reference for all commands")

        for key, data in LESSONS.items():
            if filter_key and filter_key != key:
                continue

            console.print(f"\n  {data['icon']}  [bold bright_cyan]{data['title'].upper()}[/bold bright_cyan]")
            table = Table(box=box.SIMPLE, show_header=True,
                          header_style="bold white", padding=(0, 1))
            table.add_column("Command",     style="bold bright_green", min_width=16)
            table.add_column("Description", style="white")
            table.add_column("Key Flag",    style="dim cyan")

            for c in data["commands"]:
                flag = ""
                ex   = c["example"].split("\n")[0]
                if " -" in ex:
                    flag = ex.split(" -", 1)[1].split(" ")[0]
                    flag = f"-{flag.split()[0]}"
                table.add_row(c["cmd"], c["title"], flag)
            console.print(table)

        console.print()

    def progress(self, console: Console) -> None:
        section_header(console, "Your Progress")

        done  = len(self.completed)
        total = self.total_lessons
        pct   = done / total * 100 if total else 0
        bar   = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))

        console.print(f"\n  [bold cyan]Lessons Completed:[/bold cyan]  "
                      f"[bold bright_green]{bar}[/bold bright_green]  "
                      f"[white]{done}/{total}  ({pct:.0f}%)[/white]")
        console.print(f"  [bold cyan]Total Score:[/bold cyan]       "
                      f"[bold yellow]{self.score} points[/bold yellow]")
        console.print()

        table = Table(box=box.ROUNDED, border_style="bright_cyan",
                      header_style="bold white on dark_blue", show_lines=True)
        table.add_column("Topic", style="bold bright_cyan")
        table.add_column("Progress", justify="center")
        table.add_column("Status",   justify="center")

        for key, data in LESSONS.items():
            done_t = sum(1 for c in data["commands"]
                         if f"{key}.{c['cmd']}" in self.completed)
            total_t = len(data["commands"])
            pct_t   = done_t / total_t * 100 if total_t else 0
            b       = "█" * int(pct_t / 10) + "░" * (10 - int(pct_t / 10))
            status  = "[green]✓ Done[/green]" if pct_t == 100 else (
                      "[yellow]In Progress[/yellow]" if done_t > 0 else "[dim]Not Started[/dim]")
            table.add_row(
                f"{data['icon']} {data['title']}",
                Text(f"[{b}] {done_t}/{total_t}", style="bright_green" if pct_t == 100 else "yellow"),
                Text.from_markup(status),
            )
        console.print(table)
        console.print()


def handle_learn(args: list[str], learn: LearnModule, console: Console) -> None:
    if not args:
        learn.show_menu(console)
        return

    sub = args[0].lower()

    if sub == "list":
        learn.show_menu(console)

    elif sub in LESSONS:
        learn.show_topic(console, sub)

    elif sub == "practice":
        level = args[1].lower() if len(args) > 1 else "all"
        learn.practice(console, level)

    elif sub == "quiz":
        learn.quiz(console)

    elif sub == "cheatsheet":
        fkey = args[1].lower() if len(args) > 1 else ""
        learn.cheatsheet(console, fkey)

    elif sub == "progress":
        learn.progress(console)

    else:
        console.print(f"[red]Unknown: '{sub}'[/red]")
        console.print("[dim]Usage: learn | learn <basic|files|text|permissions|process|system|network|pipes|advanced>[/dim]")
        console.print("[dim]       learn practice [beginner|intermediate|advanced][/dim]")
        console.print("[dim]       learn quiz | learn cheatsheet | learn progress[/dim]")
