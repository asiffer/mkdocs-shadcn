from bs4 import BeautifulSoup

from tests.conftest import ShadcnProject

LINKS = {
    "English": "/en/",
    "Blog": "blog/",
    "GitHub": "https://github.com/asiffer/mkdocs-shadcn",
}


def _soup(project: ShadcnProject, relpath: str) -> BeautifulSoup:
    return BeautifulSoup(
        project.get_built_file(relpath).read_text(), "html.parser"
    )


def test_topbar_links(shadcn_project: ShadcnProject):
    # nothing is rendered by default
    soup = _soup(shadcn_project, "index.md")
    labels = {a.get_text(strip=True) for a in soup.find_all("a")}
    assert labels.isdisjoint(LINKS)

    shadcn_project.update_config(
        {"theme": {"name": "shadcn", "topbar_links": LINKS}}
    )
    shadcn_project.write_file("a/b.md", "# B\n")
    shadcn_project.build()

    soup = _soup(shadcn_project, "a/b.md")
    header = soup.find("header")
    bottom_sidebar = soup.find("dialog", id="bottom-sidebar")
    assert header is not None
    assert bottom_sidebar is not None

    expected = {
        "English": "/en/",  # absolute path kept as is
        "Blog": "../../blog/",  # relative to the site root
        "GitHub": "https://github.com/asiffer/mkdocs-shadcn",
    }
    for container in (header, bottom_sidebar):
        anchors = {
            a.get_text(strip=True): a["href"]
            for a in container.find_all("a")
            if a.get_text(strip=True) in LINKS
        }
        assert anchors == expected


def test_topbar_links_override(shadcn_project: ShadcnProject):
    custom_dir = shadcn_project.path / "custom_theme" / "templates"
    custom_dir.mkdir(parents=True)
    (custom_dir / "header_links.html").write_text(
        '<a id="custom-link" class="button ghost" href="/fr/">Français</a>'
    )
    shadcn_project.update_config(
        {"theme": {"name": "shadcn", "custom_dir": "custom_theme"}}
    )
    shadcn_project.build()

    header = _soup(shadcn_project, "index.md").find("header")
    assert header is not None
    assert header.find("a", id="custom-link") is not None
