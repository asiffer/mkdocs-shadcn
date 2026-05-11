from typing import Annotated

import typer
from properdocs.__main__ import serve_command

from internal.common import BASE_PATH

PAGES_DIR = BASE_PATH / "pages"
PAGES_CONFIG = PAGES_DIR / "mkdocs.yml"


def runserver(
    verbose: Annotated[
        bool, typer.Option(help="Enable verbose output")
    ] = False,
):
    """Run the ProperDocs development server."""
    args = [f"--config-file={PAGES_CONFIG}", "--watch-theme", "--dirty"]
    if verbose:
        args.append("--verbose")

    serve_command(
        args,
        standalone_mode=False,
    )
