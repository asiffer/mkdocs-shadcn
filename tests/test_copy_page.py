from __future__ import annotations

import os
from pathlib import Path

from conftest import BASE, SITE_DIR, FileHandler, _run, http_server
from playwright.sync_api import Page, expect


def test_copy_page_button_uses_site_url(page: Page, local_deployment: str):
    page.goto(local_deployment + "/", wait_until="domcontentloaded")

    button = page.locator("#copy-page").first
    expect(button).to_be_visible()

    onclick = button.get_attribute("onclick") or ""
    assert f"{BASE}/index.md" in onclick, onclick

    # check that the md file is in the build directory
    assert os.path.exists(SITE_DIR / "index.md"), (
        "index.md not found in build directory"
    )


def test_md_files_are_copied_to_build_dir(local_deployment: str):
    # check that the md file is in the build directory
    for root, dirs, files in os.walk(SITE_DIR):
        for name in files:
            if name == "404.html":
                continue
            elif name == "index.html":
                if root == str(SITE_DIR):
                    continue

                md = Path(root).parent / (Path(root).name + ".md")
                assert md.exists(), (
                    f"{md} does not exist (root: {root}, files: {files}, name: {name})"
                )
            elif name.endswith(".html"):
                md = Path(root) / name.replace(".html", ".md")
                assert md.exists(), (
                    f"{md} does not exist (root: {root}, files: {files}, name: {name})"
                )


def test_copy_page_button_is_hidden(
    page: Page,
    shadcn_project: str,
    random_port: int,
):
    with open(f"{shadcn_project}/mkdocs.yml", "a") as f:
        f.write("    hide_source_files: true\n")

    _run(["uv", "run", "mkdocs", "build"], cwd=shadcn_project)
    server = http_server(
        handler=FileHandler(Path(shadcn_project) / "site"),
        port=random_port,
    )
    page.goto(
        f"http://{server.server_address[0]}:{server.server_address[1]}/",
        wait_until="domcontentloaded",
    )
    button = page.locator("#copy-page").first
    expect(button).to_be_hidden()
