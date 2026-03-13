import xml.etree.ElementTree as etree

from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import (
    Block,
    type_string,
    type_string_in,
)

HOVER_CARD_PATTERN = r"\[([^\[\]]+)\]\^\[([^\[\]]+)\]"

HOVER_CARD_NAME = "hover-card"


class HoverCardBlock(Block):
    NAME = HOVER_CARD_NAME
    ARGUMENT = True
    OPTIONS = {
        "position": (
            "bottom",
            type_string_in(
                ["left", "right", "bottom", "top"],
                True,
            ),
        ),
        "class": ("", type_string),
    }

    def on_create(self, parent: etree.Element) -> etree.Element:
        div = etree.SubElement(parent, "div")
        div.set("class", self.NAME)
        div.set("anchor", f"{self.NAME}-{self.argument}")

        # here we need to provide a custom css since the block and the trigger
        # are in different places in the DOM. We can't use traditional selectors.
        style = etree.SubElement(div, "style")
        style.text = f"""
        article:has(#{self.NAME}-{self.argument}:hover) .{self.NAME}[anchor="{self.NAME}-{self.argument}"] {{
            opacity: 1;
            pointer-events: auto;
            animation-name: enter;
        }}
        """

        anchor_name = f"--{self.NAME}-{self.argument}"

        if self.options["position"] == "left":
            div.set(
                "style",
                f"position-anchor: {anchor_name}; right: anchor({anchor_name} left); align-self: anchor-center; transform: translateX(-5px); --tw-enter-translate-x: -10%; --tw-enter-translate-y: initial;",
            )
        elif self.options["position"] == "right":
            div.set(
                "style",
                f"position-anchor: {anchor_name}; left: anchor({anchor_name} right); align-self: anchor-center; transform: translateX(5px); --tw-enter-translate-x: 10%; --tw-enter-translate-y: initial;",
            )
        elif self.options["position"] == "top":
            div.set(
                "style",
                f"position-anchor: {anchor_name}; bottom: anchor({anchor_name} top); justify-self: anchor-center; transform: translateY(-5px); --tw-enter-translate-y: -10%; --tw-enter-translate-x: initial;",
            )
        else:  # default to bottom
            div.set(
                "style",
                f"position-anchor: {anchor_name}; top: anchor({anchor_name} bottom); justify-self: anchor-center; transform: translateY(5px); --tw-enter-translate-y: 10%; --tw-enter-translate-x: initial;",
            )

        if self.options["class"]:
            div.set(
                "class", div.get("class", "") + " " + self.options["class"]
            )

        return div

    def on_markdown(self) -> str:
        return "block"


class HoverCardBlockExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md, block_mgr):
        block_mgr.register(HoverCardBlock, self.getConfigs())

    def extendMarkdown(self, md: Markdown) -> None:
        super().extendMarkdown(md)
        md.inlinePatterns.register(
            HoverCardProcessor(HOVER_CARD_PATTERN, md),
            "hover_card",
            200,
        )


class HoverCardProcessor(InlineProcessor):
    """Matches [trigger]^[hover card content] syntax."""

    def handleMatch(self, m, data):
        trigger_text: str = m.group(1)
        card_text: str = m.group(2)

        trigger = etree.Element("span")
        trigger.set("class", f"{HOVER_CARD_NAME}-trigger")

        trigger.text = trigger_text

        if card_text.startswith("#"):
            # block case
            trigger.set("id", f"{HOVER_CARD_NAME}-{card_text[1:]}")
            trigger.set(
                "style", f"anchor-name: --{HOVER_CARD_NAME}-{card_text[1:]};"
            )
        else:
            card = etree.SubElement(trigger, "span")
            card.set("class", HOVER_CARD_NAME)
            card.text = (
                card_text  # inline markdown will be processed automatically
            )

        return trigger, m.start(0), m.end(0)


def makeExtension(**kwargs):
    return HoverCardBlockExtension(**kwargs)
