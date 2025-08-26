import xml.etree.ElementTree as ET
from urllib.parse import parse_qs

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

from shadcn.filters import iconify

ICONIFY_TAG_RE = (
    r"[+]([a-z0-9\-]+:[a-z0-9\-]+)(?:[;][a-z]+[=][0-9a-zA-Z.#%]+)*[+]"
)


class IconifyInlinePattern(InlineProcessor):
    def handleMatch(self, m, data):
        # library = m.group(1)
        # icon_name = m.group(2)
        # icon_id = f"{library}:{icon_name}"
        print("MATCHED ICONIFY:", m.group(1), m.groups())
        raw_query = m.group(0).replace(m.group(1), "").strip("+").strip(";")
        print("RAW QUERY:", raw_query)
        if raw_query:
            params = dict(k.split("=") for k in raw_query.split(";"))
        else:
            params = {}

        # params = parse_qs(m.group(2).strip("?") if m.group(2) else "")
        print("PARAMS:", params)
        icon_id = m.group(1).strip("+")
        raw_svg = iconify(icon_id, **params)
        raw_svg = raw_svg.replace(r"<svg", r'<svg class="iconify"')
        print("RAW SVG:", raw_svg)
        # el = self.md.htmlStash.store(raw_svg)
        # Ensure the SVG is parsed correctly
        # raw_svg = raw_svg.replace('xmlns="http://www.w3.org/2000/svg"', "")
        placeholder = self.md.htmlStash.store(raw_svg)
        # print("EL:", el)
        # ET.register_namespace("", "http://www.w3.org/2000/svg")
        return placeholder, m.start(0), m.end(0)
        # return ET.fromstring(raw_svg), m.start(0), m.end(0)


class IconifyExtension(Extension):
    def extendMarkdown(self, md):
        ICONIFY_PATTERN = IconifyInlinePattern(ICONIFY_TAG_RE, md)
        md.inlinePatterns.register(ICONIFY_PATTERN, "iconify", 175)


def makeExtension(**kwargs):
    return IconifyExtension(**kwargs)
