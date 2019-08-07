import os
import sys

if sys.platform == "win32":  # pragma: no cover
    # Needed so Kivy behaves properly on Windows.
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
    from kivy import Config

    Config.set("graphics", "multisamples", "0")
from .core import Card, CardApp, Inputs, palette

__all__ = ["Card", "CardApp", "Inputs", "palette"]

# IMPORTANT
# ---------
# Keep these metadata assignments simple and single-line. They are parsed
# somewhat naively by setup.py and the Windows installer generation script.

__title__ = "pypercard"
__description__ = "A HyperCard inspired GUI framework for beginner developers."
__version__ = "0.0.1-alpha.2"
__license__ = "MIT"
__url__ = "https://github.com/ntoll/pypercard"
__author__ = "Nicholas H.Tollervey"
__email__ = "ntoll@ntoll.org"
