# -*- coding: utf-8 -*-

import os

import click
from werkzeug.serving import run_simple

import revelation
from revelation.utils import (download_reveal, extract_file, make_presentation,
                              move_and_replace)


REVEALJS_FOLDER = os.path.join(os.path.join(
    os.path.dirname(revelation.__file__), 'static'), 'revealjs')


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, default=False)
@click.pass_context
def cli(ctx, version):
    if not ctx.invoked_subcommand and version:
        click.echo(revelation.__version__)
        ctx.exit()
    elif not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


@cli.command('installreveal', help='Install or upgrade reveal.js dependency')
@click.option('--url', '-u', help='Reveal.js download url')
@click.pass_context
def installreveal(ctx, url):
    click.echo('Downloading reveal.js...')

    download = download_reveal(url)

    click.echo('Installing reveal.js...')

    move_and_replace(extract_file(download[0]), REVEALJS_FOLDER)

    click.echo('Installation completed!')


@cli.command('mkpresentation', help='Create a new revelation presentation')
@click.argument('presentation')
@click.pass_context
def mkpresentation(ctx, presentation):
    if os.path.exists(presentation):
        click.echo('This presentation already exists')
        ctx.exit()

    click.echo('Starting a new presentation...')
    make_presentation(presentation)


@cli.command('start', help='Start the revelation server')
@click.argument('presentation', default=os.getcwd())
@click.option('--port', '-p', default=4000, help='Presentation server port')
@click.option('--config', '-c', default=None, help='Custom configuration file')
@click.option('--media', '-m', default=None, help='Custom media folder')
@click.option('--theme', '-t', default=None, help='Custom theme folder')
@click.option('--debug', '-d', is_flag=True, default=False,
              help='Run the revelation server in debugger and reloader on')
@click.pass_context
def start(ctx, presentation, port, config, media, theme, debug):
    # Check if reveal.js is installed
    if not os.path.exists(REVEALJS_FOLDER):
        click.echo('You must run installreveal command first')
        ctx.exit()

    # Check for presentation file
    if os.path.isfile(presentation):
        path = os.path.dirname(presentation)
    else:
        click.echo('Presentation file not found')
        ctx.exit()

    # Check for media root
    if not media:
        media = os.path.join(path, 'media')

    if not os.path.isdir(media):
        # Running without media folder
        media = None

        click.echo('Media folder not detected, running without media')

    # Check for theme root
    if not theme:
        theme = os.path.join(path, 'theme')

    if not os.path.isdir(theme):
        # Running without theme folder
        theme = None

    # Check for configuration file
    if not config:
        config = os.path.join(path, 'config.py')

    if not os.path.isfile(config):
        # Running without configuration file
        config = None

        click.echo('Configuration file not detected, running with defaults')

    click.echo('Starting revelation server...')

    # instatiating revelation app
    app = revelation.Revelation(presentation, config, media, theme)

    if debug:
        run_simple(
            'localhost', port, app, use_debugger=True, use_reloader=True)
    else:
        run_simple('localhost', port, app)
