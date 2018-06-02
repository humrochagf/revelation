# -*- coding: utf-8 -*-

import os
import types

from werkzeug.utils import import_string

from . import default_config


class Config(dict):
    """
    Class that stores revelation configs thanks to flask Config:

    https://github.com/pallets/flask/blob/master/flask/config.py

    It loads the default_config variables and if a path is passed it also
    loads the external configs
    """

    def __init__(self, filename=None):
        self.load_from_object(default_config)

        if filename and os.path.isfile(filename):
            self.load_from_pyfile(filename)

    def load_from_object(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)

        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def load_from_pyfile(self, filename):
        d = types.ModuleType("config")
        d.__file__ = filename

        try:
            with open(filename, mode="rb") as config_file:
                exec(compile(config_file.read(), filename, "exec"), d.__dict__)
        except IOError as e:
            e.strerror = "Unable to load configuration file (%s)" % e.strerror
            raise

        self.load_from_object(d)
