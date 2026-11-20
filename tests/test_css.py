from __future__ import annotations

from dataclasses import dataclass, field

from conftest import ShadcnProject
from playwright.sync_api import (
    Page,
)


@dataclass
class _CustomStyle:
    selector: list[str] = field(default_factory=list)
    css: dict[str, str] = field(default_factory=dict)
    layer: str = field(default="utilities")

    @property
    def css_selector(self) -> str:
        return " ".join(self.selector)

    @property
    def css_rule(self) -> str:
        return "\n".join(f"{key}: {value};" for key, value in self.css.items())

    def __str__(self):
        return f"""@layer {self.layer} {{
    {self.css_selector} {{
        {self.css_rule}
    }}
}}"""


custom_styles: list[_CustomStyle] = [
    _CustomStyle(
        layer="utilities",
        selector=["article", "#page-header", "h1"],
        css={
            "color": "rgb(255, 0, 0)",
            "font-size": "51px",
            "font-weight": "700",
        },
    ),
    _CustomStyle(
        layer="utilities",
        selector=["article", ".typography", "h2"],
        css={
            "color": "rgb(255, 255, 0)",
            "font-size": "34px",
            "font-weight": "300",
        },
    ),
    _CustomStyle(
        layer="utilities",
        selector=["article", "p"],
        css={
            "text-align": "justify",
            "font-size": "12px",
        },
    ),
]


def test_css_override(shadcn_project: ShadcnProject, page: Page):
    md_file = "override.md"
    css_file = "css/custom.css"
    shadcn_project.write_file(
        css_file,
        "\n\n".join(str(style) for style in custom_styles),
    )
    shadcn_project.write_file(
        md_file,
        "## H2\n\n### H3\n\n go\n",
        {"extra_css": [css_file]},
    )

    shadcn_project.build()

    uri = shadcn_project.get_built_file(md_file).resolve().as_uri()
    page.goto(uri)

    for style in custom_styles:
        element = page.locator(style.css_selector).first
        styles = element.evaluate("""el => {
            const s = getComputedStyle(el);
            const result = {};
            for (const name of s) {          // iterates over property names
                result[name] = s.getPropertyValue(name);
            }
            return result;
        }""")
        for key, value in style.css.items():
            assert styles[key] == value
