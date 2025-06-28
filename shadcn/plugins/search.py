import re
import sys
from typing import Set

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.contrib.search import SearchPlugin as BaseSearchPlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

from shadcn.filters import iconify, parse_author, setattribute


class SearchPlugin(BaseSearchPlugin):
    """⚠️ HACK ⚠️
    Custom plugin. As search is loaded by default, we subclass it so as
    to inject what we want (and without adding a list of additional plugins)
    """

    page_index = 0
    page_indices: Set[int] = set()

    def on_startup(self, *, command, dirty):
        self.is_dev_server = command == "serve"

    def on_config(self, config, **kwargs):
        config["is_dev_server"] = self.is_dev_server
        return super().on_config(config, **kwargs)

    def on_env(self, env, /, *, config: MkDocsConfig, files: Files):
        # custom jinja2 filter
        env.filters["setattribute"] = setattribute
        env.filters["iconify"] = iconify
        env.filters["parse_author"] = parse_author
        # add custom global variables
        env.globals["is_dev_server"] = self.is_dev_server
        return env

    def on_nav(self, nav: Navigation, config: Config, files: Files) -> Navigation:
        # if we create folders with 00_name_of_the_folder we remove the prepended number
        # from the title. It is a common hack to have the folders ordered in the navigation
        rex = re.compile(r"^[0-9]+[ _]")
        for item in nav.items:
            if isinstance(item, Section) and rex.match(item.title):
                item.title = rex.sub("", item.title).capitalize()
        return nav

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ):
        # add order to page if not defined
        page.meta["order"] = page.meta.get("order", self.page_index)
        self.page_indices.add(self.page_index)
        # increment page index
        while self.page_index in self.page_indices:
            self.page_index += 1

        # remove first plain h1 if provided
        markdown = re.sub(r"^#\s+(.+)", r"", markdown, count=1)
        return markdown
