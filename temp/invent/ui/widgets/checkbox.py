from invent.i18n import _
from pyscript.web import input_,label,span
from pyscript.ffi import create_proxy
from invent.ui.core import Event,Widget,BooleanProperty,TextProperty
class CheckBox(Widget):
	value=BooleanProperty(_('The value of the checkbox.'),default_value=False);label=TextProperty(_('An optional label shown next to the checkbox'),default_value='');checked=Event(_('Sent when the checkbox is checked.'));unchecked=Event(_('Sent when the checkbox is un-checked.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M173.66 98.34a8 8 0 0 1 0 11.32l-56 56a8 8 0 0 1-11.32 0l-24-24a8 8 0 0 1 11.32-11.32L112 148.69l50.34-50.35a8 8 0 0 1 11.32 0M224 48v160a16 16 0 0 1-16 16H48a16 16 0 0 1-16-16V48a16 16 0 0 1 16-16h160a16 16 0 0 1 16 16m-16 160V48H48v160z"/></svg>'
	def on_changed(A,event):A.value=not A.value
	def on_id_changed(A):A._checkbox_element.id=A.id;A.element.setAttribute('for',A.id)
	def on_name_changed(A):A._checkbox_element.name=A.name
	def on_label_changed(A):A._text_span.innerText=A.label
	def on_value_changed(A):
		B='checked'
		if A.value:A._checkbox_element.setAttribute(B,True);A.publish(A.checked)
		else:A._checkbox_element.removeAttribute(B);A.publish(A.unchecked)
	def render(A):C='checkbox';A._checkbox_element=input_(type=C,id=A.id,name=A.name);A._text_span=span(A.label);A._text_span.classes.add(C);B=label(A._checkbox_element,A._text_span);setattr(B,'for',A.id);A._checkbox_element.addEventListener('change',create_proxy(A.on_changed));return B