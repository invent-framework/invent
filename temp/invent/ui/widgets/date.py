from invent.i18n import _
from pyscript.web import input_,label,div
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,DateProperty,TextProperty
class DatePicker(Widget):
	date=DateProperty(_('The date to display in the picker.'),default_value=None);label=TextProperty(_('An optional label shown next to the picker'),default_value='Select a date.')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 32h-24v-8a8 8 0 0 0-16 0v8H88v-8a8 8 0 0 0-16 0v8H48a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16M72 48v8a8 8 0 0 0 16 0v-8h80v8a8 8 0 0 0 16 0v-8h24v32H48V48Zm136 160H48V96h160zm-68-76a12 12 0 1 1-12-12a12 12 0 0 1 12 12m44 0a12 12 0 1 1-12-12a12 12 0 0 1 12 12m-88 40a12 12 0 1 1-12-12a12 12 0 0 1 12 12m44 0a12 12 0 1 1-12-12a12 12 0 0 1 12 12m44 0a12 12 0 1 1-12-12a12 12 0 0 1 12 12"/></svg>'
	def on_changed(A,event):A.date=A._input_element.value
	def on_id_changed(A):A._input_element.id=A.id;A._text_label.setAttribute('for',A.id)
	def on_name_changed(A):A._input_element.name=A.name
	def on_label_changed(A):A._text_label.innerText=A.label
	def on_date_changed(A):A._input_element.value=f"{A.date}"
	def render(A):A._input_element=input_(type='date',id=A.id,name=A.name);A._text_label=label(A.label);setattr(A._text_label,'for',A.id);B=div(A._input_element,A._text_label);A._input_element.addEventListener('change',create_proxy(A.on_changed));return B