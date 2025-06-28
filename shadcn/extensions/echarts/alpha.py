import logging
import random
import string
import xml.etree.ElementTree as etree
from typing import Literal

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor  # type: ignore
from pymdownx.blocks.block import Block, type_string_in  # type: ignore

log = logging.getLogger(f"mkdocs.extensions.{__name__}")


def generate_random_string(size: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=size))


class EchartsBlock(Block):
    NAME = "echarts"
    ARGUMENT = False
    OPTIONS = {
        "renderer": ("svg", type_string_in(["svg", "canvas"])),
    }

    md: Markdown

    # custom state
    echarts_options: str
    raw_content: str
    div_id: str

    def on_init(self):
        self.echarts_options = ""
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

        # generate a random id if not provided
        log.debug("echarts block found")
        self.div_id = self.attrs.get("id", generate_random_string(6))
        div = etree.SubElement(parent, "div")
        return div

    def on_add(self, block: etree.Element):
        """When any calls occur to process new content, on_add is called.
        This gives the block a chance to return the element where the
        content is desired."""

        # save the raw content in all cases
        self.raw_content = block.text or ""
        # ignore empty block
        if block.text is None:
            return block
        # check if it looks like a json object
        start = block.text.find("{")
        end = block.text.rfind("}")
        if start == -1 or end == -1:
            return block

        log.debug(f"echarts options can be extracted from the block")
        self.echarts_options = block.text[start : end + 1]
        # remove the text (otherwise the raw text will be displayed)
        block.text = ""
        return block

    def on_end(self, block: etree.Element) -> None:
        """When a block is parsed to completion, the on_end event is
        executed. This allows an extension to perform any post
        processing on the elements. You could save the data as raw
        text and then parse it special at the end or you could walk
        the HTML elements and move content around, add attributes, or
        whatever else is needed."""
        log.debug(f"content of echarts block:\n{self.raw_content}")
        if self.echarts_options == "":
            log.warning(
                f"No echarts options found in the following block:"
                f"\n---\n{self.raw_content}\n---\n"
            )
            return

        script = etree.SubElement(block, "script")
        script.set("type", "text/javascript")
        script.set("defer", "true")

        script.text = f"""
        const target{self.div_id} = document.getElementById('{self.div_id}');
        const chart{self.div_id} = echarts.init(target{self.div_id}, 'shadcn', {{ renderer: '{self.renderer}' }});
        chart{self.div_id}.setOption({self.echarts_options});
        window.addEventListener('resize', function() {{ chart{self.div_id}.resize(); }});
        const observer{self.div_id} = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    chart{self.div_id}.resize();
                    observer{self.div_id}.disconnect(); // Stop observing if you want a one-time trigger
                }}
            }});
        }});

        observer{self.div_id}.observe(target{self.div_id});
        """

        # set some attributes if not defined by the user
        block.set("id", self.div_id)
        block.set("class", block.get("class", "echarts"))
        block.set("style", block.get("style", "width:100%;height:500px;"))

        self.echarts_options = ""
        self.div_id = ""

    def on_markdown(self) -> str:  # type: ignore
        """Check how element should be treated by the Markdown parser."""
        return "raw"


class EchartsBlockExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor):
        block_mgr.register(EchartsBlock, self.getConfigs())


def makeExtension(*args, **kwargs):
    """Return extension."""
    return EchartsBlockExtension(*args, **kwargs)
