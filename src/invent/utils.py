"""
Utility functions.
"""
from invent import App
from pyscript import window

def play_sound(url):
    sound = window.Audio.new(url)
    sound.play()


def goto(page_name):
    App.app().goto(page_name)
