"""
Main revelation module

It has the Revelation main class that creates the webserver do run
the presentation
"""

import os
import re
from pathlib import Path
from typing import Optional

from jinja2 import Environment, PackageLoader, select_autoescape
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Request, Response

from .config import Config
from .utils import normalize_newlines


class Revelation(object):
    """
    Main revelation app class that instantiates the server and handles
    the requests
    """

    presentation: Path
    config: Config
    media: Optional[Path]
    theme: Optional[Path]
    style: Optional[Path]

    def __init__(
        self,
        presentation: Path,
        config: Optional[Path] = None,
        media: Optional[Path] = None,
        theme: Optional[Path] = None,
        style: Optional[Path] = None,
    ):
        """
        Initializes the server and creates the environment for the presentation
        """
        self.presentation = presentation
        self.config = Config(config)
        self.media = media
        self.theme = theme
        self.style = style

        shared_data = {
            "/static": os.path.join(os.path.dirname(__file__), "static")
        }

        shared_data.update(self.parse_shared_data(self.media))
        shared_data.update(self.parse_shared_data(self.theme))
        shared_data.update(self.parse_shared_data(self.style))

        self.wsgi_app = SharedDataMiddleware(self._wsgi_app, shared_data)

    def parse_shared_data(self, shared_root: Optional[Path]) -> dict:
        """
        Parse aditional shared_data if it exists
        """
        if shared_root and shared_root.exists():
            shared_root = shared_root.resolve()
            shared_url = f"/{shared_root.name}"

            return {shared_url: str(shared_root)}

        return {}

    def load_slides(
        self,
        path: Path,
        section_separator: str,
        vertical_separator: str,
    ):
        """
        Get slides file from the given path, loads it and split into list
        of slides.

        :return: a list of strings with the slides content
        """
        with path.open("rb") as fp:
            slides = normalize_newlines(fp.read().decode("utf-8"))

        return [
            re.split(f"^{vertical_separator}$", section, flags=re.MULTILINE)
            for section in re.split(
                f"^{section_separator}$", slides, flags=re.MULTILINE
            )
        ]

    def get_theme(self, theme_name: str):
        reveal_theme = f"static/revealjs/dist/theme/{theme_name}.css"
        fullpath_theme = os.path.join(os.path.dirname(__file__), reveal_theme)

        if os.path.isfile(fullpath_theme):
            return reveal_theme

        return theme_name

    def dispatch_request(self, request):
        env = Environment(
            loader=PackageLoader("revelation", "templates"),
            autoescape=select_autoescape(["html"]),
        )

        context = {
            "meta": self.config.get("REVEAL_META"),
            "slides": self.load_slides(
                self.presentation,
                self.config.get("REVEAL_SLIDE_SEPARATOR"),
                self.config.get("REVEAL_VERTICAL_SLIDE_SEPARATOR"),
            ),
            "config": self.config.get("REVEAL_CONFIG"),
            "theme": self.get_theme(self.config.get("REVEAL_THEME")),
            "style": getattr(self.style, "name", None),
        }

        template = env.get_template("presentation.html")

        return Response(
            template.render(**context), headers={"content-type": "text/html"}
        )

    def _wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
