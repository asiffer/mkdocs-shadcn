from collections.abc import Mapping

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger

from shadcn.plugins.mixins.base import Mixin
from shadcn.utils import deep_merge

MKDOCSTRINGS_CONFIG: Mapping = {
    "handlers": {
        "python": {
            "options": {
                "show_root_heading": True,
            }
        },
    },
}

logger = get_plugin_logger("mixins/mkdocstrings")


class MkdocstringsMixin(Mixin):
    def on_config(self, config: MkDocsConfig):
        plugin = config["plugins"].get("mkdocstrings", None)

        if plugin:
            logger.info("Mkdocstrings mixin activated.")
            options = (
                plugin.config.get("handlers", {}).get("python", {}).get("options", {})
            )
            show_root_heading = options.get("show_root_heading", None)
            if show_root_heading is None:
                logger.debug(
                    "Setting 'show_root_heading' to True for mkdocstrings python handler."
                )
                deep_merge(plugin.config, MKDOCSTRINGS_CONFIG)

        return super().on_config(config)
