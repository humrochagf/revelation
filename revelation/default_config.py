"""
Revelation presentation settings

This is an automatic generated template for revelation presentations
with the default options.
"""

REVEAL_META = {
    # Title of the slide
    "title": "The title",
    # Author in the metadata of the slide
    "author": "Some Author",
    # Description in the metadata of the slide
    "description": "Some description",
}

# Reveal markdown slide separator
REVEAL_SLIDE_SEPARATOR = "---"
REVEAL_VERTICAL_SLIDE_SEPARATOR = "---~"

# Themes
# beige, black, blood, league, moon, night, serif, simple, sky,
# solarized, white
REVEAL_THEME = "black"

REVEAL_CONFIG = {
    # Display presentation control arrows
    "controls": True,

    # Help the user learn the controls by providing hints, for example by
    # bouncing the down arrow when they first encounter a vertical slide
    "controlsTutorial": True,

    # Determines where controls appear, "edges" or "bottom-right"
    "controlsLayout": 'bottom-right',

    # Visibility rule for backwards navigation arrows; "faded", "hidden"
    # or "visible"
    "controlsBackArrows": 'faded',

    # Display a presentation progress bar
    "progress": True,

    # Display the page number of the current slide
    # - True:    Show slide number
    # - False:   Hide slide number
    #
    # Can optionally be set as a string that specifies the number formatting:
    # - "h.v":   Horizontal . vertical slide number (default)
    # - "h/v":   Horizontal / vertical slide number
    # - "c":   Flattened slide number
    # - "c/t":   Flattened slide number / total slides
    #
    # Alternatively, you can provide a function that returns the slide
    # number for the current slide. The function should take in a slide
    # object and return an array with one string [slideNumber] or
    # three strings [n1,delimiter,n2]. See #formatSlideNumber().
    "slideNumber": False,

    # Can be used to limit the contexts in which the slide number appears
    # - "all":      Always show the slide number
    # - "print":    Only when printing to PDF
    # - "speaker":  Only in the speaker view
    "showSlideNumber": 'all',

    # Use 1 based indexing for # links to match slide number (default is zero
    # based)
    "hashOneBasedIndex": False,

    # Add the current slide number to the URL hash so that reloading the
    # page/copying the URL will return you to the same slide
    "hash": True,

    # Flags if we should monitor the hash and change slides accordingly
    "respondToHashChanges": True,

    # Push each slide change to the browser history
    "history": True,

    # Enable keyboard shortcuts for navigation
    "keyboard": True,

    # Optional function that blocks keyboard events when retuning false
    #
    # If you set this to 'focused', we will only capture keyboard events
    # for embedded decks when they are in focus
    "keyboardCondition": None,

    # Disables the default reveal.js slide layout (scaling and centering)
    # so that you can use custom CSS layout
    "disableLayout": False,

    # Enable the slide overview mode
    "overview": True,

    # Vertical centering of slides
    "center": True,

    # Enables touch navigation on devices with touch input
    "touch": True,

    # Loop the presentation
    "loop": False,

    # Change the presentation direction to be RTL
    "rtl": False,

    # Changes the behavior of our navigation directions.
    #
    # "default"
    # Left/right arrow keys step between horizontal slides, up/down
    # arrow keys step between vertical slides. Space key steps through
    # all slides (both horizontal and vertical).
    #
    # "linear"
    # Removes the up/down arrows. Left/right arrows step through all
    # slides (both horizontal and vertical).
    #
    # "grid"
    # When this is enabled, stepping left/right from a vertical stack
    # to an adjacent vertical stack will land you at the same vertical
    # index.
    #
    # Consider a deck with six slides ordered in two vertical stacks:
    # 1.1    2.1
    # 1.2    2.2
    # 1.3    2.3
    #
    # If you're on slide 1.3 and navigate right, you will normally move
    # from 1.3 -> 2.1. If "grid" is used, the same navigation takes you
    # from 1.3 -> 2.3.
    "navigationMode": 'default',

    # Randomizes the order of slides each time the presentation loads
    "shuffle": False,

    # Turns fragments on and off globally
    "fragments": True,

    # Flags whether to include the current fragment in the URL,
    # so that reloading brings you to the same fragment position
    "fragmentInURL": True,

    # Flags if the presentation is running in an embedded mode,
    # i.e. contained within a limited portion of the screen
    "embedded": False,

    # Flags if we should show a help overlay when the questionmark
    # key is pressed
    "help": True,

    # Flags if it should be possible to pause the presentation (blackout)
    "pause": True,

    # Flags if speaker notes should be visible to all viewers
    "showNotes": False,

    # Global override for autolaying embedded media (video/audio/iframe)
    # - None:   Media will only autoplay if data-autoplay is present
    # - True:   All media will autoplay, regardless of individual setting
    # - False:  No media will autoplay, regardless of individual setting
    "autoPlayMedia": None,

    # Global override for preloading lazy-loaded iframes
    # - None:   Iframes with data-src AND data-preload will be loaded
    #           when within the viewDistance, iframes with only data-src
    #           will be loaded when visible
    # - True:   All iframes with data-src will be loaded when within
    #           the viewDistance
    # - False:  All iframes with data-src will be loaded only when visible
    "preloadIframes": None,

    # Can be used to globally disable auto-animation
    "autoAnimate": True,

    # Optionally provide a custom element matcher that will be
    # used to dictate which elements we can animate between.
    "autoAnimateMatcher": None,

    # Default settings for our auto-animate transitions, can be
    # overridden per-slide or per-element via data arguments
    "autoAnimateEasing": 'ease',
    "autoAnimateDuration": 1.0,
    "autoAnimateUnmatched": True,

    # CSS properties that can be auto-animated. Position & scale
    # is matched separately so there's no need to include styles
    # like top/right/bottom/left, width/height or margin.
    "autoAnimateStyles": [
        'opacity',
        'color',
        'background-color',
        'padding',
        'font-size',
        'line-height',
        'letter-spacing',
        'border-width',
        'border-color',
        'border-radius',
        'outline',
        'outline-offset'
    ],

    # Controls automatic progression to the next slide
    # - 0:      Auto-sliding only happens if the data-autoslide HTML attribute
    #           is present on the current slide or fragment
    # - 1+:     All slides will progress automatically at the given interval
    # - False:  No auto-sliding, even if data-autoslide is present
    "autoSlide": 0,

    # Stop auto-sliding after user input
    "autoSlideStoppable": True,

    # Use this method for navigation when auto-sliding
    # (defaults to navigateNext)
    "autoSlideMethod": None,

    # Specify the average time in seconds that you think you will spend
    # presenting each slide. This is used to show a pacing timer in the
    # speaker view
    "defaultTiming": None,

    # Enable slide navigation via mouse wheel
    "mouseWheel": False,

    # Opens links in an iframe preview overlay
    # Add `data-preview-link` and `data-preview-link="false"` to customise
    # each link individually
    "previewLinks": False,

    # Exposes the reveal.js API through window.postMessage
    "postMessage": True,

    # Dispatches all reveal.js events to the parent window through postMessage
    "postMessageEvents": False,

    # Focuses body when page changes visibility to ensure keyboard
    # shortcuts work
    "focusBodyOnPageVisibilityChange": True,

    # Transition style
    "transition": 'slide',  # none/fade/slide/convex/concave/zoom

    # Transition speed
    "transitionSpeed": 'default',  # default/fast/slow

    # Transition style for full page slide backgrounds
    "backgroundTransition": 'fade',  # none/fade/slide/convex/concave/zoom

    # Prints each fragment on a separate slide
    "pdfSeparateFragments": True,

    # Offset used to reduce the height of content within exported PDF pages.
    # This exists to account for environment differences based on how you
    # print to PDF. CLI printing options, like phantomjs and wkpdf, can end
    # on precisely the total height of the document whereas in-browser
    # printing has to end one pixel before.
    "pdfPageHeightOffset": -1,

    # Number of slides away from the current that are visible
    "viewDistance": 3,

    # Number of slides away from the current that are visible on mobile
    # devices. It is advisable to set this to a lower number than
    # viewDistance in order to save resources.
    "mobileViewDistance": 2,

    # The display mode that will be used to show slides
    "display": 'block',

    # Hide cursor if inactive
    "hideInactiveCursor": True,

    # Time before the cursor is hidden (in ms)
    "hideCursorTime": 5000
}
