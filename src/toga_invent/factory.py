from .app import App
from .widgets.box import Box
from .widgets.button import Button
from .widgets.label import Label
from .widgets.textinput import TextInput
from .window import Window


# Stub out some unused classes.
class Icon:
    EXTENSIONS = [".png"]
    SIZES = None

    def __init__(self, *args, **kwargs):
        pass


class Paths:
    def __init__(self, *args, **kwargs):
        pass
