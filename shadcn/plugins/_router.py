from functools import wraps
from typing import Callable, List, Union

from bottle import Bottle  # type: ignore
from mkdocs.livereload import LiveReloadServer


class RouterMixin:
    """Mixin to add custom routes to the mkdocs dev server."""

    def __init__(self):
        # we use bottle to handle our routes
        # its .wsgi() method is very convenient with regards to
        # the _serve_request method of the mkdocs dev server
        self.bottle = Bottle()

    def add_route(
        self,
        path: str,
        handler: Callable,
        method: Union[str, List[str]] = "GET",
    ):
        """Add a route to the router."""
        self.bottle.route(path, method=method)(handler)  # type: ignore

    def extend_server(self, server: LiveReloadServer):
        """Extend the mkdocs dev server to add custom behavior."""
        original = server._serve_request

        @wraps(original)
        def _serve_request(environ, start_response):
            # put priority to base routes
            result = original(environ, start_response)
            if result is not None:
                return result
            # run our extra route handler
            return self.bottle.wsgi(environ, start_response)

        # monkey patch the _serve_request method of the server
        setattr(server, "_serve_request", _serve_request)

    def on_serve(self, server: LiveReloadServer, /, *, config, builder):
        """This method is called when the server is started. At the end of the mkdocs
        workflow. At this moment we have access to the live server to inject our new
        routes.
        See https://www.mkdocs.org/dev-guide/plugins/#events to see the mkdocs workflow.
        """
        self.extend_server(server)
