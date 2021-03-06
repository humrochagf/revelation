from pathlib import Path

import revelation

REVEAL_URL = "https://github.com/hakimel/reveal.js/archive/master.zip"
MATHJAX_URL = "https://github.com/mathjax/MathJax/archive/2.7.9.zip"

STATIC_ROOT = Path(revelation.__file__).parent / "static"

REVEALJS_DIR = STATIC_ROOT / "revealjs"
MATHJAX_DIR = STATIC_ROOT / "mathjax"
