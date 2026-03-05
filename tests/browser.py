from collections import defaultdict
from urllib.parse import urlparse

from conftest import BASE
from playwright.sync_api import Page


def test_all_pages_no_browser_errors(page: Page):
    visited = set()
    to_visit = [BASE + "/"]
    errors_by_page: dict[str, list[str]] = defaultdict(list)

    def is_internal(url: str) -> bool:
        return urlparse(url).netloc == urlparse(BASE).netloc

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        console_errors: list[str] = []
        page.on(
            "console",
            # lambda msg: console_errors.append(msg.text)
            lambda msg: (
                print("[console error]", msg.text)
                if msg.type == "error"
                else None
            ),
        )
        # page.on("pageerror", lambda err: console_errors.append(str(err)))

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

    assert not errors_by_page, "\n".join(
        f"{url}:\n" + "\n".join(f"  - {e}" for e in errs)
        for url, errs in errors_by_page.items()
    )
