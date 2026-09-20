from __future__ import annotations

from pathlib import Path

from conftest import BASE, FileHandler, _run, http_server
from playwright.sync_api import Page, expect


def test_copy_page_button_uses_site_url(page: Page, local_deployment: str):
    page.goto(local_deployment + "/", wait_until="domcontentloaded")

    button = page.locator("#copy-page").first
    expect(button).to_be_visible()

    onclick = button.get_attribute("onclick") or ""
    assert f"{BASE}/index.md" in onclick, onclick


def test_copy_page_button_is_hidden(page: Page, shadcn_project: str):
    with open(f"{shadcn_project}/mkdocs.yml", "a") as f:
        f.write("    hide_source_files: true\n")

    _run(["uv", "run", "mkdocs", "build"], cwd=shadcn_project)
    server = http_server(handler=FileHandler(Path(shadcn_project) / "site"))
    page.goto(
        f"http://{server.server_address[0]}:{server.server_address[1]}/",
        wait_until="domcontentloaded",
    )
    button = page.locator("#copy-page").first
    expect(button).to_be_hidden()
