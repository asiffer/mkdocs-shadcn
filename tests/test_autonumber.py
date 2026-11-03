from __future__ import annotations

from shadcn.plugins.autonumber import AutoNumberPlugin, AutoNumberPluginConfig


def _reference_pattern():
    cfg = AutoNumberPluginConfig()
    cfg.load_dict({})
    errs, _warns = cfg.validate()
    assert errs == []
    return cfg.reference_pattern()


def test_reference_pattern_ignores_trailing_period():
    pat = _reference_pattern()
    match = pat.search("See @fig:name.")
    assert match is not None
    assert match.group(0) == "@fig:name"
    assert match.group(2) == "name"


def test_reference_pattern_ignores_trailing_paren_and_comma():
    pat = _reference_pattern()
    for text, expected_id in (
        ("(see @fig:name)", "name"),
        ("@fig:name,", "name"),
        ("@fig:name).", "name"),
    ):
        match = pat.search(text)
        assert match is not None, text
        assert match.group(2) == expected_id, text


def test_reference_pattern_keeps_internal_dots():
    pat = _reference_pattern()
    match = pat.search("See @fig:my.figure.")
    assert match is not None
    assert match.group(0) == "@fig:my.figure"
    assert match.group(2) == "my.figure"


def test_on_page_markdown_resolves_refs_with_trailing_punct(tmp_path):
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import File
    from mkdocs.structure.pages import Page

    from shadcn.plugins.autonumber import AutoNumberEntry

    plugin = AutoNumberPlugin()
    plugin.config = AutoNumberPluginConfig()
    plugin.config.load_dict({})
    assert plugin.config.validate()[0] == []
    plugin.on_config(MkDocsConfig())

    page_file = File(
        "page.md",
        str(tmp_path),
        str(tmp_path / "site"),
        use_directory_urls=True,
    )
    page_file.content_string = "Label {#fig:diagram}"
    entry = AutoNumberEntry(
        file=page_file,
        anchor="fig:diagram",
        number=1,
        prefix="fig",
    )
    plugin.registry["diagram"] = entry
    plugin.replace["{#fig:diagram}"] = (
        '<span id="fig:diagram" class="autonumber fig">Figure 1</span>'
    )

    page = Page(None, page_file, MkDocsConfig())
    out = plugin.on_page_markdown(
        "As shown in @fig:diagram. Also (@fig:diagram).",
        page=page,
        config=MkDocsConfig(),
        files=None,
    )
    assert "@fig:diagram" not in out
    assert out.count('class="autonumber fig"') == 2
    assert out.endswith(".")
    assert ")." in out
