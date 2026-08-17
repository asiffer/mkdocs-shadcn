from __future__ import annotations

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

from shadcn.plugins.mixins.base import Mixin

ORDER_META_KEY = "order"

logger = get_plugin_logger("mixins/order")


class OrderMixin(Mixin):
    page_index: int = 0
    """Internal page index for orderning purpose"""
    page_indices: set[int]
    """Internal set of pages that have hard-coded order"""

    nav_order: list[str]
    """Internal list of pages in the order they appear in the navigation"""

    def on_startup(self, *, command, dirty):
        self.page_indices = set()
        self.nav_order = []
        super().on_startup(command=command, dirty=dirty)

    def pre_order(self, nav_items: list):
        for item in nav_items:
            if isinstance(item, Page):
                self.nav_order.append(item.file.src_path)
            elif isinstance(item, Section):
                self.pre_order(item.children)

    def on_nav(
        self,
        nav: Navigation,
        /,
        *,
        config: MkDocsConfig,
        files: Files,
    ) -> Navigation:
        # save the nav order for later use
        self.pre_order(nav.items)
        return super().on_nav(nav, config=config, files=files) or nav

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        # add order to page if not defined
        # It uses the following priority:
        # 1. order defined in the page's meta (frontmatter)
        # 2. order defined by the navigation position
        # 3. order defined by the order of processing pages (alphabetically)
        try:
            page.meta[ORDER_META_KEY] = page.meta.get(
                ORDER_META_KEY,
                self.nav_order.index(page.file.src_path),
            )
        except ValueError:
            page.meta[ORDER_META_KEY] = self.page_index

        self.page_indices.add(self.page_index)
        # increment page index
        while self.page_index in self.page_indices:
            self.page_index += 1

        return super().on_page_markdown(
            markdown,
            page=page,
            config=config,
            files=files,
        )
