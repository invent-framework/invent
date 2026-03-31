_A='keypress'
from invent.i18n import _
from pyscript.web import input_,textarea
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,TextProperty,IntegerProperty,BooleanProperty,ChoiceProperty,Event
class TextInput(Widget):
	value=TextProperty(_('The text in the text box.'));required=BooleanProperty(_('A flag to indicate entry into the text box is required.'),default_value=False,map_to_attribute='required');placeholder=TextProperty(_('The placeholder text to put into the empty text box.'),map_to_attribute='placeholder');minlength=IntegerProperty(_('The minimum character length for the input.'),map_to_attribute='minlength');maxlength=IntegerProperty(_('The maximum character length for the input.'),map_to_attribute='maxlength');input_type=ChoiceProperty(_('The type of text input.'),default_value='text',choices=['text','email','number','password','tel','url'],map_to_attribute='type');keypress=Event(_('Triggered when a key is pressed to enter text.'),key=_('The key that was pressed.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M112 40a8 8 0 0 0-8 8v16H24A16 16 0 0 0 8 80v96a16 16 0 0 0 16 16h80v16a8 8 0 0 0 16 0V48a8 8 0 0 0-8-8M24 176V80h80v96Zm224-96v96a16 16 0 0 1-16 16h-88a8 8 0 0 1 0-16h88V80h-88a8 8 0 0 1 0-16h88a16 16 0 0 1 16 16M88 112a8 8 0 0 1-8 8h-8v24a8 8 0 0 1-16 0v-24h-8a8 8 0 0 1 0-16h32a8 8 0 0 1 8 8"/></svg>'
	def __init__(A,**B):
		A._number_of_lines=B.pop('number_of_lines',1)
		if A._number_of_lines<1:raise ValueError(_('number_of_lines must be at least 1'))
		super().__init__(**B)
	def on_value_changed(A):
		if A._number_of_lines==1:A.element.value=A.value
		else:A.element.innerHTML=A.value
	def on_input(A,event):A.value=event.target.value
	def on_keypress(A,event):A.publish(_A,key=event.key)
	def render(A):
		if A._number_of_lines==1:B=input_(type=A.input_type,id=A.id)
		else:B=textarea(id=A.id,rows=str(A._number_of_lines))
		B.addEventListener('input',create_proxy(A.on_input));B.addEventListener(_A,create_proxy(A.on_keypress));return B