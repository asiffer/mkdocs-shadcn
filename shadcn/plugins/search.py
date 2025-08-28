import re
from typing import Union

from git import Repo
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.contrib.search import SearchPlugin as BaseSearchPlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from shadcn.filters import (
    active_section,
    first_page,
    iconify,
    parse_author,
    setattribute,
)
from shadcn.plugins.mixins.dev import DevServerMixin
from shadcn.plugins.mixins.git import GitTimestampsMixin
from shadcn.plugins.mixins.mkdocstrings import MkdocstringsMixin
from shadcn.plugins.mixins.order import OrderMixin

# from shadcn.plugins.mixins.search import SearchMixin as BaseSearchPlugin


def find_repo(abs_src_file: str) -> Union[Repo, None]:
    """
    Find the git repository for the given source file.
    Returns None if no repository is found.
    """
    try:
        return Repo(abs_src_file, search_parent_directories=True)
    except Exception:
        print(f"Could not find git repository starting from {abs_src_file}")
        return None


class SearchPlugin(
    GitTimestampsMixin,
    DevServerMixin,
    OrderMixin,
    MkdocstringsMixin,
    BaseSearchPlugin,
):
    """⚠️ HACK ⚠️
    Custom plugin. As search is loaded by default, we subclass it so as
    to inject what we want (and without adding a list of additional plugins)
    """

    def on_config(self, config: MkDocsConfig, **kwargs):
        # we need to put "en" as default language for search
        self.config["lang"] = self.config.get("lang", None) or ["en"]
        return super().on_config(config)

    def on_env(self, env, /, *, config: MkDocsConfig, files: Files):
        # custom jinja2 filter
        env.filters["setattribute"] = setattribute
        env.filters["iconify"] = iconify
        env.filters["parse_author"] = parse_author
        env.filters["active_section"] = active_section
        env.filters["first_page"] = first_page
        return super().on_env(env, config=config, files=files)

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ):
        # remove first plain h1 if provided
        markdown = re.sub(r"^#\s+(.+)", r"", markdown, count=1)
        return super().on_page_markdown(
            markdown, page=page, config=config, files=files
        )
