from mkdocs.config.defaults import MkDocsConfig

from shadcn.plugins.mixins.base import Mixin

MKDOCSTRINGS_CONFIG = {
    "handlers": {
        "python": {
            "options": {
                "show_root_heading": True,
            }
        },
    },
    "default_handler": "python",
}


class MkdocstringsMixin(Mixin):
    def on_config(self, config: MkDocsConfig):
        plugin = config["plugins"].get("mkdocstrings", None)

        if plugin:
            options = (
                plugin.config.get("handlers", {})
                .get("python", {})
                .get("options", {})
            )
            show_root_heading = options.get("show_root_heading", None)
            if show_root_heading is None:
                plugin.config.update(MKDOCSTRINGS_CONFIG)

        return super().on_config(config)
