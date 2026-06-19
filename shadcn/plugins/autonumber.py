import os
import re
from dataclasses import dataclass
from typing import Dict

from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

logger = get_plugin_logger("autonumber")


@dataclass
class AutoNumberEntry:
    page: Page
    anchor: str
    number: int
    prefix: str


def relpath(dst: str, src: str) -> str:
    r = os.path.relpath(dst, start=src)
    if r == ".":
        return ""
    return r


class AutoNumberPluginConfig(Config):
    numbering = c.Choice(["flat"], default="flat")
    prefixes: c.Type[Dict[str, str]] = c.Type(
        dict,
        default={
            "fig": "Figure",
            "tbl": "Table",
            "eq": "Equation",
        },
    )

    def label_pattern(self) -> re.Pattern:
        pattern = (
            f"[{{]#({'|'.join(self.prefixes.keys())}):([a-zA-Z0-9._-]+)[}}]"
        )
        return re.compile(pattern)

    def reference_pattern(self) -> re.Pattern:
        up_lo_prefixes = (
            "("
            + "|".join(
                list(self.prefixes.keys())
                + [k.capitalize() for k in self.prefixes.keys()]
            )
            + ")"
        )
        pattern = f"@{up_lo_prefixes}:([a-zA-Z0-9._-]+)"
        return re.compile(pattern)


class AutoNumberPlugin(BasePlugin[AutoNumberPluginConfig]):
    # autonumber: Autonumber

    def on_config(self, config: MkDocsConfig):
        self.registry: Dict[str, AutoNumberEntry] = {}
        # put fig and tbl by default if not provided
        if "fig" not in self.config.prefixes:
            self.config.prefixes["fig"] = "Figure"
        if "tbl" not in self.config.prefixes:
            self.config.prefixes["tbl"] = "Table"

        self.label_pattern = self.config.label_pattern()
        self.reference_pattern = self.config.reference_pattern()

        return config

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ):

        # init counters for this page
        counters = {prefix: 0 for prefix in self.config.prefixes.keys()}
        for match in self.label_pattern.finditer(markdown):
            full_match: str = match.group(0)
            prefix: str = match.group(1)
            id_: str = match.group(2)
            logger.debug(
                f"Found label '{full_match}' with prefix '{prefix}' "
                f"and id '{id_}' in page '{page.file.src_path}'."
            )
            if id_ in self.registry:
                logger.warning(
                    f"Duplicate ID '{id_}' found in page "
                    f"'{page.file.src_path}'. Skipping."
                )
                continue
            # Increment counter for this prefix
            number = counters[prefix] + 1
            counters[prefix] = number
            anchor: str = f"{prefix}:{id_}"
            self.registry[id_] = AutoNumberEntry(
                page=page,
                anchor=anchor,
                number=number,
                prefix=prefix,
            )
            # Replace {#fig:x} with <span id="fig:x" class="autonumber figure">Figure N</span>
            replacement = f'<span id="{anchor}" class="autonumber {prefix}">{self.config.prefixes[prefix]} {number}</span>'
            markdown = markdown.replace(full_match, replacement)
            logger.debug(
                f"Replaced label '{full_match}' with '{replacement}' in page "
                f"'{page.file.src_path}'."
            )
        return markdown

    def on_page_content(
        self,
        html: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ):
        # Pass 2: replace references with links and numbers
        for match in self.reference_pattern.finditer(html):
            full_match: str = match.group(0)
            prefix: str = match.group(1)
            is_capitalized: bool = prefix[0].isupper()
            prefix = prefix.lower()

            id_: str = match.group(2)
            logger.debug(
                f"Found reference '{full_match}' with prefix '{prefix}' "
                f"and id '{id_}' in page '{page.file.src_path}'."
            )
            if id_ not in self.registry:
                logger.warning(
                    f"Reference to unknown ID '{id_}' found in page "
                    f"'{page.file.src_path}'. Skipping."
                )
                continue
            entry = self.registry[id_]
            if entry.prefix != prefix:
                logger.warning(
                    f"Reference prefix '{prefix}' does not match label prefix "
                    f"'{entry.prefix}' for ID '{id_}' in page "
                    f"'{page.file.src_path}'. Skipping."
                )
                continue

            p = (
                self.config.prefixes[prefix].capitalize()
                if is_capitalized
                else self.config.prefixes[prefix].lower()
            )
            # Replace fig:x with <a href="page#anchor">Figure N</a>
            # -> use relative path
            href = relpath(entry.page.url, page.url)
            replacement = (
                f'<a href="{href}#{entry.anchor}" class="autonumber {prefix}">'
                f"{p} {entry.number}</a>"
            )
            html = html.replace(full_match, replacement)
            logger.debug(
                f"Replaced reference '{full_match}' with '{replacement}' in page "
                f"'{page.file.src_path}'."
            )
        return html
