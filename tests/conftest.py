import logging
import os
import re
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pytest

PAGES_DIR = Path(__file__).parent.parent / "pages"
SITE_DIR = Path(__file__).parent / "_site"
HOST, PORT = "127.0.0.1", 8080
BASE = f"http://{HOST}:{PORT}"

site_url_re = re.compile(r"^site_url:.*$", re.MULTILINE)


logger = logging.getLogger(__name__)


def handler(*args, **kwargs):
    return SimpleHTTPRequestHandler(*args, directory=str(SITE_DIR), **kwargs)


@pytest.fixture(scope="session", autouse=True)
def fileserver():
    if not SITE_DIR.exists():
        logger.info("Modifying mkdocs.yml...")
        # copy a modified mkdocs.yml with the correct site_url to the test directory and build the site
        with open(PAGES_DIR / "test.mkdocs.yml", "w") as test:
            with open(PAGES_DIR / "mkdocs.yml", "r") as original:
                test.write(
                    site_url_re.sub(f"site_url: {BASE}", original.read())
                )

        logger.info("Building site...")
        subprocess.run(
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
            check=True,
        )

    # run fileserver
    logger.info("Starting file server...")
    server = HTTPServer((HOST, PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://{HOST}:{PORT}"

    logger.info("Shutting down file server...")
    server.shutdown()
    if (PAGES_DIR / "test.mkdocs.yml").exists():
        logger.info("Cleaning up test.mkdocs.yml...")
        os.unlink(PAGES_DIR / "test.mkdocs.yml")
