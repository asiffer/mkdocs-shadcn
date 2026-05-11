import os
import re
import tarfile
import tempfile
from pathlib import Path
from typing import Annotated, Union

import requests
import typer
from github import Github
from github.GithubException import UnknownObjectException
from github.GitRelease import GitRelease
from github.Repository import Repository

from internal.common import THEME_PATH, error, info, log

ARITMATEX_TEMPLATE = """
<!-- katex -->
<link rel="stylesheet" href="{{ 'katex.min.css' | url }}" >
<!-- The loading of KaTeX is deferred to speed up page rendering -->
<script defer src="{{ 'katex.min.js' | url }}"></script>
<!-- To automatically render math in text elements, include the auto-render extension: -->
<script defer src="{{ 'js/auto-render.min.js' | url }}"
    onload='renderMathInElement(document.body, {{ ((config.theme.katex_options or "{}") | tojson) }});'></script>
"""

ARITMATEX_TEMPLATE_FILE = THEME_PATH / "templates" / "katex.html"

REPO = "KaTeX/KaTeX"
GH = Github()

MAPPER = {
    "katex.min.css": THEME_PATH / "css" / "katex.min.css",
    "katex.min.js": THEME_PATH / "js" / "katex.min.js",
    "contrib/auto-render.min.js": THEME_PATH / "js" / "auto-render.min.js",
}

FONTS_DIR = THEME_PATH / "fonts" / "katex"

WOFF_OR_TTF = re.compile(
    r',?\s*url\([^)]+\.woff\)\s*format\("woff"\)|,?\s*url\([^)]+\.ttf\)\s*format\("truetype"\)'
)


def get_release(repo: Repository, tag: str) -> GitRelease:
    if tag == "latest":
        release = repo.get_latest_release()
    else:
        try:
            release = repo.get_release(tag)
        except UnknownObjectException:
            last_releases = [r.tag_name for r in repo.get_releases()]
            raise RuntimeError(
                f"Release '{tag}' not found. Last available assets: {last_releases[:5]}"
            )
    return release


def download_tarball(release: GitRelease):
    for asset in release.assets:
        if asset.name.endswith(".tar.gz"):
            tar = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)
            log(f"Downloading {asset.name} to {tar.name}")
            # asset.download_asset(path=tar.name)
            response = requests.get(
                asset.browser_download_url, allow_redirects=True
            )
            if response.status_code != 200:
                raise RuntimeError(
                    f"Failed to download {asset.name} ({response.status_code})"
                )

            with open(tar.name, "wb") as f:
                f.write(response.content)
            return tar
    raise RuntimeError(f"No tarball found within assets ({release.assets})")


def extract_css_js(tarpath: str) -> str:
    log(f"Extracting {tarpath}")
    template = ARITMATEX_TEMPLATE
    with tarfile.open(tarpath, "r:gz") as archive:
        for name, path in MAPPER.items():
            log(f"Extracting {name} to {path.relative_to(THEME_PATH)}")
            file = archive.extractfile(f"katex/{name}")
            if file is None:
                raise RuntimeError(f"Failed to extract {name}")

            with open(path, "w") as target:
                # replace the font path
                css = WOFF_OR_TTF.sub("", file.read().decode()).replace(
                    "url(fonts/", "url(../fonts/katex/"
                )
                target.write(css)

            template = template.replace(
                name,
                path.relative_to(THEME_PATH).__str__(),
            )
    return template


def extract_fonts(tarpath: Union[str, Path]):
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tarpath, "r:gz") as archive:
        for member in archive.getmembers():
            if member.name.startswith("katex/fonts/") and member.name.endswith(
                ".woff2"
            ):
                font = archive.extractfile(member)
                if font is None:
                    raise RuntimeError(f"Failed to extract {member.name}")

                font_path = FONTS_DIR / os.path.basename(member.name)
                log(
                    f"Extracting {member.name} to {font_path.relative_to(THEME_PATH)}"
                )
                with open(font_path, "wb") as target:
                    target.write(font.read())


def katex(
    tag: Annotated[
        str,
        typer.Option(
            help="Specify the KaTeX release tag (see https://github.com/KaTeX/KaTeX/releases)"
        ),
    ] = "latest",
):
    """Download the specified release of KaTeX from GitHub,
    and install CSS, JS, font files and update templates accordingly.
    """
    repo: Repository = GH.get_repo(REPO)

    try:
        release = get_release(repo, tag)
        info(f"Installing release {release.tag_name}")
        tar = download_tarball(release)
        template = extract_css_js(tar.name)
        extract_fonts(tar.name)
        info(f"Writing {ARITMATEX_TEMPLATE_FILE.relative_to(THEME_PATH)}")
        with open(ARITMATEX_TEMPLATE_FILE, "w") as f:
            f.write(template)
    except RuntimeError as e:
        error(f"{e}")
    finally:
        if "tar" in locals():
            os.unlink(tar.name)
