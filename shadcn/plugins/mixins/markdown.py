import os
import shutil
from urllib.parse import urljoin

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from shadcn.plugins.mixins.base import Mixin
from shadcn.plugins.mixins.order import NUMBER_PREFIX

logger = get_plugin_logger("mixins/markdown")


class MarkdownMixin(Mixin):
    """A mixin to expose raw page markdown in templates, copy them to the build dir, and provide a URL."""

    def __init__(self):
        self.raw_markdown = {}

    def on_page_context(
        self,
        context: TemplateContext,
        page: Page,
        config: MkDocsConfig,
        nav: Navigation,
    ):
        src_path = NUMBER_PREFIX.sub(lambda m: m.group(1), page.file.src_path)
        self.raw_markdown[page.file.abs_src_path] = os.path.join(
            config.site_dir, src_path
        )
        context["raw_markdown_url"] = urljoin(config.site_url or "/", src_path)  # type: ignore (need this to download markdown files)
        return super().on_page_context(context, page, config, nav)

    def on_post_build(self, config):  # type: ignore[invalid-method-override]
        # Copy raw markdown files to the build directory
        for src, dst in self.raw_markdown.items():
            logger.debug(f"Copying raw markdown file {src} to {dst}")
            shutil.copy2(src, dst)
        return super().on_post_build(config)
