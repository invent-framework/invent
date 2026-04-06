from invent.i18n import _
from pyscript.web import input_,label,div
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,Event,TextProperty
class ColorPicker(Widget):
	value=TextProperty(_('The value of the color picker. Must be in seven-characterhexadecimal notation.'),default_value='#000000',min_length=7,max_length=7);label=TextProperty(_('An optional label shown next to the picker'),default_value='Select a color.');picked=Event(_('Sent when a color is picked.'),colour=_('The picked colour in hexadecimal notation.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M200.77 53.89A103.27 103.27 0 0 0 128 24h-1.07A104 104 0 0 0 24 128c0 43 26.58 79.06 69.36 94.17A32 32 0 0 0 136 192a16 16 0 0 1 16-16h46.21a31.81 31.81 0 0 0 31.2-24.88a104.4 104.4 0 0 0 2.59-24a103.28 103.28 0 0 0-31.23-73.23m13 93.71a15.89 15.89 0 0 1-15.56 12.4H152a32 32 0 0 0-32 32a16 16 0 0 1-21.31 15.07C62.49 194.3 40 164 40 128a88 88 0 0 1 87.09-88h.9a88.35 88.35 0 0 1 88 87.25a89 89 0 0 1-2.18 20.35ZM140 76a12 12 0 1 1-12-12a12 12 0 0 1 12 12m-44 24a12 12 0 1 1-12-12a12 12 0 0 1 12 12m0 56a12 12 0 1 1-12-12a12 12 0 0 1 12 12m88-56a12 12 0 1 1-12-12a12 12 0 0 1 12 12"/></svg>'
	def on_changed(A,event):A.value=A._input_element.value
	def on_id_changed(A):A._input_element.id=A.id;A._text_label.setAttribute('for',A.id)
	def on_name_changed(A):A._input_element.name=A.name
	def on_label_changed(A):A._text_label.innerText=A.label
	def on_value_changed(A):A._input_element.value=A.value;A.publish(A.picked,colour=A.value)
	def render(A):A._input_element=input_(type='color',id=A.id,name=A.name);A._text_label=label(A.label);setattr(A._text_label,'for',A.id);B=div(A._input_element,A._text_label);A._input_element.addEventListener('change',create_proxy(A.on_changed));return B