from mkdocs.plugins import get_plugin_logger

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/table")


class TableMixin(Mixin):
    """A mixin to wrap <table> to better manage overflow"""

    def on_page_content(self, html, **kwargs):
        return html.replace(
            r"<table",
            r'<div class="table-wrapper"><table',
        ).replace(r"</table>", r"</table></div>")
