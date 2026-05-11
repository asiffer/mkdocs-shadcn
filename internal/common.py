import re
from pathlib import Path

import rich

BASE_PATH = Path(__file__).parent.parent
THEME_PATH = BASE_PATH / "shadcn"


def error(msg):
    rich.print(f"[bold red]{msg}[/bold red]")


def log(msg):
    rich.print(f"[dim]{msg}[/dim]")


def info(msg):
    rich.print(f"{msg}")


def version():
    version_regex = re.compile(r"^version\s*=\s*['\"]([^'\"]+)['\"]")
    with open(BASE_PATH / "pyproject.toml", "r") as f:
        for line in f:
            match = version_regex.match(line)
            if match:
                return match.group(1)
    raise ValueError("Version not found in pyproject.toml")
