# -*- coding: utf-8 -*-

REVEAL_META = {
    # Title of the slide
    'title': 'revelation',

    # Author in the metadata of the slide
    'author': 'Humberto Rocha',

    # Description in the metadata of the slide
    'description': 'A revelation example presentation',
}

# Reveal markdown slide separator
REVEAL_SLIDE_SEPARATOR = '---'

# Themes
# beige, black, blood, league, moon, night, serif, simple, sky,
# solarized, white
REVEAL_THEME = 'sky'

REVEAL_CONFIG = {
    # Display controls in the bottom right corner
    'controls': False,

    # Display a presentation progress bar
    'progress': True,

    # Display the page number of the current slide
    'slideNumber': True,

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
    'backgroundTransition': 'convex',

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
