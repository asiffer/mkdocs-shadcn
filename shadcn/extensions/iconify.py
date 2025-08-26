from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

from shadcn.filters import iconify

ICONIFY_TAG_RE = (
    r"[+]([a-z0-9\-]+:[a-z0-9\-]+)(?:[;][a-z]+[=][0-9a-zA-Z.#%]+)*[+]"
)


class IconifyInlinePattern(InlineProcessor):
    def handleMatch(self, m, data):
        raw_query = m.group(0).replace(m.group(1), "").strip("+").strip(";")
        if raw_query:
            params = dict(k.split("=") for k in raw_query.split(";"))
        else:
            params = {}

        icon_id = m.group(1).strip("+")
        raw_svg = iconify(icon_id, **params)
        raw_svg = raw_svg.replace(r"<svg", r'<svg class="iconify"')
        placeholder = self.md.htmlStash.store(raw_svg)
        return placeholder, m.start(0), m.end(0)


class IconifyExtension(Extension):
    def extendMarkdown(self, md):
        ICONIFY_PATTERN = IconifyInlinePattern(ICONIFY_TAG_RE, md)
        md.inlinePatterns.register(ICONIFY_PATTERN, "iconify", 175)


def makeExtension(**kwargs):
    return IconifyExtension(**kwargs)
