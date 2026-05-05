from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/table")


class TableMixin(Mixin):
    """A mixin to wrap <table> to better manage overflow"""

    def on_page_content(
        self,
        html: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        html = html.replace(
            r"<table",
            r'<div class="table-wrapper"><table',
        ).replace(r"</table>", r"</table></div>")
        return super().on_page_content(html, page, config, files)
