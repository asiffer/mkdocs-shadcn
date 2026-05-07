import re
from typing import List, Set

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

from shadcn.plugins.mixins.base import Mixin

ORDER_META_KEY = "order"

logger = get_plugin_logger("mixins/order")

NUMBER_PREFIX = re.compile(r"((?:^|/))([0-9]+[ _])")


class OrderMixin(Mixin):
    page_index = 0
    """Internal page index for orderning purpose"""
    page_indices: Set[int] = set()
    """Internal set of pages that have hard-coded order"""

    nav_order: List[str] = []
    """Internal list of pages in the order they appear in the navigation"""

    def pre_order(self, nav_items: list):
        for item in nav_items:
            if isinstance(item, Page):
                self.nav_order.append(item.file.src_path)
            elif isinstance(item, Section):
                self.pre_order(item.children)

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        """Remove order from file destination URI, to get nicer URLs."""
        for file in files:
            if NUMBER_PREFIX.search(file.dest_uri):
                file.dest_uri = NUMBER_PREFIX.sub(
                    lambda m: m.group(1),
                    file.dest_uri,
                )
        return super().on_files(files, config)

    def on_nav(
        self,
        nav: Navigation,
        /,
        *,
        config: MkDocsConfig,
        files: Files,
    ) -> Navigation:
        # if we create folders with 00_name_of_the_folder we remove the prepended number
        # from the title. It is a common hack to have the folders ordered in the navigation
        rex = re.compile(r"^[0-9]+[ _]")

        def recursive_strip_number_prefix(items: list):
            for item in items:
                if (
                    isinstance(item, Section)
                    and item.title
                    and rex.match(item.title)
                ):
                    item.title = rex.sub("", item.title).capitalize()
                    if item.children:
                        recursive_strip_number_prefix(item.children)

        recursive_strip_number_prefix(nav.items)

        # save the nav order for later use
        self.pre_order(nav.items)
        logger.debug(f"Navigation order: {self.nav_order}")
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
