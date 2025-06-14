"""Cli tool to handle revelation commands"""

import glob
import shutil
from pathlib import Path
from typing import Any

import typer
from typer.main import get_command
from werkzeug.serving import run_simple

import revelation
from revelation import Revelation
from revelation.cli_types import (
    ConfigFile,
    DebugFlag,
    MediaDir,
    OutputFile,
    OutputFolder,
    OverwriteOutputFlag,
    RevealUrl,
    ServerPort,
    StyleOverrideFile,
    ThemeDir,
)
from revelation.constants import (
    MATHJAX_DIR,
    MATHJAX_URL,
    REVEAL_URL,
    REVEALJS_DIR,
)
from revelation.utils import (
    download_file,
    extract_file,
    make_presentation,
    move_and_replace,
)

cli = typer.Typer()
echo = typer.echo


def error(message: str) -> None:
    typer.secho(f"Error: {message}", err=True, fg="red", bold=True)


def revelation_factory(
    presentation: Path,
    config: ConfigFile = None,
    media: MediaDir = None,
    theme: ThemeDir = None,
    style: StyleOverrideFile = None,
) -> Revelation:
    if presentation.is_file():
        path = presentation.parent
    else:
        error("Presentation file not found.")

        raise typer.Abort()

    if style and (not style.is_file() or not style.suffix == ".css"):
        error("Style is not a css file or does not exists.")

        raise typer.Abort()

    if not media:
        media = path / "media"

    if not media.is_dir():
        media = None

        echo("Media folder not detected, running without media.")

    if not theme:
        theme = path / "theme"

    if not theme.is_dir():
        theme = None

        echo("Theme not detected, running without custom theme.")

    if not config:
        config = path / "config.py"

    if config and not config.is_file():
        config = None

        echo("Configuration file not detected, running with defaults.")

    return Revelation(presentation, config, media, theme, style)


@cli.command()
def version() -> None:
    """
    Show version
    """
    echo(revelation.__version__)


@cli.command()
def installreveal(url: RevealUrl = REVEAL_URL) -> None:
    """
    Install or upgrade reveal.js dependency

    Receives the download url to install from a specific version or
    downloads the latest version if noting is passed
    """
    echo("Downloading reveal.js...")

    download = download_file(url)

    echo("Installing reveal.js...")

    move_and_replace(extract_file(download[0]), REVEALJS_DIR)

    echo("Downloading MathJax...")

    download = download_file(MATHJAX_URL)

    echo("Installing MathJax...")

    move_and_replace(extract_file(download[0]), MATHJAX_DIR)

    echo("Installation completed!")


@cli.command()
def mkpresentation(presentation: Path) -> None:
    """Create a new revelation presentation"""
    if presentation.exists():
        error(f"'{presentation}' already exists.")

        raise typer.Abort()

    echo("Starting a new presentation...")

    make_presentation(presentation)


@cli.command()
def mkstatic(
    ctx: typer.Context,
    presentation: Path,
    *,
    config: ConfigFile = None,
    media: MediaDir = None,
    theme: ThemeDir = None,
    output_folder: OutputFolder = Path("output"),
    output_file: OutputFile = Path("index.html"),
    force: OverwriteOutputFlag = False,
    style: StyleOverrideFile = None,
) -> None:
    """Make static presentation"""

    if not REVEALJS_DIR.exists():
        echo("Reveal.js not found, running installation...")

        # Change after fix on https://github.com/tiangolo/typer/issues/102
        ctx.invoke(
            get_command(cli).get_command(ctx, "installreveal")  # type: ignore
        )

    if output_folder.is_dir():
        if force:
            shutil.rmtree(output_folder)
        else:
            error(f"'{output_folder}' already exists, use --force to override it.")

            raise typer.Abort()

    if output_folder.is_file():
        error(f"'{output_folder}' already exists and is a file.")

        raise typer.Abort()

    app = revelation_factory(presentation, config, media, theme, style)

    echo("Generating static presentation...")

    staticfolder = output_folder / "static"

    output_folder.mkdir(parents=True, exist_ok=True)

    if app.style:
        shutil.copy(app.style, output_folder / app.style.name)

    shutil.copytree(REVEALJS_DIR, staticfolder / "revealjs")

    if app.media:
        shutil.copytree(app.media, output_folder / "media")

    if app.theme:
        shutil.copytree(app.theme, output_folder / "theme")

    output_folder = output_folder.resolve()

    if not output_folder.is_dir():
        output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / output_file

    with output_file.open("wb") as fp:
        fp.write(app.dispatch_request().get_data(as_text=True).encode("utf-8"))

    echo(f"Static presentation generated in {output_folder}")


@cli.command()
def start(
    ctx: typer.Context,
    presentation: Path,
    *,
    port: ServerPort = 4000,
    config: ConfigFile = None,
    media: MediaDir = None,
    theme: ThemeDir = None,
    style: StyleOverrideFile = None,
    debug: DebugFlag = False,
) -> None:
    """Start the revelation server"""

    if not REVEALJS_DIR.exists():
        echo("Reveal.js not found, running installation...")

        # Change after fix on https://github.com/tiangolo/typer/issues/102
        ctx.invoke(
            get_command(cli).get_command(ctx, "installreveal")  # type: ignore
        )

    app = revelation_factory(presentation, config, media, theme, style)

    presentation_root = presentation.parent

    echo("Starting revelation server...")

    server_args: dict[str, Any] = {
        "hostname": "localhost",
        "port": port,
        "application": app,
        "use_reloader": False,
    }

    if debug:
        server_args["use_debugger"] = True
        server_args["use_reloader"] = True
        server_args["reloader_type"] = "watchdog"
        server_args["extra_files"] = glob.glob(
            str(presentation_root / "*.md")
        ) + glob.glob(str(presentation_root / "*.css"))

    run_simple(**server_args)
