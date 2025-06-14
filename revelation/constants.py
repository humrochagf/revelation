from pathlib import Path

from platformdirs import user_cache_dir

REVEAL_URL = "https://github.com/hakimel/reveal.js/archive/master.zip"
MATHJAX_URL = "https://github.com/mathjax/MathJax/archive/2.7.9.zip"

STATIC_ROOT = Path(user_cache_dir(appname="revelation"))

REVEALJS_DIR = STATIC_ROOT / "revealjs"
MATHJAX_DIR = STATIC_ROOT / "mathjax"
