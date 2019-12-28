"""Cli tool to handle revelation commands"""

import os
import shutil
from functools import partial

import click
from geventwebsocket import Resource, WebSocketServer
from werkzeug.debug import DebuggedApplication

import revelation
from revelation import PresentationReloader, Revelation
from revelation.utils import (
    download_reveal,
    extract_file,
    make_presentation,
    move_and_replace,
)

REVEALJS_FOLDER = os.path.join(
    os.path.join(os.path.dirname(revelation.__file__), "static"), "revealjs"
)

# DRY form for echoing errors
error_echo = partial(click.secho, err=True, fg="red", bold=True)


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, default=False)
@click.pass_context
def cli(ctx, version):
    """Base command function, it gets the context and passes it to
    its subcommands"""
    if not ctx.invoked_subcommand and version:
        click.echo(revelation.__version__)
        ctx.exit()
    elif not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


@cli.command("installreveal", help="Install or upgrade reveal.js dependency")
@click.option("--url", "-u", help="Reveal.js download url")
def installreveal(url):
    """Reveal.js installation command

    Receives the download url to install from a specific version or
    downloads the latest version if noting is passed
    """
    click.echo("Downloading reveal.js...")

    download = download_reveal(url)

    click.echo("Installing reveal.js...")

    move_and_replace(extract_file(download[0]), REVEALJS_FOLDER)

    click.echo("Installation completed!")


@cli.command("mkpresentation", help="Create a new revelation presentation")
@click.argument("presentation")
@click.pass_context
def mkpresentation(ctx, presentation):
    """Make presentation project boilerplate"""
    if os.path.exists(presentation):
        error_echo("Error: '{}' already exists.".format(presentation))
        ctx.exit(1)

    click.echo("Starting a new presentation...")

    make_presentation(presentation)


@cli.command("mkstatic", help="Make a static presentation")
@click.argument("presentation", default=os.getcwd())
@click.option("--config", "-c", default=None, help="Custom configuration file")
@click.option("--media", "-m", default=None, help="Custom media folder")
@click.option("--theme", "-t", default=None, help="Custom theme folder")
@click.option(
    "--style-override-file",
    "-s",
    "style",
    default=None,
    help="Custom css file to override reveal.js styles",
)
@click.option(
    "--output-folder",
    "-o",
    default="output",
    help="Folder where the static presentation will be generated",
)
@click.option(
    "--output-file",
    "-f",
    default="index.html",
    help="File name of the static presentation",
)
@click.option(
    "--force", "-r", is_flag=True, help="Overwrite the output folder if exists"
)
@click.pass_context
def mkstatic(
    ctx,
    presentation,
    config,
    media,
    theme,
    output_folder,
    output_file,
    force,
    style,
):
    """Make static presentation"""

    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        click.echo("Reveal.js not found, running installation...")
        ctx.invoke(installreveal)

    output_folder = os.path.realpath(output_folder)

    # Check for style override file
    if os.path.isfile(output_folder):
        error_echo(
            "Error: '{}' already exists and is a file.".format(output_folder)
        )
        ctx.exit(1)

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        error_echo("Error: Presentation file not found.")
        ctx.exit(1)

    if style and (not os.path.isfile(style) or not style.endswith(".css")):
        click.echo("Error: Style is not a css file or does not exists.")
        ctx.exit(1)

    if os.path.isdir(output_folder):
        if force:
            shutil.rmtree(output_folder)
        else:
            error_echo(
                (
                    "Error: '{}' already exists, use --force to override it."
                ).format(output_folder)
            )
            ctx.exit(1)

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
        click.echo("Media folder not detected, running without media.")
    else:
        shutil.copytree(media, os.path.join(output_folder, "media"))

    # Check for theme root
    if not theme:
        theme = os.path.join(path, "theme")

    if not os.path.isdir(theme):
        # Running without theme folder
        theme = None
        click.echo("Theme not detected, running without custom theme.")
    else:
        shutil.copytree(theme, os.path.join(output_folder, "theme"))

    # Check for configuration file
    if not config:
        config = os.path.join(path, "config.py")

    if not os.path.isfile(config):
        # Running without configuration file
        config = None

        click.echo("Configuration file not detected, running with defaults.")

    click.echo("Generating static presentation...")

    # instantiating revelation app
    app = Revelation(presentation, config, media, theme, style)

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, output_file)

    with open(output_file, "wb") as f:
        f.write(
            app.dispatch_request(None).get_data(as_text=True).encode("utf-8")
        )

    click.echo(
        "Static presentation generated in {}".format(
            os.path.realpath(output_folder)
        )
    )


@cli.command("start", help="Start the revelation server")
@click.argument("presentation", default=os.getcwd())
@click.option("--port", "-p", default=4000, help="Presentation server port")
@click.option("--config", "-c", default=None, help="Custom configuration file")
@click.option("--media", "-m", default=None, help="Custom media folder")
@click.option("--theme", "-t", default=None, help="Custom theme folder")
@click.option(
    "--style-override-file",
    "-s",
    "style",
    default=None,
    help="Custom css file to override reveal.js styles",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    default=False,
    help="Run the revelation server on debug mode",
)
@click.pass_context
def start(ctx, presentation, port, config, media, theme, style, debug):
    """Start revelation presentation command"""
    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        click.echo("Reveal.js not found, running installation...")
        ctx.invoke(installreveal)

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        click.echo("Error: Presentation file not found.")
        ctx.exit(1)

    # Check for style override file
    if style and (not os.path.isfile(style) or not style.endswith(".css")):
        click.echo("Error: Style is not a css file or does not exists.")
        ctx.exit(1)

    # Check for media root
    if not media:
        media = os.path.join(path, "media")

    if not os.path.isdir(media):
        # Running without media folder
        media = None

        click.echo("Media folder not detected, running without media")

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

        click.echo("Configuration file not detected, running with defaults.")

    click.echo("Starting revelation server...")

    # instantiating revelation app
    app = Revelation(presentation, config, media, theme, style, True)

    if debug:
        app = DebuggedApplication(app)

    PresentationReloader.tracking_path = os.path.abspath(path)

    click.echo("Running at http://localhost:{}".format(port))

    WebSocketServer(
        ("localhost", port),
        Resource(
            [
                ("^/reloader.*", PresentationReloader),
                ("^/.*", DebuggedApplication(app)),
            ]
        ),
    ).serve_forever()
