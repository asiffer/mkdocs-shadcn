import logging

from shadcn.plugins.autonumber import AutoNumberPlugin, replace_many


class FakeFile:
    def __init__(self, content: str, src_path: str = "index.md", url: str = ""):
        self.content_string = content
        self.src_path = src_path
        self.url = url

    def is_documentation_page(self) -> bool:
        return True


class FakePage:
    def __init__(self, file: FakeFile):
        self.file = file
        self.url = ""


def make_plugin() -> AutoNumberPlugin:
    plugin = AutoNumberPlugin()
    plugin.load_config({})
    plugin.on_config(None)
    return plugin


def test_replace_many_with_no_replacements_returns_text_unchanged():
    assert replace_many("unchanged {#fig:x}", {}) == "unchanged {#fig:x}"


def test_unsupported_prefix_label_warns_and_does_not_crash(caplog):
    plugin = make_plugin()
    file = FakeFile("See {#bad-prefix:object-id} for details.\n")
    with caplog.at_level(logging.WARNING):
        plugin.on_nav(None, config=None, files=[file])
        markdown = plugin.on_page_markdown(
            file.content_string, page=FakePage(file), config=None, files=[file]
        )
    # The label is left as-is instead of crashing the build.
    assert markdown == file.content_string
    warnings = [record.getMessage() for record in caplog.records]
    assert any(
        "Unsupported prefix 'bad-prefix'" in message
        and "fig" in message
        and "prefixes" in message
        for message in warnings
    )


def test_supported_prefix_label_still_numbers(caplog):
    plugin = make_plugin()
    file = FakeFile("![img](x.png)\n\n{#fig:mountain} - A mountain.\n")
    with caplog.at_level(logging.WARNING):
        plugin.on_nav(None, config=None, files=[file])
        markdown = plugin.on_page_markdown(
            file.content_string, page=FakePage(file), config=None, files=[file]
        )
    assert "Unsupported prefix" not in caplog.text
    assert '<span id="fig:mountain"' in markdown
    assert "Figure 1" in markdown
