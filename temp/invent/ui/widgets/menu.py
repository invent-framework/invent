_D='invent-menu-wrapper--open'
_C='MEDIUM'
_B='style'
_A=None
from invent.i18n import _
from pyscript.ffi import create_proxy
from pyscript.web import div,li,ul
from invent.ui.core import Widget,TextProperty,ListProperty,ChoiceProperty,Event
from invent.ui.widgets.button import Button
from invent.ui.core.measures import PURPOSES
class Menu(Widget):
	choices=ListProperty(_('The options from which to select.'));hover=ChoiceProperty(_('Defines where the menu appears in relation to the button.'),default_value='BELOW',choices=['ABOVE','BELOW','BEFORE','AFTER'],group=_B);text=TextProperty(_('The text on the button.'),default_value='≡');size=ChoiceProperty(_('The size of the button.'),default_value=_C,choices=['LARGE',_C,'SMALL'],group=_B);purpose=ChoiceProperty(_("The button's purpose."),default_value='DEFAULT',choices=PURPOSES,group=_B);opened=Event(_('Sent when the button is pressed.'),button=_('The button that was clicked.'));selected=Event(_('The menu option has been selected.'),selected=_('The new selected option.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,128ZM40,72H216a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16ZM216,184H40a8,8,0,0,0,0,16H216a8,8,0,0,0,0-16Z"></path></svg>'
	def on_choices_changed(A):...
	def on_text_changed(A):A.trigger_button.text=A.text
	def on_size_changed(A):A.trigger_button.size=A.size
	def on_purpose_changed(A):A.trigger_button.purpose=A.purpose
	def on_hover_changed(A):
		for B in('above','below','before','after'):A._wrapper.classList.remove(f"invent-menu-wrapper--{B}")
		A._wrapper.classList.add(f"invent-menu-wrapper--{A.hover.lower()}")
	def _close_menu(A):
		if A._menu_list is not _A:A._menu_list.remove();A._menu_list=_A
		A._wrapper.classList.remove(_D)
	def open_menu(A,event):
		if A._menu_list is not _A:A._close_menu();return
		A.publish(A.opened,button=A.trigger_button.element)
		def E(option):
			def B(e):e.stopPropagation();A._close_menu();A.publish(A.selected,selected=option)
			return create_proxy(B)
		B=ul();B.classList.add('invent-menu')
		for D in A.choices or[]:C=li(D);C.classList.add('invent-menu-item');C.addEventListener('click',E(D));B.append(C)
		A._menu_list=B;A._wrapper.classList.add(_D);A._wrapper.append(B)
	def render(A):A.trigger_button=Button();A.trigger_button.render();B=A.trigger_button.element;B.addEventListener('click',create_proxy(A.open_menu));A._menu_list=_A;A._wrapper=div();A._wrapper.classList.add('invent-menu-wrapper');A._wrapper.classList.add(f"invent-menu-wrapper--{A.hover.lower()}");A._wrapper.append(B);return A._wrapper