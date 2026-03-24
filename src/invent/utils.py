"""
Utility and compatibility functions.
"""

import inspect
import sys
from pyscript.web import div
from .app import App
from .i18n import _

#: A flag to show if MicroPython is the current Python interpreter.
is_micropython = "micropython" in sys.version.lower()


#: Weekday lookups; datetime.weekday() returns 0=Mon.
WEEKDAYS = (
    _("Mon"),
    _("Tue"),
    _("Wed"),
    _("Thu"),
    _("Fri"),
    _("Sat"),
    _("Sun"),
)


#: Month lookups; datetime.month returns 1=Jan.
MONTHS = (
    _("Jan"),
    _("Feb"),
    _("Mar"),
    _("Apr"),
    _("May"),
    _("Jun"),
    _("Jul"),
    _("Aug"),
    _("Sep"),
    _("Oct"),
    _("Nov"),
    _("Dec"),
)


def show_page(page_id):
    """
    Show the page with the specified `page_id`. Hide the current page if
    there is one.
    """
    App.app().show_page(page_id)


def getmembers_static(cls):
    """
    Cross-interpreter implementation of `inspect.getmembers_static`.
    """
    if is_micropython:  # pragma: no cover
        return [
            (name, getattr(cls, name)) for name, _ in inspect.getmembers(cls)
        ]
    return inspect.getmembers_static(cls)


def iscoroutinefunction(obj):
    """
    Cross-interpreter implementation of `inspect.iscoroutinefunction`.
    """
    if is_micropython:
        # MicroPython doesn't appear to have a way to determine if a closure is
        # an async function except via the repr. This is a bit hacky.
        r = repr(obj)
        if "<closure <generator>" in r:
            return True
        # Same applies to bound methods.
        if "<bound_method" in r and "<generator>" in r:
            return True
        return inspect.isgeneratorfunction(obj)

    return inspect.iscoroutinefunction(obj)


def capitalize(s):
    """
    Cross-interpreter implementation of `str.capitalize`.
    """
    return s[0].upper() + s[1:].lower()


def sanitize(raw):
    """
    Returns an HTML safe version of the `raw` input string.
    """
    temp = div()
    temp.innerText = raw
    return temp.innerHTML


def from_markdown(raw_markdown):
    """
    Convert `raw_markdown` to sanitized HTML.
    """
    result = raw_markdown
    from . import marked, purify  # To avoid circular imports.

    if marked:
        result = purify.default().sanitize(marked.parse(raw_markdown))
    return result


def _hex_to_rgb(hex_colour):
    """
    Parse a CSS `hex_colour` string to an `(r, g, b)` tuple.

    Accepts a `#rrggbb` string and returns each channel as an integer in the
    range 0-255.

    Created with the help of an LLM.
    """
    h = hex_colour.lstrip("#")
    return (
        int(h[0:2], 16),  # Red
        int(h[2:4], 16),  # Green
        int(h[4:6], 16),  # Blue
    )


def _linearise(channel):
    """
    Convert a single sRGB `channel` to linear light.

    Put simply, how bright is this channel, as a fraction of its maximum
    brightness?

    Accepts a 0-255 integer and returns a 0-1 float. Applies the sRGB piecewise
    transfer function defined in the WCAG 2.1 contrast specification:

    https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    Created with the help of an LLM.
    """
    c = channel / 255
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _luminance(r, g, b):
    """
    Calculate the WCAG relative luminance of an RGB colour.

    Put simply, how bright is this colour overall, as a fraction of absolute
    white?

    Accepts `r`, `g`, `b` as 0-255 integers and returns a 0-1 float where 0 is
    absolute black and 1 is absolute white. Uses the standard WCAG 2.1
    luminance coefficients (0.2126, 0.7152, 0.0722) which reflect human eye
    sensitivity across the visible spectrum:

    https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    Created with the help of an LLM.
    """
    return (
        0.2126 * _linearise(r)
        + 0.7152 * _linearise(g)
        + 0.0722 * _linearise(b)
    )


