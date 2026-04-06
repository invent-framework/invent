_A='MEDIUM'
from invent.i18n import _
from invent.ui.core import Widget,TextProperty,ChoiceProperty,Event
from invent.ui.core.measures import PURPOSES
from pyscript.web import button
from pyscript.ffi import create_proxy
class Button(Widget):
	text=TextProperty(_('The text on the button.'),default_value='Click Me');size=ChoiceProperty(_('The size of the button.'),default_value=_A,choices=['LARGE',_A,'SMALL'],group='style');purpose=ChoiceProperty(_("The button's purpose."),default_value='DEFAULT',choices=PURPOSES,group='style');press=Event(_('Sent when the button is pressed.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176z"/></svg>'
	def click(A,event):A.publish(A.press)
	def on_text_changed(A):A.element.innerText=A.text
	def on_size_changed(A):
		C='small';B='large';A.element.classList.remove(B);A.element.classList.remove(C)
		if A.size=='LARGE':A.element.classList.add(B)
		elif A.size=='SMALL':A.element.classList.add(C)
	def on_purpose_changed(A):
		F='danger';E='warning';D='success';C='secondary';B='primary';A.element.classList.remove(B);A.element.classList.remove(C);A.element.classList.remove(D);A.element.classList.remove(E);A.element.classList.remove(F)
		if A.purpose=='PRIMARY':A.element.classList.add(B)
		elif A.purpose=='SECONDARY':A.element.classList.add(C)
		elif A.purpose=='SUCCESS':A.element.classList.add(D)
		elif A.purpose=='WARNING':A.element.classList.add(E)
		elif A.purpose=='DANGER':A.element.classList.add(F)
	def render(A):B=button(A.text,id=A.id);B.addEventListener('click',create_proxy(A.click));return B