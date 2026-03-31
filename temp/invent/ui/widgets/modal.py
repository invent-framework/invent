_B='MEDIUM'
_A='click'
from invent.i18n import _
from invent.ui.core import Widget,TextProperty,ChoiceProperty,Event
from invent.ui.widgets.button import Button
from invent.ui.containers import Column
from invent.ui.core.measures import PURPOSES
from pyscript.web import button,div,page
from pyscript.ffi import create_proxy
class Modal(Widget):
	text=TextProperty(_('The text on the button.'),default_value='Click Me');size=ChoiceProperty(_('The size of the button.'),default_value=_B,choices=['LARGE',_B,'SMALL'],group='style');purpose=ChoiceProperty(_("The button's purpose."),default_value='DEFAULT',choices=PURPOSES,group='style');open=Event(_('Sent when the button is pressed.'),button=_('The button that was clicked.'),modal=_('The modal that was opened.'));close=Event(_('Sent when the modal is dismissed.'),modal=_('The modal that was closed.'))
	def on_text_changed(A):A.trigger_button.text=A.text
	def on_size_changed(A):A.trigger_button.size=A.size
	def on_purpose_changed(A):A.trigger_button.purpose=A.purpose
	def __init__(A,**B):C=B.pop('children',[]);super().__init__(**B);A.modal.children=C;A.trigger_button.parent=A;A.modal.parent=A
	def close_modal(A,event=None):
		if hasattr(A,'backdrop'):A.backdrop.remove();A.publish('close',modal=A)
	def open_modal(A,event):A.publish('open',button=A.trigger_button,modal=A);C=button('×');C.classList.add('dismiss');C.setAttribute('aria-label',_('Close'));C.addEventListener(_A,create_proxy(lambda e:A.close_modal()));B=div();B.classList.add('invent-modal');B.setAttribute('role','dialog');B.setAttribute('aria-modal','true');B.append(C);B.append(A.modal.element);B.addEventListener(_A,create_proxy(lambda e:e.stopPropagation()));A.backdrop=div();A.backdrop.classList.add('invent-modal-backdrop');A.backdrop.append(B);A.backdrop.addEventListener(_A,create_proxy(lambda e:A.close_modal()));page.body.append(A.backdrop)
	def render(A):A.trigger_button=Button();A.modal=Column();A.modal.render();A.trigger_button.render();B=A.trigger_button.element;B.addEventListener(_A,create_proxy(A.open_modal));return B