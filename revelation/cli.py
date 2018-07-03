# -*- coding: utf-8 -*-
"""Cli tool to handle revelation commands"""

import os
import shutil

import click
from geventwebsocket import Resource, WebSocketServer
from werkzeug.debug import DebuggedApplication

import revelation
from revelation import Revelation, PresentationReloader
from revelation.utils import (
    download_reveal,
    extract_file,
    make_presentation,
    move_and_replace,
)


REVEALJS_FOLDER = os.path.join(
    os.path.join(os.path.dirname(revelation.__file__), "static"), "revealjs"
)


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
        click.echo("This presentation already exists")
        ctx.exit()

    click.echo("Starting a new presentation...")
    make_presentation(presentation)


@cli.command("mkstatic", help="Make a static presentation")
@click.argument("presentation", default=os.getcwd())
@click.option("--config", "-c", default=None, help="Custom configuration file")
@click.option("--media", "-m", default=None, help="Custom media folder")
@click.option("--theme", "-t", default=None, help="Custom theme folder")
@click.option(
    "--outputfolder",
    "-o",
    default="output",
    help="Folder where the static presentation will be generated",
)
@click.option(
    "--outputfilename",
    "-f",
    default="index.html",
    help="Filename of the static presentation",
)
@click.option(
    "--force", "-r", default=False, help="Overwrite the outputfolder if exists"
)
@click.pass_context
def mkstatic(
    ctx,
    presentation,
    config,
    media,
    theme,
    outputfolder,
    outputfilename,
    force,
):
    """Make static presentation"""

    outputfolder = os.path.realpath(outputfolder)

    if os.path.isfile(outputfolder):
        click.echo("{} already exists and is a file".format(outputfolder))
        ctx.exit()

    if os.path.isdir(outputfolder):
        if force:
            shutil.rmtree(outputfolder)
        else:
            click.echo(
                (
                    "{} already exists. If you want to override it, "
                    "use --force or -r"
                ).format(outputfolder)
            )
            ctx.exit()

    staticfolder = os.path.join(outputfolder, "static")

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        click.echo("Presentation file not found")
        ctx.exit()

    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        click.echo("You must run installreveal command first")
        ctx.exit()
    else:
        shutil.copytree(
            REVEALJS_FOLDER, os.path.join(staticfolder, "revealjs")
        )

    # Check for media root
    if not media:
        media = os.path.realpath(os.path.join(path, "media"))
    else:
        media = os.path.realpath(media)

    if not os.path.isdir(media):
        # Running without media folder
        media = None
        click.echo("Media folder not detected, running without media")
    else:
        shutil.copytree(media, os.path.join(outputfolder, "media"))

    # Check for theme root
    if not theme:
        theme = os.path.join(path, "theme")

    if not os.path.isdir(theme):
        # Running without theme folder
        theme = None
        click.echo("Theme not detected, running without custom theme")
    else:
        shutil.copytree(theme, os.path.join(outputfolder, "theme"))

    # Check for configuration file
    if not config:
        config = os.path.join(path, "config.py")

    if not os.path.isfile(config):
        # Running without configuration file
        config = None

        click.echo("Configuration file not detected, running with defaults")

    click.echo("Generating static presentation...")

    # instatiating revelation app
    app = Revelation(presentation, config, media, theme)

    if not os.path.isdir(outputfolder):
        os.makedirs(outputfolder)

    output_filename = os.path.join(outputfolder, outputfilename)
    with open(output_filename, "w") as f:
        f.write(app.dispatch_request(None).get_data(as_text=True))

    click.echo(
        "Static presentation generated in {}".format(
            os.path.realpath(outputfolder)
        )
    )


@cli.command("start", help="Start the revelation server")
@click.argument("presentation", default=os.getcwd())
@click.option("--port", "-p", default=4000, help="Presentation server port")
@click.option("--config", "-c", default=None, help="Custom configuration file")
@click.option("--media", "-m", default=None, help="Custom media folder")
@click.option("--theme", "-t", default=None, help="Custom theme folder")
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    default=False,
    help="Run the revelation server in debugger and reloader on",
)
@click.pass_context
def start(ctx, presentation, port, config, media, theme, debug):
    """Start revelation presentation command"""
    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        click.echo("You must run installreveal command first")
        ctx.exit()

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        click.echo("Presentation file not found")
        ctx.exit()

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

        click.echo("Configuration file not detected, running with defaults")

    click.echo("Starting revelation server...")

    # instatiating revelation app
    app = Revelation(presentation, config, media, theme)

    if debug:
        app = DebuggedApplication(app)

    PresentationReloader.presentation = os.path.abspath(presentation)

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
