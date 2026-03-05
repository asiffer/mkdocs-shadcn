from collections import defaultdict
from typing import Dict, List
from urllib.parse import urlparse, urlunparse

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

    base_url = urlparse(BASE)
    # def is_internal(url: str) -> bool:
    #     return urlparse(url).netloc == urlparse(BASE).netloc

    def catch_console_error(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    while to_visit:
        url = to_visit.pop()
        if url in visited:
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
            normalized = urlparse(href)
            if normalized.scheme not in ["http", "https"]:
                continue
            normalized = normalized._replace(fragment="")
            if normalized.path.endswith("/"):
                normalized = normalized._replace(
                    path=normalized.path + "index.html"
                )
            link = urlunparse(normalized)
            if normalized.netloc == base_url.netloc and link not in visited:
                to_visit.append(link)

    assert not errors_by_page, format_errors(errors_by_page)
