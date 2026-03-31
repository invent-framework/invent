from invent.i18n import _
from pyscript.web import input_,label,span,div
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,BooleanProperty,TextProperty
class Switch(Widget):
	value=BooleanProperty(_('The value of the switch.'),default_value=False);label=TextProperty(_('An optional label shown next to the switch'),default_value='')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M176 56H80a72 72 0 0 0 0 144h96a72 72 0 0 0 0-144m0 128H80a56 56 0 0 1 0-112h96a56 56 0 0 1 0 112M80 88a40 40 0 1 0 40 40a40 40 0 0 0-40-40m0 64a24 24 0 1 1 24-24a24 24 0 0 1-24 24"/></svg>'
	def on_changed(A,event):A.value=not A.value
	def on_id_changed(A):A._checkbox_element.id=A.id;A._label_text_element.setAttribute('for',A.id)
	def on_name_changed(A):A._checkbox_element.name=A.name
	def on_label_changed(A):A._label_text_element.innerText=A.label
	def on_value_changed(A):
		B='checked'
		if A.value:A._checkbox_element.setAttribute(B,True)
		else:A._checkbox_element.removeAttribute(B)
	def render(A):A._checkbox_element=input_(type='checkbox',id=A.id,name=A.name);A._span_element=span(' ');A._span_element.classes.add('slider');A._label_text_element=label(text=A.label);A._label_text_element.classes.add('switch-label');setattr(A._label_text_element,'for',A.id);B=label(A._checkbox_element,A._span_element);B.classes.add('switch');C=div(B,A._label_text_element);A._checkbox_element.addEventListener('change',create_proxy(A.on_changed));return C