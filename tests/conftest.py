from __future__ import annotations

import logging
import os
import re
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from random import randbytes, randint
from socketserver import BaseRequestHandler
from subprocess import CalledProcessError
from typing import Any, Protocol

import pytest
import yaml

from internal.common import THEME_PATH

PAGES_DIR = Path(__file__).parent.parent / "pages"
SITE_DIR = Path(__file__).parent / "_site"

HOST, PORT = "127.0.0.1", 8081
BASE = f"http://{HOST}:{PORT}"

site_url_re = re.compile(r"^site_url:.*$", re.MULTILINE)


logger = logging.getLogger(__name__)


def upload_folder() -> Path:
    up = Path(__file__).parent / ".pytest"
    if not up.exists():
        os.makedirs(up)
    return up


def find_mkdocs_config(root: str | Path) -> Path:
    """Find the mkdocs.yml file in the given directory or its parents"""
    root = Path(root)
    for parent in [root] + list(root.parents):
        for file in ["mkdocs.yml", "mkdocs.yaml"]:
            mkdocs_file = parent / file
            if mkdocs_file.exists():
                return mkdocs_file

    raise FileNotFoundError(f"mkdocs.yml not found in {root} or its parents")


def update_mkdocs_config(cwd: str | Path, extra_config: dict):
    """Update the mkdocs.yml file in the given directory with the extra config"""
    mkdocs_file = find_mkdocs_config(cwd)
    # Ouvrir le fichier YAML en mode lecture
    with open(mkdocs_file, "r") as file:
        # Charger le contenu du fichier en tant que dictionnaire Python
        config = yaml.safe_load(file)
        config.update(extra_config)

    with open(mkdocs_file, "w") as file:
        yaml.dump(config, file)


@pytest.fixture(scope="session")
def random_upload_folder():
    path = upload_folder() / randbytes(3).hex()
    yield path
    logger.warning(f"File stored in {path}")


def _run(
    args: list[str],
    cwd: str | Path | None = None,
    check: bool = True,
    **kwargs,
):
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
            **kwargs,
        )
    except CalledProcessError as err:
        raise RuntimeError(
            f"Command failed ({err.returncode}): {' '.join(args)}\n"
            f"cwd: {cwd}\n"
            f"--- output ---\n{err.output}\n"
            f"--- stderr ---\n{err.stderr}"
        ) from err
    return result


def _uv_run(
    args: list[str],
    cwd: str | Path | None = None,
    check: bool = True,
    **kwargs,
):
    return _run(["uv", "run"] + args, cwd=cwd, check=check, **kwargs)


class Handler(Protocol):
    def __call__(
        self, request: Any, client_address: Any, server: HTTPServer, /
    ) -> BaseRequestHandler: ...


class FileHandler:
    def __init__(self, directory: str | Path):
        self.directory = directory

    def __call__(self, *args, **kwargs):
        return SimpleHTTPRequestHandler(
            *args, directory=self.directory, **kwargs
        )


def http_server(
    handler: Handler = SimpleHTTPRequestHandler,
    host: str = HOST,
    port: int = PORT,
) -> HTTPServer:
    server = HTTPServer((host, port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


@pytest.fixture
def local_deployment():
    """Build the current pages into a local site and serve them"""
    if not SITE_DIR.exists():
        logger.info("Modifying mkdocs.yml...")
        # copy a modified mkdocs.yml with the correct site_url to the test directory and build the site
        with open(PAGES_DIR / "test.mkdocs.yml", "w") as test, open(
            PAGES_DIR / "mkdocs.yml", "r"
        ) as original:
            test.write(site_url_re.sub(f"site_url: {BASE}", original.read()))

        logger.info("Building site...")
        _run(
            [
                "uv",
                "run",
                "mkdocs",
                "build",
                "--config-file",
                str(PAGES_DIR / "test.mkdocs.yml"),
                "--site-dir",
                str(SITE_DIR),
            ],
        )

    # run fileserver
    logger.info("Starting file server...")
    server = http_server(handler=FileHandler(SITE_DIR))

    yield f"http://{server.server_address[0]}:{server.server_address[1]}"

    logger.info("Shutting down file server...")
    server.shutdown()
    if (PAGES_DIR / "test.mkdocs.yml").exists():
        logger.info("Cleaning up test.mkdocs.yml...")
        os.unlink(PAGES_DIR / "test.mkdocs.yml")


class ShadcnProject:
    path: Path

    def __init__(self, path: str | Path):
        self.path = Path(path) / "docsite"

    def __fspath__(self):
        return str(self.path)

    def __str__(self):
        return str(self.path)

    @property
    def site_dir(self) -> Path:
        return self.path / "site"

    @property
    def site_name(self) -> str:
        return "Testing pages"

    @property
    def site_description(self) -> str:
        return "Website to test the mkdocs-shadcn theme"

    def init(self):
        self.path.mkdir()

        logger.info("Init new uv project")
        _run(["uv", "init", "--no-readme", "."], cwd=self.path)
        _run(["uv", "add", "mkdocs[i18n]"], cwd=self.path)

        logger.info("Install shadcn theme from local path")
        _run(["uv", "add", str(THEME_PATH.parent)], cwd=self.path)

        logger.info("Init mkdocs project")
        # it creates also git repo
        _uv_run(["mkdocs", "new", "."], cwd=self.path)
        self.update_config(
            {
                "site_name": self.site_name,
                "site_description": self.site_description,
                "theme": {"name": "shadcn"},
            }
        )

    def _init_git(
        self,
        user_email: str = "mkdocs-shadcn@github.com",
        user_name: str = "Mkdocs Shadcn",
    ):
        if not (self.path / ".git").exists():
            _run(["git", "init"], cwd=self.path)
        _run(["git", "config", "user.email", user_email], cwd=self.path)
        _run(["git", "config", "user.name", user_name], cwd=self.path)
        _run(["git", "add", "-A"], cwd=self.path)
        _run(["git", "commit", "-m", "chore: initial project"], cwd=self.path)

    def build(self):
        _uv_run(["mkdocs", "build"], cwd=self.path)

    def update_config(self, extra_config: dict):
        update_mkdocs_config(self.path, extra_config)

    def write_file(
        self,
        relpath: str | Path,
        content: str,
        options: dict | None = None,
    ):
        file_path = self.path / "docs" / relpath
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            if options:
                f.write("---\n")
                yaml.dump(options, f)
                f.write("\n---\n\n")
            f.write(content)

    def get_built_file(self, relpath: str | Path) -> Path:
        if isinstance(relpath, str):
            relpath = Path(relpath)

        if relpath.name in {"index.md", "index.html"}:
            return self.site_dir / relpath.with_suffix(".html")
        return self.site_dir / relpath.with_suffix("") / "index.html"


@pytest.fixture
def shadcn_project(tmp_path: Path) -> ShadcnProject:
    project = ShadcnProject(tmp_path)
    project.init()
    project._init_git()
    project.build()
    return project


@pytest.fixture
def random_port() -> int:
    return randint(20000, 40000)
