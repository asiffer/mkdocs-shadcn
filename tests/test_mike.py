from dataclasses import dataclass
from pathlib import Path

import pytest
from conftest import FileHandler, _run, _uv_run, http_server, logger
from playwright.sync_api import (
    Browser,
    ConsoleMessage,
    Error,
    ViewportSize,
    expect,
)

full_hd = ViewportSize(width=1920, height=1080)


@dataclass
class MikeDeployments:
    url: str
    default_version: str
    versions: list[str]

    def version_url(
        self, index: int | None = None, version: str | None = None
    ):
        if index is not None:
            return f"{self.url}/{self.versions[0]}/"
        elif version is not None:
            return self.version_url(self.versions.index(version))
        else:
            return self.version_url(self.versions.index(self.default_version))


@pytest.fixture
def mike_deployments(
    shadcn_project: Path,
    request: pytest.FixtureRequest,
):
    versions: list[str] = request.param or ["1.0", "2.0"]
    if len(versions) == 0:
        raise pytest.UsageError(
            "mike_deployments fixture requires an non empty list of versions"
        )

    initial_version = versions.pop(0)
    default_version = initial_version

    _run(["uv", "add", "mike"], cwd=shadcn_project)
    _run(["git", "add", "-u"], cwd=shadcn_project)
    _run(["git", "commit", "-m", "add mike"], cwd=shadcn_project)

    _uv_run(
        ["mike", "deploy", initial_version, "latest"],
        cwd=shadcn_project,
    )
    _uv_run(["mike", "set-default", "latest"], cwd=shadcn_project)

    for version in versions:
        with open(shadcn_project / "docs" / "index.md", "a") as index:
            index.write("\n\n")
            index.write(f"## What's new in v{version}\n")

        _run(["git", "add", "docs/index.md"], cwd=shadcn_project)
        _run(["git", "commit", "-m", f"v{version}"], cwd=shadcn_project)

        _uv_run(
            ["mike", "deploy", "-u", version, "latest"],
            cwd=shadcn_project,
        )
        default_version = version

    _run(
        ["git", "checkout", "gh-pages"],
        cwd=shadcn_project,
    )

    server = http_server(port=5000, handler=FileHandler(shadcn_project))

    yield MikeDeployments(
        url=f"http://{server.server_address[0]}:{server.server_address[1]}",
        versions=[initial_version] + versions,
        default_version=default_version,
    )

    logger.info("Shutting down file server...")
    server.shutdown()


def console_error_handler(msg: ConsoleMessage):
    if msg.type == "error":
        assert False, msg


def page_error_handler(err: Error):
    assert False, err


@pytest.mark.parametrize(
    "mike_deployments",
    [["0.1.0", "0.1.1", "2.0.0"]],
    indirect=True,
)
def test_mike_deployments(
    mike_deployments: MikeDeployments,
    browser: Browser,
    random_upload_folder: Path,
):
    logger.info(f"Versions to tests: {mike_deployments.versions}")
    # page_wait_seconds = 2
    context = browser.new_context(
        screen=full_hd,
        viewport=full_hd,
        record_har_path=random_upload_folder / "records.har",
    )
    page = context.new_page()

    try:
        logger.debug(f"versions: {mike_deployments.versions}")
        page.on("pageerror", page_error_handler)
        page.on("console", console_error_handler)

        logger.info(f"Navigating to {mike_deployments.version_url(0)}")
        page.goto(
            mike_deployments.version_url(0),
            wait_until="networkidle",
        )
        assert mike_deployments.versions[0] in page.url, page.url

        for version in mike_deployments.versions[1:]:
            page.bring_to_front()
            logger.info(f"Selecting version {version}")
            with page.expect_navigation(wait_until="load"):
                page.select_option("#version-selector", version)

            page.wait_for_selector("#version-selector")
            expect(page.locator("#version-selector")).to_have_value(version)
            assert version in page.url, page.url

    finally:
        page.close()
        context.close()
