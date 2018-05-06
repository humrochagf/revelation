# -*- coding: utf-8 -*-

import os
import re

from jinja2 import Environment, PackageLoader, select_autoescape
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

from .config import Config


class Revelation(object):
    '''
    Main revelation app class that instantiates the server and handles
    the requests
    '''

    def __init__(self, presentation, config=None, media=None, theme=None):
        '''
        Initializes the server and creates the environment for the presentation
        '''
        self.config = Config(config)
        self.presentation = presentation

        shared_data = {
            '/static': os.path.join(os.path.dirname(__file__), 'static'),
        }

        shared_data.update(self.parse_shared_data(media))
        shared_data.update(self.parse_shared_data(theme))

        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, shared_data)

    def parse_shared_data(self, shared_root):
        '''
        Parse aditional shared_data if it exists
        '''
        if shared_root:
            shared_root = os.path.abspath(shared_root)

            if os.path.isdir(shared_root):
                shared_url = '/{}'.format(os.path.basename(shared_root))

                return {shared_url: shared_root}

        return {}

    def load_slides(self, path, separator):
        '''
        Get slides file from the given path, loads it and split into list
        of slides.

        :return: a list of strings with the slides content
        '''
        with open(path, 'r') as presentation:
            slides = presentation.read()

        return re.split('^{}$'.format(separator), slides, flags=re.MULTILINE)

    def get_theme(self, theme):
        reveal_theme = 'static/revealjs/css/theme/{}.css'.format(theme)

        if os.path.isfile(os.path.join(
                os.path.dirname(__file__), reveal_theme)):
            return reveal_theme

        return theme

    def dispatch_request(self, request):
        env = Environment(
            loader=PackageLoader('revelation', 'templates'),
            autoescape=select_autoescape(['html'])
        )

        context = {
            'meta': self.config.get('REVEAL_META'),
            'slides': self.load_slides(
                self.presentation, self.config.get('REVEAL_SLIDE_SEPARATOR')),
            'config': self.config.get('REVEAL_CONFIG'),
            'theme': self.get_theme(self.config.get('REVEAL_THEME')),
        }

        template = env.get_template('presentation.html')

        return Response(
            template.render(**context),
            headers={'content-type': 'text/html'}
        )

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
