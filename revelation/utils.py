# -*- coding: utf-8 -*-

import os
import shutil

from . import default_config


def make_presentation(presentation_path):
    '''
    Make a new presentation boilerplate code given a presentation_path
    '''
    name = os.path.basename(presentation_path)
    # Presentation dir
    os.mkdir(name)
    # Media dir
    os.mkdir(os.path.join(presentation_path, 'media'))
    # Config file
    shutil.copy(
        default_config.__file__,
        os.path.join(presentation_path, 'config.py')
    )
    # Slide file
    with open(os.path.join(presentation_path, 'slides.md'), 'w') as f:
        f.write('# {0}\n\nStart from here!'.format(
            name.replace('_', ' ').replace('-', ' ').title()))
