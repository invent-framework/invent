"""
Utility functions.
"""

from invent import App
from pyscript import window


def play_sound(url):
    sound = window.Audio.new(str(url))
    sound.play()


def show_page(page_name):
    App.app().show_page(page_name)
