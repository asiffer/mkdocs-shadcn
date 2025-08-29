from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

mixin_logger = get_plugin_logger("mixins")


class Mixin:
    """A base mixin class for MkDocs plugins."""

    def on_startup(self, *, command, dirty):
        pass

    def on_env(
        self, env: Environment, /, *, config: MkDocsConfig, files: Files
    ) -> Environment:
        return env

    def on_nav(
        self, nav: Navigation, /, *, config: MkDocsConfig, files: Files
    ) -> Navigation:
        return nav

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        return markdown

    def on_config(self, config: MkDocsConfig):
        return config
