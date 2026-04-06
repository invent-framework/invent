from invent.i18n import _
from pyscript.web import input_,label,span
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,BooleanProperty,TextProperty
class Radio(Widget):
	selected=BooleanProperty(_('A flag to indicate if the radio button is selected'),default_value=False);value=TextProperty(_('The meaningful value associated with the checkbox.'),default_value='');label=TextProperty(_('An optional label shown next to the radio button'),default_value='');group=TextProperty(_('The group to which the radio button belongs'),default_value='')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88m0-144a56 56 0 1 0 56 56a56.06 56.06 0 0 0-56-56m0 96a40 40 0 1 1 40-40a40 40 0 0 1-40 40"/></svg>'
	def on_changed(A,event):A.selected=not A.selected
	def on_id_changed(A):A._radio_element.id=A.id;A.element.setAttribute('for',A.id)
	def on_label_changed(A):A._text_span.innerText=A.label
	def on_selected_changed(A):
		B='checked'
		if A.selected:A._radio_element.setAttribute(B,True)
		else:A._radio_element.removeAttribute(B)
	def on_group_changed(A):A._radio_element.name=A.group
	def on_value_changed(A):A._radio_element.value=A.value
	def render(A):A._radio_element=input_(type='radio',id=A.id,name=A.group);A._text_span=span(A.label);B=label(A._radio_element,A._text_span);setattr(B,'for',A.id);A._radio_element.addEventListener('change',create_proxy(A.on_changed));return B