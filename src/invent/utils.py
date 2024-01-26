"""
Utility functions.
"""
from pyscript import window

def play_sound(url):
    sound = window.Audio.new(url)
    sound.play()
