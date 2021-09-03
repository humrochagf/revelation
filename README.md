# Revelation

[![PyPI](https://img.shields.io/pypi/v/revelation.svg)](https://pypi.org/project/revelation/)
[![PyPI - License](https://img.shields.io/pypi/l/revelation.svg)](https://pypi.org/project/revelation/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/revelation.svg)](https://pypi.org/project/revelation/)
[![Actions Status](https://github.com/humrochagf/revelation/workflows/CI/badge.svg)](https://github.com/humrochagf/revelation/actions)
[![Coverage Status](https://coveralls.io/repos/github/humrochagf/revelation/badge.svg?branch=main)](https://coveralls.io/github/humrochagf/revelation?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[revelation](https://github.com/humrochagf/revelation) is a cli tool that makes your [revealjs](https://github.com/hakimel/reveal.js) presentations nice and easy using markdown and serving it locally.

## Features

- Presentation server to run it locally when you are offline.
- Presentation creation from template with a single command.
- Custom theming support with css.
- Export to static html tool.
- Debug mode with server auto refresh.

## Installation

You can install it with:

```shell
pip install revelation
```

Or with [pipx](https://pypa.github.io/pipx/):

```shell
pipx install revelation
```

## Usage

### Install/Update revealjs files

Revelation depends on revealjs to run its presentation and every command bellow will check and install it if revealjs isn't installed yet.

But, you can also manually install or even update it to a different version with the `installreveal` command:

```shell
$ revelation installreveal
```

### Creating a new Presentation

To create a new presentation you can use `mkpresentation` command that will setup a new presentation using the base layout for you:

```shell
$ revelation mkpresentation mypresentation
```

### Running the Presentation

You can start presenting with the `start` command on your presentation markdown file:

```shell
$ cd mypresentation
$ revelation start slides.md
```

### Static Export

To export the presentation as static HTML content use the command:

```shell
$ revelation mkstatic slides.md
```

### PDF Export

Presentations can be exported to PDF via a special print stylesheet. This feature will be described using [Google Chrome](https://google.com/chrome) or [Chromium](https://www.chromium.org/Home), but I got the same results using [Firefox](https://www.mozilla.org/en-US/firefox/new/).

1. Run the presentation with revelation.
2. Open your browser with the `print-pdf` as query string like : `localhost:5000/?print-pdf`.
3. Open the in-browser print dialog (CTRL+P or CMD+P).
4. Change the **Destination** setting to **Save as PDF**.
5. Change the **Layout** to **Landscape**.
6. Change the **Margins** to **None**.
7. Enable the **Background graphics** option.
8. Click **Save**.

Alternatively you can use the [decktape](https://github.com/astefanutti/decktape) project.

## Presentation Setup

The base presentation file structure looks like this:

```
presentation/
|- media/
|- theme/
|- config.py
|- slides.md
```

### The slides.md File

This is your presentation file written using markdown with some especial tags described on [markdown section](#markdown) and is placed on your presentation root folder.

Split your slides by setting up a *slide separator* and *vertical slide separator* into **REVEAL_CONFIG**. Default separator are `---` and `---~`.

### The media folder

By default, revelation looks for a folder called **media** inside your presentation root folder. All media placed inside it can be referenced on your presentation by the path `/media`:

```md
![Python Logo](media/python.png)
```

You can define a custom media path using the `--media` option on revelation `start` command.

### The theme folder

You can create your custom theme file and place it inside a **theme** folder and reference it at the configuration file by the option `--theme`.

### The config.py File

The configuration file located in the root folder of your presentation, allows you to customize your presentation. This file is optional and have the following configuration options:

- **REVEAL_META**: Metadata of your presentation, mostly to identify the author and title.
- **REVEAL_THEME**: A string where you can select the theme you would like to use. All revealjs base themes are available.
- **REVEAL_CONFIG**: A python dictionary with the [revealjs configuration attributes](https://revealjs.com/config/) but using python types (e.g.: true is python boolean True)

Once you create a new presentation, all configuration values will be there for you to customize.

## Markdown

The markdown used on the presentation files support everything that [revealjs docs](https://revealjs.com/markdown/) allows to place inside the `data-template` section.
