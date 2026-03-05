from collections import defaultdict
from typing import Dict, List
from urllib.parse import urlparse

from conftest import BASE
from playwright.sync_api import Page


def format_errors(errors_by_page: Dict[str, List[str]]) -> str:
    if len(errors_by_page) == 0:
        return ""
    out = ""
    for url, errs in errors_by_page.items():
        out += f"{url} ({len(errs)}):\n"
        for e in errs:
            out += f"\t- {e}\n"
    return out


def test_all_pages_no_browser_errors(page: Page):
    visited = set()
    to_visit = [BASE + "/"]
    errors_by_page: Dict[str, List[str]] = defaultdict(list)

    def is_internal(url: str) -> bool:
        return urlparse(url).netloc == urlparse(BASE).netloc

    def catch_console_error(msg):
        print(msg.__dict__)
        if msg.type == "error":
            console_errors.append(msg.text)

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        if url.endswith("index.html/"):
            # ignore trailing slash on index.html
            continue

        visited.add(url)

        console_errors: list[str] = []
        page.on(
            "console",
            lambda msg: (
                console_errors.append(msg.text)
                if msg.type == "error"
                else None
            ),
        )
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        page.goto(url, wait_until="networkidle")

        if console_errors:
            errors_by_page[url].extend(console_errors)

        # Collect internal links
        anchors = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => e.href)"
        )
        for href in anchors:
            normalized = href.split("#")[0].rstrip("/") + "/"
            if is_internal(normalized) and normalized not in visited:
                to_visit.append(normalized)

    assert not errors_by_page, format_errors(errors_by_page)
