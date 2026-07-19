import logging
import os
import re
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from random import randbytes
from socketserver import BaseRequestHandler
from subprocess import CalledProcessError
from typing import Any, Protocol

import pytest

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
        with open(PAGES_DIR / "test.mkdocs.yml", "w") as test:
            with open(PAGES_DIR / "mkdocs.yml", "r") as original:
                test.write(
                    site_url_re.sub(f"site_url: {BASE}", original.read())
                )

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


@pytest.fixture
def shadcn_project(tmp_path: Path) -> Path:
    """A fresh uv-managed python project with mkdocs, shadcn theme (local)
    and git-initialized."""
    project_dir = tmp_path / "docsite"
    project_dir.mkdir()

    logger.info("Init new uv project")
    _run(["uv", "init", "--no-readme", "."], cwd=project_dir)
    _run(["uv", "add", "mkdocs[i18n]"], cwd=project_dir)

    logger.info("Init mkdocs project")
    # it creates also git repo
    _run(["uv", "run", "mkdocs", "new", "."], cwd=project_dir)

    with open(project_dir / "mkdocs.yml", "w") as config_file:
        config_file.write("site_name: Testing docs\n")
        config_file.write("theme:\n")
        config_file.write("    name: null\n")
        config_file.write(f"    custom_dir: {THEME_PATH}\n")

    _run(
        ["git", "config", "user.email", "mkdocs-shadcn@github.com"],
        cwd=project_dir,
    )
    _run(["git", "config", "user.name", "Mkdocs Shadcn"], cwd=project_dir)

    logger.info("First commit")
    _run(["git", "add", "-A"], cwd=project_dir)
    _run(["git", "commit", "-m", "chore: initial project"], cwd=project_dir)
    # test build is ok
    logger.info("First build...")
    _run(["uv", "run", "mkdocs", "build"], cwd=project_dir)

    return project_dir
