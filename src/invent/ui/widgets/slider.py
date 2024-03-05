"""
A minimal area of the UI containing textual content.
"""

from invent.ui.core import Widget, NumericProperty
from pyscript import document


class Slider(Widget):
    value = NumericProperty("The value of the slider.", default_value=50)
    minvalue = NumericProperty("The minimum value of the slider.", default_value=0)
    maxvalue = NumericProperty("The maximum value of the slider.", default_value=100)
    step = NumericProperty("The granularity of the value of the slider.", default_value=1)

    @classmethod
    def preview(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M40 88h33a32 32 0 0 0 62 0h81a8 8 0 0 0 0-16h-81a32 32 0 0 0-62 0H40a8 8 0 0 0 0 16m64-24a16 16 0 1 1-16 16a16 16 0 0 1 16-16m112 104h-17a32 32 0 0 0-62 0H40a8 8 0 0 0 0 16h97a32 32 0 0 0 62 0h17a8 8 0 0 0 0-16m-48 24a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'  # noqa

    def on_value_changed(self):
        self.update_attribute("value", self.value)

    def on_minvalue_changed(self):
        self.update_attribute("min", self.minvalue)

    def on_maxvalue_changed(self):
        self.update_attribute("max", self.maxvalue)

    def on_step_changed(self):
        self.update_attribute("step", self.step)

    def render(self):
        element = document.createElement("input")
        element.id = self.id
        element.setAttribute("type", "range")
        return element
