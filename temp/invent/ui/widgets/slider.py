from invent.i18n import _
from pyscript.web import input_
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,NumericProperty
class Slider(Widget):
	value=NumericProperty(_('The value of the slider.'),default_value=50,map_to_attribute='value');minvalue=NumericProperty(_('The minimum value of the slider.'),default_value=0,map_to_attribute='min');maxvalue=NumericProperty(_('The maximum value of the slider.'),default_value=100,map_to_attribute='max');step=NumericProperty(_('The granularity of the value of the slider.'),default_value=1,map_to_attribute='step')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M40 88h33a32 32 0 0 0 62 0h81a8 8 0 0 0 0-16h-81a32 32 0 0 0-62 0H40a8 8 0 0 0 0 16m64-24a16 16 0 1 1-16 16a16 16 0 0 1 16-16m112 104h-17a32 32 0 0 0-62 0H40a8 8 0 0 0 0 16h97a32 32 0 0 0 62 0h17a8 8 0 0 0 0-16m-48 24a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'
	def on_input(A,event):A.value=int(event.target.value)
	def on_value_changed(A):A.element.value=A.value
	def render(A):B=input_(type='range',id=A.id);B.addEventListener('input',create_proxy(A.on_input));return B