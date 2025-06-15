from pathlib import Path

from platformdirs import user_cache_dir

REVEAL_URL = "https://github.com/hakimel/reveal.js/archive/master.zip"

STATIC_ROOT = Path(user_cache_dir(appname="revelation")) / "static"

REVEALJS_DIR = STATIC_ROOT / "revealjs"
