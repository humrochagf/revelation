# -*- coding: utf-8 -*-

import os

import click
from werkzeug.serving import run_simple

import revelation


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, default=False)
@click.pass_context
def cli(ctx, version):
    if not ctx.invoked_subcommand and version:
        click.echo(revelation.__version__)
        ctx.exit()
    elif not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


@cli.command('start', help='Start revelation server')
@click.argument('path', default=os.getcwd())
@click.option('--port', '-p', default=4000, help='Presentation server port')
@click.option('--config', '-c', default=None, help='Custom configuration file')
@click.option('--media', '-m', default=None, help='Custom media folder')
@click.option('--debug', '-d', is_flag=True, default=False,
              help='Run the revelation server in debugger and reloader on')
def start(path, port, config, media, debug):
    app = revelation.Revelation(path)

    if debug:
        run_simple(
            'localhost', port, app, use_debugger=True, use_reloader=True)
    else:
        run_simple('localhost', port, app)
