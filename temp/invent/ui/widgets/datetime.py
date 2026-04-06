from invent.i18n import _
from pyscript.web import input_,label,div
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,DateProperty,TextProperty,TimeProperty
class DateTimePicker(Widget):
	date=DateProperty(_('The date to display in the picker.'),default_value=None);time=TimeProperty(_('The time to display in the picker.'),default_value=None);label=TextProperty(_('An optional label shown next to the picker'),default_value='Select a date/time.')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 32h-24v-8a8 8 0 0 0-16 0v8H88v-8a8 8 0 0 0-16 0v8H48a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16M72 48v8a8 8 0 0 0 16 0v-8h80v8a8 8 0 0 0 16 0v-8h24v32H48V48Zm136 160H48V96h160zm-96-88v64a8 8 0 0 1-16 0v-51.06l-4.42 2.22a8 8 0 0 1-7.16-14.32l16-8A8 8 0 0 1 112 120m59.16 30.45L152 176h16a8 8 0 0 1 0 16h-32a8 8 0 0 1-6.4-12.8l28.78-38.37a8 8 0 1 0-13.31-8.83a8 8 0 1 1-13.85-8A24 24 0 0 1 176 136a23.76 23.76 0 0 1-4.84 14.45"/></svg>'
	def on_changed(A,event):
		try:B,C=A._input_element.value.split('T');A.date=B;A.time=C
		except Exception as D:raise ValueError(f"Invalid date/time: {D}")
	def on_id_changed(A):A._input_element.id=A.id;A._text_label.setAttribute('for',A.id)
	def on_name_changed(A):A._input_element.name=A.name
	def on_label_changed(A):A._text_label.innerText=A.label
	def on_date_changed(A):A._update_input_value()
	def on_time_changed(A):A._update_input_value()
	def _update_input_value(A):A._input_element.value=f"{A.date}T{A.time}"
	def render(A):A._input_element=input_(type='datetime-local',id=A.id,name=A.name);A._text_label=label(A.label);setattr(A._text_label,'for',A.id);B=div(A._input_element,A._text_label);A._input_element.addEventListener('change',create_proxy(A.on_changed));return B