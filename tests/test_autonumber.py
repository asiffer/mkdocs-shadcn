import pytest
from bs4 import BeautifulSoup
from conftest import ShadcnProject

from shadcn.plugins.autonumber import DEFAULT_PREFIXES


@pytest.fixture
def project_with_autonumber_plugin(
    shadcn_project: ShadcnProject,
) -> ShadcnProject:
    shadcn_project.update_config({"plugins": ["autonumber"]})
    return shadcn_project


def test_base_reference_in_html(project_with_autonumber_plugin: ShadcnProject):
    project = project_with_autonumber_plugin

    labels = "".join(
        f"\n\n{{#{ref}:my{label.lower()}}}\n"
        for ref, label in DEFAULT_PREFIXES.items()
    )
    references = "".join(
        f"\n\nLook at @{ref}:my{label.lower()}\n"
        for ref, label in DEFAULT_PREFIXES.items()
    )
    project.write_file("label.md", labels)
    project.write_file("reference.md", references)

    project.build()

    # check links
    with open(project.get_built_file("reference/index.html"), "r") as f:
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


def test_unknown_prefix(project_with_autonumber_plugin: ShadcnProject):
    project = project_with_autonumber_plugin

    project.write_file(
        "all.md",
        "\n\nLabel {#unknown:mything}\nReference to @unknown2:mything2\n",
    )

    project.build()

    # check that references and labels are not replaced
    with open(project.get_built_file("all/index.html"), "r") as f:
        html = f.read()
        assert "Label {#unknown:mything}" in html
        assert "Reference to @unknown2:mything2" in html


def test_custom_prefix(project_with_autonumber_plugin: ShadcnProject):
    project = project_with_autonumber_plugin
    project.update_config(
        {"plugins": {"autonumber": {"prefixes": {"xxx": "Cool"}}}}
    )

    prefixes = {**DEFAULT_PREFIXES, "xxx": "Cool"}

    labels = "".join(
        f"\n\n{{#{ref}:my{label.lower()}}}\n"
        for ref, label in prefixes.items()
    )
    references = "".join(
        f"\n\nLook at @{ref}:my{label.lower()}\n"
        for ref, label in prefixes.items()
    )
    project.write_file("label.md", labels)
    project.write_file("reference.md", references)

    project.build()

    # check links
    with open(project.get_built_file("reference/index.html"), "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", {"class": "autonumber"})
    expected = {
        f"../label#{ref}:my{label.lower()}" for ref, label in prefixes.items()
    }
    hrefs = {a.attrs.get("href") for a in links}

    assert hrefs == expected, f"Expected {expected}, but got {hrefs}"


def test_uppercase_and_numbering(
    project_with_autonumber_plugin: ShadcnProject,
):
    project = project_with_autonumber_plugin

    project.write_file("label.md", "\n\n{#fig:myfigure}\n{#fig:myfigure2}\n")
    project.write_file(
        "reference.md",
        "\n\nLook at @Fig:myfigure and @fig:myfigure2\n",
    )

    project.build()

    # check links
    with open(project.get_built_file("reference/index.html"), "r") as f:
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
