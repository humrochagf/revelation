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

    def __init__(self, slides_file, media_root=None, config=None, debug=False):
        '''
        Initializes the server and creates the environment for the presentation
        '''
        self.config = Config(config)
        self.slides_file = slides_file

        shared_data = {
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        }

        shared_data.update(self.parse_media_root(media_root))

        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, shared_data)

    def parse_media_root(self, media_root):
        '''
        Create the shared_data configuration for media_root
        if the folder exists
        '''
        if media_root:
            media_root = os.path.abspath(media_root)

            if os.path.isdir(media_root):
                media_url = '/{}'.format(os.path.basename(media_root))

                return {media_url: media_root}

        return {}

    def load_slides(self, path, separator):
        '''
        Get slides file from the given path, loads it and split into list
        of slides.

        :return: a list of strings with the slides content
        '''
        with open(path, 'r') as slides_file:
            slides = slides_file.read()

        return re.split('^{}$'.format(separator), slides, flags=re.MULTILINE)

    def dispatch_request(self, request):
        env = Environment(
            loader=PackageLoader('revelation', 'templates'),
            autoescape=select_autoescape(['html'])
        )

        context = {
            'meta': self.config.get('REVEAL_META'),
            'slides': self.load_slides(
                self.slides_file, self.config.get('REVEAL_SLIDE_SEPARATOR')),
            'config': self.config.get('REVEAL_CONFIG'),
            'theme': 'static/css/theme/{}.css'.format(
                self.config.get('REVEAL_THEME')),
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
