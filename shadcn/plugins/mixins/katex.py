import re
from typing import Dict
from urllib.parse import urljoin

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from shadcn.plugins.mixins.base import Mixin

logger = get_plugin_logger("mixins/katex")

LABEL_PATTERN = re.compile(r"\\label[{]([a-zA-Z0-9:._-]+)[}]")


class KatexMixin(Mixin):
    """A mixin to add extra features to Katex plugin."""

    katex_mixin_activated = False
    katex_mixin_use_links = False
    katex_mixin_labels: Dict[str, int] = {}
    katex_mixin_translations: Dict[str, str] = {}

    def on_config(self, config: MkDocsConfig):
        if "pymdownx.arithmatex" in config.markdown_extensions:
            self.katex_mixin_activated = True
            self.katex_mixin_use_links = (
                config.theme.get("katex_options", {}).get(
                    "trust", None
                )  # trust could be boolean or function
                is not None
            )
            logger.info("Katex mixin activated.")

        self.katex_mixin_labels.clear()
        self.katex_mixin_translations.clear()
        return super().on_config(config)

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        if self.katex_mixin_activated:
            for old, new in self.katex_mixin_translations.items():
                logger.debug(
                    f"Replacing '{old}' with '{new}' in page '{page.file.src_path}'."
                )
                markdown = markdown.replace(old, new)

        return super().on_page_markdown(
            markdown,
            page=page,
            config=config,
            files=files,
        )

    def on_files(self, files: Files, config: MkDocsConfig):
        if not self.katex_mixin_activated:
            return super().on_files(files, config)

        for file in files:
            if not (
                file.is_documentation_page and file.src_path.endswith(".md")
            ):
                continue

            try:
                markdown = file.content_string
            except Exception as e:
                logger.warning(
                    f"Could not read content of file '{file.src_path}': {e}"
                )
                continue

            for match in LABEL_PATTERN.finditer(markdown):
                label: str = match.group(1)
                if label in self.katex_mixin_labels:
                    logger.warning(
                        f"Duplicate label '{label}' found in page '{file.src_path}'. "
                        f"Previous occurrence was in page '{self.katex_mixin_translations[label]}'."
                    )
                else:
                    self.katex_mixin_labels[label] = (
                        len(self.katex_mixin_labels) + 1
                    )  # starts with 1

                    href = (
                        urljoin(config.site_url or "/", file.dest_uri)
                        + f"#{label}"
                    )
                    if self.katex_mixin_use_links:
                        self.katex_mixin_translations[f"\\ref{{{label}}}"] = (
                            f"(\\href{{{href}}}{{{self.katex_mixin_labels[label]}}})"
                        )
                        self.katex_mixin_translations[
                            f"\\label{{{label}}}"
                        ] = f"\\htmlId{{{label}}}{{\\tag{{{self.katex_mixin_labels[label]}}}}}"
                    else:
                        self.katex_mixin_translations[f"\\ref{{{label}}}"] = (
                            f"({self.katex_mixin_labels[label]})"
                        )
                        self.katex_mixin_translations[
                            f"\\label{{{label}}}"
                        ] = f"\\tag{{{self.katex_mixin_labels[label]}}}"

        return super().on_files(
            files=files,
            config=config,
        )
