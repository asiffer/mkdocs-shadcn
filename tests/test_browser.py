import json
from collections import defaultdict
from typing import Dict, List, Union
from urllib.parse import urlparse, urlunparse

from conftest import BASE
from playwright.sync_api import ConsoleMessage, Error, Page

BrowserError = Union[ConsoleMessage, Error]


def format_errors(errors_by_page: Dict[str, List[BrowserError]]) -> str:
    if len(errors_by_page) == 0:
        return ""
    out = ""
    for url, errs in errors_by_page.items():
        out += f"😱 {url} ({len(errs)}):\n"
        for e in errs:
            if isinstance(e, ConsoleMessage):
                out += json.dumps(
                    {
                        "text": e.text,
                        "url": e.location["url"] if e.location else "",
                        "lineNumber": e.location["lineNumber"]
                        if e.location
                        else None,
                        "columnNumber": e.location["columnNumber"]
                        if e.location
                        else None,
                    },
                    indent=2,
                )
            elif isinstance(e, Error):
                out += json.dumps(
                    {
                        "name": e.name,
                        "message": e.message,
                        "stack": e.stack.replace("\n", "").replace("  ", " ")
                        if e.stack
                        else "",
                        "args": e.args,
                    },
                    indent=2,
                )
            out += "\n"
    return out


# fixtures: see https://playwright.dev/python/docs/test-runners#fixtures
def test_all_pages_no_browser_errors(page: Page):
    visited = set()
    to_visit = [BASE + "/"]
    errors_by_page: Dict[str, List[BrowserError]] = defaultdict(list)

    base_url = urlparse(BASE)
    errors: List[BrowserError] = []

    def console_error_handler(msg: ConsoleMessage):
        if msg.type == "error":
            # err: Dict[str, Any] = {}
            # if msg.location:
            #     err: Dict[str, Any] = dict(msg.location.items())
            # err["text"] = msg.text
            errors.append(msg)

    def page_error_handler(err: Error):
        errors.append(err)
        # print(err.args)
        # print(err.stack.replace("\n", ""))
        # print(err.name)
        # print(err.message)

    # page.on(
    #     "console",
    #     lambda msg: (
    #         print(type(msg), msg.args, msg.location)
    #         if msg.type == "error"
    #         else None
    #     ),
    # )
    page.on(
        "console",
        console_error_handler,
    )
    page.on("pageerror", page_error_handler)

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue

        visited.add(url)

        errors.clear()
        page.goto(url, wait_until="networkidle")

        if errors:
            errors_by_page[url].extend(errors)

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
