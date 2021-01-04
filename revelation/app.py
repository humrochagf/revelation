"""
Main revelation module

It has the Revelation main class that creates the webserver do run
the presentation
"""

import os
import re

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

    def __init__(
        self,
        presentation,
        config=None,
        media=None,
        theme=None,
        style=None,
    ):
        """
        Initializes the server and creates the environment for the presentation
        """
        self.config = Config(config)
        self.presentation = presentation

        shared_data = {
            "/static": os.path.join(os.path.dirname(__file__), "static")
        }

        shared_data.update(self.parse_shared_data(media))
        shared_data.update(self.parse_shared_data(theme))

        if style:
            self.style = os.path.basename(style)
            shared_data.update(self.parse_shared_data(style))
        else:
            self.style = None

        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, shared_data)

    def parse_shared_data(self, shared_root):
        """
        Parse aditional shared_data if it exists
        """
        if shared_root:
            shared_root = os.path.abspath(shared_root)

            if os.path.exists(shared_root):
                shared_url = f"/{os.path.basename(shared_root)}"

                return {shared_url: shared_root}

        return {}

    def load_slides(self, path, section_separator, vertical_separator):
        """
        Get slides file from the given path, loads it and split into list
        of slides.

        :return: a list of strings with the slides content
        """
        with open(path, "rb") as presentation:
            slides = normalize_newlines(presentation.read().decode("utf-8"))

        return [
            re.split(f"^{vertical_separator}$", section, flags=re.MULTILINE)
            for section in re.split(
                f"^{section_separator}$", slides, flags=re.MULTILINE
            )
        ]

    def get_theme(self, theme):
        reveal_theme = f"static/revealjs/dist/theme/{theme}.css"
        fullpath_theme = os.path.join(os.path.dirname(__file__), reveal_theme)

        if os.path.isfile(fullpath_theme):
            return reveal_theme

        return theme

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
            "style": self.style,
        }

        template = env.get_template("presentation.html")

        return Response(
            template.render(**context), headers={"content-type": "text/html"}
        )

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
