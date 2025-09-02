from typing import Any

from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

mixin_logger = get_plugin_logger("mixins")


class Mixin:
    """A base mixin class for MkDocs plugins."""

    def _super_method_or(
        self,
        method_name: str,
        *args,
        fallback: Any = None,
        **kwargs,
    ):
        """Call the superclass method if it exists, otherwise return the fallback value."""
        fun = getattr(super(), method_name, None)
        if fun is None:
            return fallback
        return fun(*args, **kwargs)

    def on_startup(self, *, command, dirty) -> None:
        return self._super_method_or(
            "on_startup",
            command=command,
            dirty=dirty,
        )

    def on_env(
        self,
        env: Environment,
        /,
        *,
        config: MkDocsConfig,
        files: Files,
    ) -> Environment:
        return self._super_method_or(
            "on_env",
            env,
            config=config,
            files=files,
            fallback=env,
        )

    def on_nav(
        self,
        nav: Navigation,
        /,
        *,
        config: MkDocsConfig,
        files: Files,
    ) -> Navigation:
        return self._super_method_or(
            "on_nav",
            nav,
            config=config,
            files=files,
            fallback=nav,
        )

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        return self._super_method_or(
            "on_page_markdown",
            markdown,
            page=page,
            config=config,
            files=files,
            fallback=markdown,
        )

    def on_config(self, config: MkDocsConfig):
        return self._super_method_or("on_config", config, fallback=config)
