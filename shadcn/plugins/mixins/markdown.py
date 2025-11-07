import os
import shutil
from urllib.parse import urljoin

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from shadcn.plugins.mixins.base import Mixin

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
        nav,
    ):
        self.raw_markdown[page.file.abs_src_path] = os.path.join(
            config.site_dir, page.file.src_path
        )
        context.update(
            {
                "raw_markdown_url": urljoin(
                    config.site_url or "/", page.file.src_path
                )
            }
        )
        return super().on_page_context(context, page, config, nav)

    def on_post_build(self, config):
        # Copy raw markdown files to the build directory
        for src, dst in self.raw_markdown.items():
            logger.debug(f"Copying raw markdown file {src} to {dst}")
            shutil.copy2(src, dst)
        return super().on_post_build(config)
