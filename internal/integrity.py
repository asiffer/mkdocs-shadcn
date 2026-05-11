import os
import re
from base64 import b64encode
from hashlib import sha384
from typing import Annotated

import typer
from bs4 import BeautifulSoup

from internal.common import THEME_PATH, info, log


def integrity(
    force: Annotated[
        bool, typer.Option(help="Force update of all integrity attributes")
    ] = False,
):
    """Generate integrity attributes for all <script src=""></script>
    tags in the templates.
    """
    attrs_filter = {"src": True}
    if not force:
        attrs_filter["integrity"] = False

    for file in os.listdir(THEME_PATH / "templates"):
        fp = THEME_PATH / "templates" / file
        if file.endswith(".html"):
            save = False
            with open(fp, "r") as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")
                for script in soup.find_all("script", attrs=attrs_filter):  # type: ignore
                    src = script["src"]
                    if not isinstance(src, str):
                        continue

                    match = re.search(r"[']([a-zA-Z0-9_./-]+[.]js)[']", src)
                    if match:
                        source = match.group(1)
                        log(f"Processing script: {source} in file {file}")
                        with open(THEME_PATH / source, "rb") as f:
                            a = b64encode(sha384(f.read()).digest())
                            integrity = f"sha384-{a.decode()}"
                            script["integrity"] = integrity
                            save = True
            if save:
                with open(fp, "w") as f:
                    f.write(str(soup))
                info(f"Updated integrity attributes in {file}")
