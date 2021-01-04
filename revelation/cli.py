"""Cli tool to handle revelation commands"""

import glob
import os
import shutil

import typer
from typer import Option
from werkzeug.serving import run_simple

import revelation
from revelation import Revelation
from revelation.utils import (
    MATHJAX_URL,
    REVEAL_URL,
    download_file,
    extract_file,
    make_presentation,
    move_and_replace,
)

REVEALJS_FOLDER = os.path.join(
    os.path.join(os.path.dirname(revelation.__file__), "static"), "revealjs"
)

MATHJAX_FOLDER = os.path.join(
    os.path.join(os.path.dirname(revelation.__file__), "static"), "mathjax"
)

cli = typer.Typer()
echo = typer.echo


def error(message: str):
    typer.secho(f"Error: {message}", err=True, fg="red", bold=True)


@cli.command()
def version():
    """
    Show version
    """
    echo(revelation.__version__)


@cli.command()
def installreveal(
    url: str = Option(REVEAL_URL, "--url", "-u", help="Reveal.js download url")
):
    """
    Install or upgrade reveal.js dependency

    Receives the download url to install from a specific version or
    downloads the latest version if noting is passed
    """
    echo("Downloading reveal.js...")

    download = download_file(url)

    echo("Installing reveal.js...")

    move_and_replace(extract_file(download[0]), REVEALJS_FOLDER)

    echo("Downloading MathJax...")

    download = download_file(MATHJAX_URL)

    echo("Installing MathJax...")

    move_and_replace(extract_file(download[0]), MATHJAX_FOLDER)

    echo("Installation completed!")


@cli.command()
def mkpresentation(presentation: str):
    """Create a new revelation presentation"""
    if os.path.exists(presentation):
        error(f"'{presentation}' already exists.")

        raise typer.Abort()

    echo("Starting a new presentation...")

    make_presentation(presentation)


@cli.command()
def mkstatic(
    ctx: typer.Context,
    presentation: str,
    config: str = Option(None, "--config", "-c", help="Custom config file"),
    media: str = Option(None, "--media", "-m", help="Custom media folder"),
    theme: str = Option(None, "--theme", "-t", help="Custom theme folder"),
    output_folder: str = Option(
        "output",
        "--output-folder",
        "-o",
        help="Folder where the static presentation will be generated",
    ),
    output_file: str = Option(
        "index.html",
        "--output-file",
        "-f",
        help="File name of the static presentation",
    ),
    force: bool = Option(
        False,
        "--force",
        "-r",
        help="Overwrite the output folder if exists",
    ),
    style: str = Option(
        None,
        "--style-override-file",
        "-s",
        help="Custom css file to override reveal.js styles",
    ),
):
    """Make static presentation"""

    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        echo("Reveal.js not found, running installation...")

        # Change after fix on https://github.com/tiangolo/typer/issues/102
        ctx.invoke(
            typer.main.get_command(cli).get_command(ctx, "installreveal")
        )

    output_folder = os.path.realpath(output_folder)

    # Check for style override file
    if os.path.isfile(output_folder):
        error(f"'{output_folder}' already exists and is a file.")

        raise typer.Abort()

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        error("Presentation file not found.")

        raise typer.Abort()

    if style and (not os.path.isfile(style) or not style.endswith(".css")):
        error("Style is not a css file or does not exists.")

        raise typer.Abort()

    if os.path.isdir(output_folder):
        if force:
            shutil.rmtree(output_folder)
        else:
            error(
                f"'{output_folder}' already exists, "
                "use --force to override it."
            )

            raise typer.Abort()

    staticfolder = os.path.join(output_folder, "static")

    # make the output path
    os.makedirs(output_folder)

    # if has override style copy
    if style:
        shutil.copy(
            style, os.path.join(output_folder, os.path.basename(style))
        )

    shutil.copytree(REVEALJS_FOLDER, os.path.join(staticfolder, "revealjs"))

    # Check for media root
    if not media:
        media = os.path.realpath(os.path.join(path, "media"))
    else:
        media = os.path.realpath(media)

    if not os.path.isdir(media):
        # Running without media folder
        media = None
        echo("Media folder not detected, running without media.")
    else:
        shutil.copytree(media, os.path.join(output_folder, "media"))

    # Check for theme root
    if not theme:
        theme = os.path.join(path, "theme")

    if not os.path.isdir(theme):
        # Running without theme folder
        theme = None
        echo("Theme not detected, running without custom theme.")
    else:
        shutil.copytree(theme, os.path.join(output_folder, "theme"))

    # Check for configuration file
    if not config:
        config = os.path.join(path, "config.py")

    if not os.path.isfile(config):
        # Running without configuration file
        config = None

        echo("Configuration file not detected, running with defaults.")

    echo("Generating static presentation...")

    # instantiating revelation app
    app = Revelation(presentation, config, media, theme, style)

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, output_file)

    with open(output_file, "wb") as f:
        f.write(
            app.dispatch_request(None).get_data(as_text=True).encode("utf-8")
        )

    echo(f"Static presentation generated in {os.path.realpath(output_folder)}")


@cli.command()
def start(
    ctx: typer.Context,
    presentation: str,
    port: str = Option(4000, "--port", "-p", help="Presentation server port"),
    config: str = Option(None, "--config", "-c", help="Custom config file"),
    media: str = Option(None, "--media", "-m", help="Custom media folder"),
    theme: str = Option(None, "--theme", "-t", help="Custom theme folder"),
    style: str = Option(
        None,
        "--style-override-file",
        "-s",
        help="Custom css file to override reveal.js styles",
    ),
    debug: bool = Option(
        False,
        "--debug",
        "-d",
        is_flag=True,
        help="Run the revelation server on debug mode",
    ),
):
    """Start the revelation server"""
    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        echo("Reveal.js not found, running installation...")

        # Change after fix on https://github.com/tiangolo/typer/issues/102
        ctx.invoke(
            typer.main.get_command(cli).get_command(ctx, "installreveal")
        )

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        error("Presentation file not found.")

        raise typer.Abort()

    # Check for style override file
    if style and (not os.path.isfile(style) or not style.endswith(".css")):
        error("Style is not a css file or does not exists.")

        raise typer.Abort()

    # Check for media root
    if not media:
        media = os.path.join(path, "media")

    if not os.path.isdir(media):
        # Running without media folder
        media = None

        echo("Media folder not detected, running without media")

    # Check for theme root
    if not theme:
        theme = os.path.join(path, "theme")

    if not os.path.isdir(theme):
        # Running without theme folder
        theme = None

    # Check for configuration file
    if not config:
        config = os.path.join(path, "config.py")

    if not os.path.isfile(config):
        # Running without configuration file
        config = None

        echo("Configuration file not detected, running with defaults.")

    echo("Starting revelation server...")

    # instantiating revelation app
    app = Revelation(presentation, config, media, theme, style)

    server_args = {
        "hostname": "localhost",
        "port": port,
        "application": app,
        "use_reloader": False,
    }

    if debug:
        server_args["use_debugger"] = True
        server_args["use_reloader"] = True
        server_args["reloader_type"] = "watchdog"
        server_args["extra_files"] = glob.glob(os.path.join(path, "*.md"))
        server_args["extra_files"] += glob.glob(os.path.join(path, "*.css"))

    run_simple(**server_args)
