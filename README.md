# Revelation

[![PyPI](https://img.shields.io/pypi/v/revelation.svg)](https://pypi.org/project/revelation/)
[![PyPI - License](https://img.shields.io/pypi/l/revelation.svg)](https://pypi.org/project/revelation/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/revelation.svg)](https://pypi.org/project/revelation/)
[![Actions Status](https://github.com/humrochagf/revelation/workflows/CI/badge.svg)](https://github.com/humrochagf/revelation/actions)
[![Coverage Status](https://coveralls.io/repos/github/humrochagf/revelation/badge.svg?branch=main)](https://coveralls.io/github/humrochagf/revelation?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[revelation](https://github.com/humrochagf/revelation) is a cli tool that makes your [reveal.js](https://github.com/hakimel/reveal.js) presentations nice and easy using markdown and serving it locally.

## Features

- Local presentation server to run your presentations even with no connection.
- Boilerplate presentation creation with one command.
- Custom css theming support.
- Export to static html tool.
- Browser live reload of the presentation at markdown change.

## Installation

You can install it from the PyPI:

```shell
$ pip install revelation
```

## Usage

### Install/Update reveal.js files

Revelation depends on reveal.js to run its presentation and every command bellow will check and install it if reveal.js isn't installed yet.

You can also manually install reveal.js or even update it to a different version with the `installreveal` command:

```shell
$ revelation installreveal
```

### Creating a new Presentation

To start making your presentation revelation has the `mkpresentation` command that will setup a new presentation using the base layout for you:

```shell
$ revelation mkpresentation mypresentation
```

### Running the Presentation

Once you have your presentation ready you can start presenting by running the `start` command on your presentation markdown file:

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

### Share your presentation using [Ngrok](https://ngrok.com/)

You can easily share your presentation using [Ngrok](https://ngrok.com/). Download it, and put the binary file at root. Then you can do :
```shell
$ ngrok http 5000
```
This assume `5000` is your localhost.
`ngrok` will create a secure tunnel to your localhost :

```shell
ngrok by @inconshreveable                                              (Ctrl+C to quit)

Tunnel Status                 online
Version                       2.0.19/2.1.1
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://323744c6.ngrok.io -> localhost:5000
Forwarding                    https://323744c6.ngrok.io -> localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

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

The configuration file are placed on the presentation root folder and is responsible to customize your presentation.

This file is optional and can the values above can be changed:

**REVEAL_META**: python dictionary with metadata from the presentation

```python
REVEAL_META = {
    # Title of the slide
    'title': 'The title',

    # Author in the metadata of the slide
    'author': 'Some Author',

    # Description in the metadata of the slide
    'description': 'Some description'
}
```

**REVEAL_THEME**: string with reveal theme of choice

```python
# Themes
# beige, black, blood, league, moon, night, serif, simple, sky,
# solarized, white
REVEAL_THEME = 'black'
```

**REVEAL_CONFIG**: python dictionary with the [reveal.js configuration attributes](https://github.com/hakimel/reveal.js/#configuration) but using python types (e.g.: true is python boolean True)

```python
REVEAL_CONFIG = {
    # Slide separator
    'slideSep': '---',

    # Display controls in the bottom right corner
    'controls': True,

    # Display a presentation progress bar
    'progress': True,

    # Display the page number of the current slide
    'slideNumber': False,

    # Push each slide change to the browser history
    'history': True,

    # Enable keyboard shortcuts for navigation
    'keyboard': True,

    # Enable the slide overview mode
    'overview': True,

    # Vertical centering of slides
    'center': True,

    # Enables touch navigation on devices with touch input
    'touch': True,

    # Loop the presentation
    'loop': False,

    # Change the presentation direction to be RTL
    'rtl': False,

    # Turns fragments on and off globally
    'fragments': True,

    # Flags if the presentation is running in an embedded mode,
    # i.e. contained within a limited portion of the screen
    'embedded': False,

    # Flags if we should show a help overlay when the questionmark
    # key is pressed
    'help': True,

    # Flags if speaker notes should be visible to all viewers
    'showNotes': False,

    # Number of milliseconds between automatically proceeding to the
    # next slide, disabled when set to 0, this value can be overwritten
    # by using a data-autoslide attribute on your slides
    'autoSlide': 0,

    # Stop auto-sliding after user input
    'autoSlideStoppable': True,

    # Enable slide navigation via mouse wheel
    'mouseWheel': False,

    # Hides the address bar on mobile devices
    'hideAddressBar': True,

    # Opens links in an iframe preview overlay
    'previewLinks': False,

    # Transition style
    # default/cube/page/concave/zoom/linear/fade/none
    'transition': 'default',

    # Transition speed
    'transitionSpeed': 'default',  # default/fast/slow

    # Transition style for full page slide backgrounds
    # default/none/slide/concave/convex/zoom
    'backgroundTransition': 'default',

    # Number of slides away from the current that are visible
    'viewDistance': 3,

    # Parallax background image
    # e.g.:
    # "'https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg'"
    'parallaxBackgroundImage': '',

    # Parallax background size
    'parallaxBackgroundSize': '',  # CSS syntax, e.g. "2100px 900px"

    # Amount to move parallax background (horizontal and vertical)
    # on slide change
    # Number, e.g. 100
    'parallaxBackgroundHorizontal': '',
    'parallaxBackgroundVertical': '',
}
```

## Markdown

The markdown used on the presentation files support most of the [GitHub Markdown](https://help.github.com/articles/markdown-basics) and adds some especial html comment tags to edit styles and control effects that are explained on the [reveal.js markdown docs](https://github.com/hakimel/reveal.js/#markdown).

**Important:** You can use all html tags on the presentation files, but some block tags can present unexpected behavior.
