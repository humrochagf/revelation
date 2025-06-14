from pathlib import Path
from typing import Annotated

from typer import Option

RevealUrl = Annotated[str, Option("--url", "-u", help="Reveal.js download url")]
ServerPort = Annotated[int, Option("--port", "-p", help="Presentation server port")]
ConfigFile = Annotated[Path | None, Option("--config", "-c", help="Custom config file")]
MediaDir = Annotated[Path | None, Option("--media", "-m", help="Custom media folder")]
ThemeDir = Annotated[Path | None, Option("--theme", "-t", help="Custom theme folder")]
StyleOverrideFile = Annotated[
    Path | None,
    Option(
        "--style-override-file",
        "-s",
        help="Custom css file to override reveal.js styles",
    ),
]
OutputFile = Annotated[
    Path, Option("--output-file", "-f", help="File name of the static presentation")
]
OutputFolder = Annotated[
    Path,
    Option(
        "--output-folder",
        "-o",
        help="Folder where the static presentation will be generated",
    ),
]
OverwriteOutputFlag = Annotated[
    bool, Option("--force", "-r", help="Overwrite the output folder if exists")
]
DebugFlag = Annotated[
    bool, Option("--debug", "-d", help="Run the revelation server on debug mode")
]
