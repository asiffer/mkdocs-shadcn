import urllib.parse
import urllib.request
from functools import lru_cache
from pathlib import Path
from typing import Any, Union

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page


@lru_cache()
def iconify(key: str, height: str = "20px", **kwargs) -> str:
    base_url = "https://api.iconify.design"
    icon = key.split(":")
    if len(icon) != 2:
        raise ValueError(
            f"Invalid icon format: {key}. Expected format 'provider:name'."
        )
    # collapse icon
    provider, name = icon
    url = f"{base_url}/{provider}/{name}.svg?{urllib.parse.urlencode({'height': height, **kwargs})}"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode(
            "utf-8"
        )  # Convert to string if needed
    return content


def parse_author(site_author: str) -> Union[str, None]:
    """Returns the email address of the site author."""
    # parse thinks like "Alban Siffer <31479857+asiffer@users.noreply.github.com>"
    if "<" in site_author and ">" in site_author:
        chunks = site_author.split("<")
        email = chunks[-1].split(">")[0]
        name = chunks[0].strip()
    else:
        email = None
        name = site_author.strip()

    if email:
        return f'<a href="mailto:{email}">{name}</a>'
    return f"<span>{name}</span>"


def setattribute(value: Union[dict, object], k: str, v: Any):
    if hasattr(value, "__setattr__"):
        setattr(value, k, v)
    return value


def active_section(nav: Navigation) -> Union[Section, None]:
    """Return the top-level active section"""
    for item in nav:
        if isinstance(item, Section) and item.is_section and item.active:
            return item
    return None


def first_page(section: Section) -> Union[Page, None]:
    """Return the first page in a section"""
    for item in section.children:
        if isinstance(item, Page) and item.is_page:
            return item

    for item in section.children:
        if isinstance(item, Section):
            fp = first_page(item)
            if fp:
                return fp

    return None


def file_exists(path: str, config: MkDocsConfig) -> bool:
    """Check if a file exists at the given path, from docs_dir"""
    p: Path = Path(config.docs_dir) / Path(path)
    return p.exists() and p.is_file()


def is_http_url(path: str) -> bool:
    """Check if a path is a valid URL (http, https and also data scheme)"""
    try:
        parsed = urllib.parse.urlparse(path)
    except Exception:
        return False

    if parsed.scheme not in ("http", "https", "data"):
        return False
    return True
