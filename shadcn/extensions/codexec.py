import logging
import random
import re
import string
import xml.etree.ElementTree as etree
from typing import Literal

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor  # type: ignore
from pymdownx.blocks.block import Block, type_string_in  # type: ignore

log = logging.getLogger(f"mkdocs.extensions.{__name__}")


def generate_random_string(size: int) -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=size)
    )


class CodexecBlock(Block):
    NAME = "codexec"
    ARGUMENT = False
    OPTIONS = {
        "renderer": ("svg", type_string_in(["svg", "canvas"])),
    }

    md: Markdown

    def on_init(self):
        self.codexec_options = ""
        self.div_id = ""
        self.raw_content = ""

    @property
    def attrs(self) -> dict:
        return self.options.get("attrs", {})

    @property
    def renderer(self) -> Literal["svg", "canvas"]:
        return self.options.get("renderer", "svg")

    def on_create(self, parent: etree.Element):  # type: ignore
        """Called when a block is initially found and initialized.
        The on_create method should create the container for the
        block under the parent element. Other child elements can
        be created on the root of the container, but outer element
        of the created container should be returned.
        """
        div = etree.SubElement(parent, "div")
        div.set("class", "codexec")
        return div

    def on_end(self, block: etree.Element) -> None:
        """When a block is parsed to completion, the on_end event is
        executed. This allows an extension to perform any post
        processing on the elements. You could save the data as raw
        text and then parse it special at the end or you could walk
        the HTML elements and move content around, add attributes, or
        whatever else is needed."""

        code = block.find(".//code")
        if code is None:
            log.warning(
                "CodexecBlock: No <code> element found in block. "
                "This block will not be rendered."
            )
            return

        regex = re.compile(r"^:::([a-zA-Z0-9_]+)\s*")
        content = (code.text or "").strip(" \n\t")
        m = regex.match(content)
        if m:
            # Extract the language from the first line
            self.lang = m.group(1)
            content = content[m.end() :].strip(" \n\t")

        content = re.sub(
            r"(?<!\\)\\(.)",
            r"\\\\\1",
            content,
        )  # Escape single backslashes

        # run button
        button = etree.SubElement(block, "button")
        callback = """({output, ok}) => { 
            const result = this.parentElement.getElementsByClassName('codexec-result')[0]; 
            if (result) { 
                if (ok === false) {
                    result.classList.add('error');
                } else {
                    result.classList.remove('error');
                }
                const pre = result.querySelector('pre');
                if (pre) {
                    pre.innerHTML = output;
                }
            }
            this.dataset.status = '';
        }
        """
        button.set("data-status", "")
        button.set(
            "onclick",
            f"""this.dataset.status='loading';runCodexec(`{content}`,'{self.lang}').then({callback})""",
        )
        icon = etree.SubElement(button, "svg")
        icon.set("class", "play")
        icon.set("xmlns", "http://www.w3.org/2000/svg")
        icon.set("viewBox", "0 0 24 24")
        icon.set("fill", "currentColor")
        path = etree.SubElement(icon, "path")
        path.set("fill-rule", "evenodd")
        path.set(
            "d",
            "M4.5 5.653c0-1.427 1.529-2.33 2.779-1.643l11.54 6.347c1.295.712 1.295 2.573 0 3.286L7.28 19.99c-1.25.687-2.779-.217-2.779-1.643V5.653Z",
        )

        # <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-loader-circle-icon lucide-loader-circle"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
        icon = etree.SubElement(button, "svg")
        icon.set("class", "loading animate-spin")
        icon.set("xmlns", "http://www.w3.org/2000/svg")
        icon.set("viewBox", "0 0 24 24")
        icon.set("stroke", "currentColor")
        icon.set("stroke-width", "2")
        icon.set("stroke-linecap", "round")
        icon.set("stroke-linejoin", "round")
        icon.set("fill", "none")
        path = etree.SubElement(icon, "path")
        path.set(
            "d",
            "M21 12a9 9 0 1 1-6.219-8.56",
        )

        # add result container
        result = etree.SubElement(block, "div")
        result.set("class", "codexec-result")
        etree.SubElement(result, "pre")

    def on_markdown(self) -> str:  # type: ignore
        #     """Check how element should be treated by the Markdown parser."""
        return "block"


class CodexecBlockExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor):
        block_mgr.register(CodexecBlock, self.getConfigs())


def makeExtension(*args, **kwargs):
    """Return extension."""
    return CodexecBlockExtension(*args, **kwargs)
