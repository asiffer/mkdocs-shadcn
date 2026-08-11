from __future__ import annotations

import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, Section

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/prefix")

NUMBER_PREFIX = re.compile(r"((?:^|/))([0-9]+[ _])")


class PrefixMixin(Mixin):
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
        def recursive_strip_number_prefix(items: list):
            for item in items:
                if (
                    isinstance(item, Section)
                    and item.title
                    and NUMBER_PREFIX.match(item.title)
                ):
                    new_title = NUMBER_PREFIX.sub("", item.title).capitalize()
                    logger.debug(f"Turning '{item.title}' into '{new_title}'")
                    item.title = new_title

                    if item.children:
                        recursive_strip_number_prefix(item.children)

        recursive_strip_number_prefix(nav.items)
        return super().on_nav(nav, config=config, files=files) or nav
