from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/dev")


class DevServerMixin(Mixin):
    """A mixin to add development server capabilities to MkDocs plugins."""

    def on_startup(self, *, command, dirty):
        self.is_dev_server = command == "serve"
        logger.debug(f"Dev server: {self.is_dev_server}")
        super().on_startup(command=command, dirty=dirty)

    def on_env(
        self, env: Environment, /, *, config: MkDocsConfig, files: Files
    ) -> Environment:
        env.globals["is_dev_server"] = self.is_dev_server
        return super().on_env(env, config=config, files=files)

    def on_config(self, config: MkDocsConfig):
        # dev server detection
        config["is_dev_server"] = self.is_dev_server
        return super().on_config(config)
