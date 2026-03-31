from invent.i18n import _
from pyscript.web import select
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,TextProperty,ListProperty,Event
class Selector(Widget):
	value=TextProperty(_('The selected option.'),default_value='');choices=ListProperty(_('The options from which to select.'));changed=Event(_('The selected option has changed.'),selected=_('The new selected option.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M112 40a8 8 0 0 0-8 8v16H24A16 16 0 0 0 8 80v96a16 16 0 0 0 16 16h80v16a8 8 0 0 0 16 0V48a8 8 0 0 0-8-8M24 176V80h80v96Zm224-96v96a16 16 0 0 1-16 16h-88a8 8 0 0 1 0-16h88V80h-88a8 8 0 0 1 0-16h88a16 16 0 0 1 16 16M88 112a8 8 0 0 1-8 8h-8v24a8 8 0 0 1-16 0v-24h-8a8 8 0 0 1 0-16h32a8 8 0 0 1 8 8"/></svg>'
	def on_choices_changed(A):
		A.element.options.clear()
		for B in A.choices:C=bool(B==A.value);A.element.options.add(value=B,text=B,selected=C)
	def on_change(A,event):A.value=A.element.options.selected.value;A.publish('changed',selected=A.value)
	def render(A):B=select(id=A.id);B.addEventListener('change',create_proxy(A.on_change));return B