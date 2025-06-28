import urllib.parse
import urllib.request
from functools import lru_cache
from typing import Any, Union


@lru_cache()
def iconify(key: str) -> str:
    base_url = "https://api.iconify.design"
    icon = key.split(':')
    if len(icon) != 2:
        raise ValueError(f"Invalid icon format: {key}. Expected format 'provider:name'.")
    provider, name = icon
    url = f'{base_url}/{provider}/{name}.svg?{urllib.parse.urlencode({"height": "20px"})}'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')   # Convert to string if needed
    return content


def parse_author(site_author: str) -> Union[str, None]:
    """Returns the email address of the site author."""
    # parse thinks like "Alban Siffer <31479857+asiffer@users.noreply.github.com>"
    if '<' in site_author and '>' in site_author:
        chunks = site_author.split('<')
        email = chunks[-1].split('>')[0]
        name = chunks[0].strip()
    else:
        email = None
        name = site_author.strip()

    if email:
        return f'<a href="mailto:{email}">{name}</a>'
    return f"<span>{name}</span>"
    

def setattribute(value: Union[dict, object], k: str, v: Any):
    if hasattr(value, "__setattr__"):
        value.__setattr__(k, v)
    return value


