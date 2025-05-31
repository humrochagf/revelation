from pathlib import Path

REVEAL_URL = "https://github.com/hakimel/reveal.js/archive/master.zip"
MATHJAX_URL = "https://github.com/mathjax/MathJax/archive/2.7.9.zip"

STATIC_ROOT = Path.home() / ".local" / "share" / "revelation" / "static"

REVEALJS_DIR = STATIC_ROOT / "revealjs"
MATHJAX_DIR = STATIC_ROOT / "mathjax"
