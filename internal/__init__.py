import typer

from .i18n import compilemessages, makemessages
from .integrity import integrity
from .katex import katex
from .serve import runserver
from .test import test

app = typer.Typer(help="mkdocs-shadcn dev cli")

app.command()(integrity)
app.command()(katex)
app.command()(makemessages)
app.command()(compilemessages)
app.command()(runserver)
app.command()(test)