def _rgb_to_hsl(r, g, b):
    """
    Convert an RGB colour to HSL (hue, saturation, lightness).

    Accepts `r`, `g`, `b` as 0-255 integers and returns a tuple of
    `(hue, saturation, lightness)` where `hue` is 0-360 degrees and
    `saturation` and `lightness` are 0-1 floats. Uses the standard
    geometric derivation from the RGB colour cube:

    https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB

    Created with the help of an LLM.
    """
    r, g, b = r / 255, g / 255, b / 255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2
    if max_c == min_c:
        return 0, 0, l
    d = max_c - min_c
    s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
    if max_c == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif max_c == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60, s, l


def _hue_to_rgb(p, q, t):
    """
    Map a hue fraction to a single RGB channel value.

    A helper for `_hsl_to_hex` implementing the standard HSL-to-RGB
    piecewise interpolation across the six hue sectors:

    https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB

    Created with the help of an LLM.
    """
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1 / 6:
        return p + (q - p) * 6 * t
    if t < 1 / 2:
        return q
    if t < 2 / 3:
        return p + (q - p) * (2 / 3 - t) * 6
    return p


def _hsl_to_hex(h, s, l):
    """
    Convert an HSL (hue, saturation, lightness) colour to a CSS hex string.

    Accepts `hue` as 0-360 degrees and `saturation` and `lightness` as 0-1 floats.
    Returns a lowercase `#rrggbb` string. Achromatic colours (`s == 0`) bypass
    the hue calculation entirely. See:

    https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB

    Created with the help of an LLM.
    """
    if s == 0:
        v = int(l * 255)
        return f"#{v:02x}{v:02x}{v:02x}"
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    h_norm = h / 360
    r = _hue_to_rgb(p, q, h_norm + 1 / 3)
    g = _hue_to_rgb(p, q, h_norm)
    b = _hue_to_rgb(p, q, h_norm - 1 / 3)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def contrast_colours(hex_bg):
    """
    Return contrasting text and link colours for a given `hex_bg`
    background.

    Accepts a `#rrggbb` hex string and returns a dict with 'text' and
    'link' keys, each a hex colour string chosen to remain legible
    over the supplied background.

    Created with the help of an LLM.

    Text colour is selected as near-white or near-black based on the
    WCAG relative luminance threshold of 0.179 (the midpoint of the
    WCAG AA contrast ratio scale):

    https://www.w3.org/TR/WCAG21/#contrast-minimum

    The link colour is derived from the background hue at a safe
    lightness, preserving recognisable colour identity whilst
    ensuring sufficient contrast. Near-achromatic backgrounds
    (saturation below 0.1) fall back to a neutral blue (210 degrees)
    since their hue is not perceptually meaningful.
    """
    r, g, b = _hex_to_rgb(hex_bg)
    lum = _luminance(r, g, b)
    dark_bg = lum <= 0.179
    h, s, _ = _rgb_to_hsl(r, g, b)
    if s < 0.1:
        h = 210
    # Ensure enough saturation for the link hue to be perceptible.
    link_s = max(s, 0.55)
    if dark_bg:
        return {
            "text": "#f0f0f0",
            "link": _hsl_to_hex(h, link_s, 0.85),
        }
    return {
        "text": "#1a1a1a",
        "link": _hsl_to_hex(h, link_s, 0.25),
    }


def humanise_timestamp(dt):
    """
    Format a datetime `dt` as a human-readable string. For example,
    "Thu 01 Jan 2026, 14:32".
    """
    day_name = WEEKDAYS[dt.weekday()]
    month_name = MONTHS[dt.month - 1]
    period = "AM" if dt.hour < 12 else "PM"
    hour = dt.hour % 12 or 12
    return (
        f"{day_name} {dt.day:02d} {month_name}"
        f" {dt.year}, {hour}:{dt.minute:02d} {period}"
    )
