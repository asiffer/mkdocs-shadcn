from babel.messages.catalog import Catalog
from babel.messages.extract import extract_from_dir
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po, write_po

from internal.common import THEME_PATH, info, version

LOCALES_DIR = THEME_PATH / "locales"

# The method_map mirrors what you'd put in babel.cfg
method_map = [
    ("**.html", "jinja2"),
]

# Options correspond to what goes under each section in babel.cfg
options_map = {
    "**.html": {
        "encoding": "utf-8",
        "extensions": "jinja2.ext.i18n",
    },
}


# Extract all messages
# messages = extract_from_dir(
#     dirname=THEME_PATH / "templates",  # your templates directory
#     method_map=method_map,
#     options_map=options_map,
# )
def populate_catalog(catalog: Catalog) -> Catalog:
    catalog.project = "mkdocs-shadcn"
    catalog.version = version()
    catalog.charset = "utf-8"
    catalog.domain = "messages"
    return catalog


def extract_template() -> Catalog:
    """Extract all translatable strings into a fresh catalog."""
    catalog = populate_catalog(Catalog())
    for fname, lineno, msg, comments, ctx in extract_from_dir(
        THEME_PATH / "templates", method_map, options_map
    ):
        catalog.add(
            id=msg,
            locations=[(fname, lineno)],
            auto_comments=comments,
            context=ctx,
        )
    return catalog


def save_pot(catalog):
    """Write the .pot template file (Portable Object Template)"""
    with open(LOCALES_DIR / "messages.pot", "wb") as f:
        write_po(f, catalog)


def update_locale(catalog: Catalog, lang: str):
    """Merge new strings into an existing .po file (Portable Object for a specific language)"""
    po_path = LOCALES_DIR / lang / "LC_MESSAGES" / "messages.po"

    with open(po_path, "rb") as f:
        existing = read_po(f)

    existing.update(catalog)

    existing = populate_catalog(existing)
    with open(po_path, "wb") as f:
        write_po(f, existing)


def compile_locale(lang: str):
    """Compile .po to .mo."""
    po_path = LOCALES_DIR / lang / "LC_MESSAGES" / "messages.po"
    mo_path = LOCALES_DIR / lang / "LC_MESSAGES" / "messages.mo"

    with open(po_path, "rb") as f:
        catalog = read_po(f)

    with open(mo_path, "wb") as f:
        write_mo(f, catalog)


def makemessages():
    """Extract translatable strings from templates and updates messages.po file"""
    catalog = extract_template()

    for lang_dir in LOCALES_DIR.iterdir():
        if lang_dir.is_dir() and (lang_dir / "LC_MESSAGES").exists():
            lang = lang_dir.name
            update_locale(catalog, lang)
            info(f"Locales updated: {lang}")


def compilemessages():
    """Compile .po files to .mo for all languages."""
    for lang_dir in LOCALES_DIR.iterdir():
        if lang_dir.is_dir() and (lang_dir / "LC_MESSAGES").exists():
            lang = lang_dir.name
            compile_locale(lang)
            info(f"Locales compiled: {lang}")
