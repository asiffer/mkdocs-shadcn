from __future__ import annotations

from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/llmstxt")


@dataclass
class _Item:
    title: str
    url: str
    summary: str | None = None

    def __str__(self) -> str:
        out = f" - [{self.title}]({self.url})"
        if self.summary:
            out += f": {self.summary}"
        return out


class LlmstxtMixin(Mixin):
    """A mixin to llms.txt at the root of the built site"""

    def __init__(self):
        self.toc = {}
        super().__init__()

    @classmethod
    def _is_enabled(cls, config: MkDocsConfig) -> bool:
        if config.theme.get("llmstxt", False):
            if config.theme.get("hide_source_files", False) is True:
                raise ValueError(
                    "llmstxt cannot be activated with `hide_source_files: true`"
                )
            return True
        return False

    def on_page_context(
        self,
        context: TemplateContext,
        page: Page,
        config: MkDocsConfig,
        nav: Navigation,
    ):
        if self._is_enabled(config):
            root = self.toc
            ancestors = [a.title for a in page.ancestors]
            for ancestor in reversed(ancestors):
                child = root.get(ancestor, None)
                if child is None:
                    root[ancestor] = {}
                root = root[ancestor]

            url = context.get("raw_markdown_url")
            assert url is not None, (
                f"The page {page.title} has no markdown url"
            )
            root[page.title] = _Item(
                title=page.meta.get("title", page.title),
                url=url,
                summary=page.meta.get("summary", None),
            )

        return super().on_page_context(context, page, config, nav)

    @classmethod
    def _recursive_write(
        cls,
        toc: dict,
        buffer: TextIOWrapper,
        level: int = 2,
    ):
        for key, value in toc.items():
            if isinstance(value, _Item):
                buffer.write(f"{value}\n")
            else:
                if level == 2:
                    buffer.write(f"\n{'#' * level} {key}\n\n")
                cls._recursive_write(value, buffer, level + 1)

    def on_post_build(self, config: MkDocsConfig):
        if self._is_enabled(config):
            with open(Path(config.site_dir) / "llms.txt", "w") as txt:
                txt.write(f"# {config.site_name}\n\n")
                if config.site_description is not None:
                    txt.write(f"> {config.site_description}\n\n")
                self._recursive_write(self.toc, txt)
                txt.write("\n")

        return super().on_post_build(config)
