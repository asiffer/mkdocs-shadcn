import pytest
from bs4 import BeautifulSoup
from conftest import _uv_run, update_mkdocs_config

from shadcn.plugins.autonumber import DEFAULT_PREFIXES


@pytest.fixture
def project_with_autonumber_plugin(shadcn_project: str):
    update_mkdocs_config(
        shadcn_project,
        {"plugins": ["autonumber"]},
    )
    return shadcn_project


def test_base_reference_in_html(project_with_autonumber_plugin: str):
    project = project_with_autonumber_plugin

    with open(f"{project}/docs/label.md", "a") as f:
        for ref, label in DEFAULT_PREFIXES.items():
            f.write("\n\n")
            f.write(f"{{#{ref}:my{label.lower()}}}\n")

    with open(f"{project}/docs/reference.md", "a") as f:
        for ref, label in DEFAULT_PREFIXES.items():
            f.write("\n\n")
            f.write(f"Look at @{ref}:my{label.lower()}\n")

    # build the project
    _uv_run(["mkdocs", "build"], cwd=project)

    # check links
    with open(f"{project}/site/reference/index.html", "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", {"class": "autonumber"})
    expected = {
        f"../label#{ref}:my{label.lower()}"
        for ref, label in DEFAULT_PREFIXES.items()
    }
    hrefs = {a.attrs.get("href") for a in links}

    assert hrefs == expected, f"Expected {expected}, but got {hrefs}"

    # check numbering
    numbers = {a.text for a in links}
    expected_numbers = {
        f"{label.lower()} 1" for label in DEFAULT_PREFIXES.values()
    }
    assert numbers == expected_numbers, (
        f"Expected {expected_numbers}, but got {numbers}"
    )


def test_unknown_prefix(project_with_autonumber_plugin: str):
    project = project_with_autonumber_plugin

    with open(f"{project}/docs/all.md", "a") as f:
        f.write("\n\n")
        f.write("Label {#unknown:mything}\n")
        f.write("Reference to @unknown2:mything2\n")

    # build the project
    _uv_run(["mkdocs", "build"], cwd=project)

    # check that references and labels are not replaced
    with open(f"{project}/site/all/index.html", "r") as f:
        html = f.read()
        assert "Label {#unknown:mything}" in html
        assert "Reference to @unknown2:mything2" in html


def test_custom_prefix(project_with_autonumber_plugin: str):
    project = project_with_autonumber_plugin
    update_mkdocs_config(
        project, {"plugins": {"autonumber": {"prefixes": {"xxx": "Cool"}}}}
    )

    prefixes = {**DEFAULT_PREFIXES, "xxx": "Cool"}

    with open(f"{project}/docs/label.md", "a") as f:
        for ref, label in prefixes.items():
            f.write("\n\n")
            f.write(f"{{#{ref}:my{label.lower()}}}\n")

    with open(f"{project}/docs/reference.md", "a") as f:
        for ref, label in prefixes.items():
            f.write("\n\n")
            f.write(f"Look at @{ref}:my{label.lower()}\n")

    # build the project
    _uv_run(["mkdocs", "build"], cwd=project)

    # check links
    with open(f"{project}/site/reference/index.html", "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", {"class": "autonumber"})
    expected = {
        f"../label#{ref}:my{label.lower()}" for ref, label in prefixes.items()
    }
    hrefs = {a.attrs.get("href") for a in links}

    assert hrefs == expected, f"Expected {expected}, but got {hrefs}"


def test_uppercase_and_numbering(project_with_autonumber_plugin: str):
    project = project_with_autonumber_plugin

    with open(f"{project}/docs/label.md", "a") as f:
        f.write("\n\n")
        f.write("{#fig:myfigure}\n")
        f.write("{#fig:myfigure2}\n")

    with open(f"{project}/docs/reference.md", "a") as f:
        f.write("\n\n")
        f.write("Look at @Fig:myfigure and @fig:myfigure2\n")

    # build the project
    _uv_run(["mkdocs", "build"], cwd=project)

    # check links
    with open(f"{project}/site/reference/index.html", "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", {"class": "autonumber"})
    expected = {
        "../label#fig:myfigure",
        "../label#fig:myfigure2",
    }
    hrefs = {a.attrs.get("href") for a in links}

    assert hrefs == expected, f"Expected {expected}, but got {hrefs}"

    # check numbering
    numbers = {a.text for a in links}
    expected_numbers = {"Figure 1", "figure 2"}
    assert numbers == expected_numbers, (
        f"Expected {expected_numbers}, but got {numbers}"
    )
