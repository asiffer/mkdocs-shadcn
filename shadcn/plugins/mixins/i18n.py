import gettext

from jinja2 import Environment
from jinja2.ext import InternationalizationExtension
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/i18n")


class I18nMixin(Mixin):
    """A mixin to support internationalization"""

    def on_env(
        self, env: Environment, /, *, config: MkDocsConfig, files: Files
    ) -> Environment:
        env.add_extension(InternationalizationExtension)
        translations = gettext.translation(
            "messages",
            localedir=self.theme_root / "locales",
            languages=[config.theme.locale.language],
            fallback=True,
        )
        env.install_gettext_translations(translations)  # ty:ignore[unresolved-attribute] (install_gettext_translations is added by the i18n extension)
        return super().on_env(env, config=config, files=files)
