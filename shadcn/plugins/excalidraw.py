import json
import os

from bottle import request, response  # type: ignore
from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger

from ._router import RouterMixin

log = get_plugin_logger("excalidraw")


def svg_handler_factory(directory: str):
    """
    Attributes:
        directory (str): Directory where the SVG files are stored. This is relative to the docs_dir.
    """

    def handler():
        file = request.query.get("file")
        svg_file = os.path.join(directory, file.replace(".json", ".svg"))

        if request.method == "POST":
            log.info(f"POST {request.path}?{request.query_string}")
            log.debug(f"opening {svg_file} for writing request body")
            with open(svg_file, "wb") as f:
                f.write(request.body.read())

        elif request.method == "GET":
            log.info(f"GET {request.path}?{request.query_string}")
            if not os.path.exists(svg_file):
                log.warning(f"file {svg_file} not found, creating it")
                with open(svg_file, "w") as f:
                    # default height to 400px
                    f.write(
                        f"""<svg id="{file}" version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 670 400" width="100%" height="400"></svg>"""
                    )
            response.content_type = "image/svg+xml"
            return open(svg_file, "r").read().strip()

    return handler


def scene_handler_factory(directory: str):
    def handler():
        file = request.query.get("file")
        scene_file = os.path.join(directory, file)

        if request.method == "POST":
            log.info(f"POST {request.path}?{request.query_string}")
            data = request.json
            if data:
                # we have an issue since excalidraw pass an object but
                # expect an array
                log.debug(f"saving state to {scene_file}")
                del data["appState"]["collaborators"]
                with open(scene_file, "w") as f:
                    json.dump(data, f, indent=2)
            else:
                log.warning("no data in request body")

        elif request.method == "GET":
            log.info(f"GET {request.path}?{request.query_string}")
            if not os.path.exists(scene_file):
                log.warning(f"file {scene_file} not found, creating it")
                with open(scene_file, "w") as f:
                    json.dump({"elements": [], "appState": {}, "files": {}}, f)

            response.content_type = "application/json"
            return open(scene_file, "r").read().strip()

    return handler


class ExcalidrawPluginConfig(Config):
    # Directory where the excalidraw files are stored
    # relative to the docs_dir
    directory = c.Dir(
        exists=False,
        default="excalidraw",
    )


class ExcalidrawPlugin(RouterMixin, BasePlugin[ExcalidrawPluginConfig]):
    """This plugin enabled the real time edition of
    excalidraw scenes in development mode"""

    is_dev_server = False
    """Internal flag to detect if we are in development mode."""

    def on_startup(self, *, command, dirty: bool):
        """Detect if the server is running in development mode."""
        self.is_dev_server = command == "serve"

    def on_config(self, config: MkDocsConfig, **kwargs):
        """Three operations are performed:

        - detect and create the excalidraw directory
        - load the internal excalidraw markdown extension
        - inject the HTTP routes needed to handle excalidraw scenes and SVGs
        """
        base = os.path.dirname(config["config_file_path"])
        excalidraw_path = os.path.join(base, self.config.directory)
        extension_config = {
            "base_dir": excalidraw_path,
            "svg_only": not self.is_dev_server,
        }
        log.debug(
            f"Loading markdown extension 'shadcn.extensions.excalidraw' "
            f"with configuration: {extension_config}"
        )
        config["markdown_extensions"].append("shadcn.extensions.excalidraw")
        config["mdx_configs"]["shadcn.extensions.excalidraw"] = (
            extension_config
        )
        # create directory
        log.debug(f"creating excalidraw directory: {excalidraw_path}")
        os.makedirs(excalidraw_path, exist_ok=True)

        # these routes are injected in on_serve
        log.debug("injecting HTTP routes for excalidraw plugin")
        self.add_route(
            "/excalidraw/scene",
            scene_handler_factory(excalidraw_path),
            method=["GET", "POST"],
        )
        self.add_route(
            "/excalidraw/svg",
            svg_handler_factory(excalidraw_path),
            method=["GET", "POST"],
        )
