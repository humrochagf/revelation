# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple

from revelation import Revelation

if __name__ == '__main__':
    app = Revelation(
        './example_slides/slides.md',
        './example_slides/img',
        './example_slides/config.py'
    )

    run_simple('localhost', 4000, app, use_debugger=True, use_reloader=True)
