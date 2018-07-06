# -*- coding: utf-8 -*-
"""Main revelation module

It has the Revelation main class that creates the webserver do run
the presentation
"""

import json
import os
import re

from geventwebsocket import WebSocketApplication
from jinja2 import Environment, PackageLoader, select_autoescape
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

from .config import Config


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
        reloader=False,
    ):
        """
        Initializes the server and creates the environment for the presentation
        """
        self.config = Config(config)
        self.presentation = presentation
        self.reloader = reloader

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
                shared_url = "/{}".format(os.path.basename(shared_root))

                return {shared_url: shared_root}

        return {}

    def load_slides(self, path, separator):
        """
        Get slides file from the given path, loads it and split into list
        of slides.

        :return: a list of strings with the slides content
        """
        with open(path, "r") as presentation:
            slides = presentation.read()

        return re.split("^{}$".format(separator), slides, flags=re.MULTILINE)

    def get_theme(self, theme):
        reveal_theme = "static/revealjs/css/theme/{}.css".format(theme)
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
                self.presentation, self.config.get("REVEAL_SLIDE_SEPARATOR")
            ),
            "config": self.config.get("REVEAL_CONFIG"),
            "theme": self.get_theme(self.config.get("REVEAL_THEME")),
            "style": self.style,
            "reloader": self.reloader,
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


class PresentationReloadWebSocketSendEvent(FileSystemEventHandler):
    def __init__(self, file, ws):
        self.file = file
        self.ws = ws

    def on_modified(self, event):
        if event.src_path == self.file and not self.ws.closed:
            self.ws.send(
                json.dumps({"msg_type": "message", "message": "reload"})
            )


class PresentationReloader(WebSocketApplication):

    presentation = None

    def on_open(self):
        if self.presentation:
            event_handler = PresentationReloadWebSocketSendEvent(
                self.presentation, self.ws
            )
            self.observer = Observer()
            self.observer.schedule(
                event_handler, os.path.dirname(self.presentation)
            )
            self.observer.start()

    def on_message(self, message, *args, **kwargs):
        pass

    def on_close(self, reason):
        self.observer.stop()
