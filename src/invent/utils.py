"""
Utility functions.
"""


import inspect
import sys
from pyscript import window
from invent.ui import App


def play_sound(url):
    sound = window.Audio.new(str(url))
    sound.play()


def show_page(page_name):
    App.app().show_page(page_name)

