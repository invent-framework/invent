from invent.i18n import _
from pyscript.web import input_,label,div
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,TextProperty,TimeProperty
class TimePicker(Widget):
	time=TimeProperty(_('The time to display in the picker.'),default_value=None);label=TextProperty(_('An optional label shown next to the picker'),default_value='Select a time.')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88m64-88a8 8 0 0 1-8 8h-56a8 8 0 0 1-8-8V72a8 8 0 0 1 16 0v48h48a8 8 0 0 1 8 8"/></svg>'
	def on_changed(A,event):A.time=A._input_element.value
	def on_id_changed(A):A._input_element.id=A.id;A._text_label.setAttribute('for',A.id)
	def on_name_changed(A):A._input_element.name=A.name
	def on_label_changed(A):A._text_label.innerText=A.label
	def on_time_changed(A):A._input_element.value=f"{A.time}"
	def render(A):A._input_element=input_(type='time',id=A.id,name=A.name);A._text_label=label(A.label);setattr(A._text_label,'for',A.id);B=div(A._input_element,A._text_label);A._input_element.addEventListener('change',create_proxy(A.on_changed));return B