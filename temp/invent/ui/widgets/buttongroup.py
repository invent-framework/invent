_A='MEDIUM'
from collections import OrderedDict
from invent.i18n import _
from pyscript.ffi import create_proxy
from pyscript.web import div,input_,label
from invent.ui.core import Widget,TextProperty,ListProperty,ChoiceProperty,Event
from invent.ui.core.measures import PURPOSES
class ButtonGroup(Widget):
	choices=ListProperty(_('The options from which to select.'));value=TextProperty(_('The currently selected option.'),default_value=None);group=TextProperty(_('The group to which the button-group belongs.'),default_value='');size=ChoiceProperty(_('The size of the buttons.'),default_value=_A,choices=['LARGE',_A,'SMALL'],group='style');purpose=ChoiceProperty(_("The buttons' purpose."),default_value='DEFAULT',choices=PURPOSES,group='style');changed=Event(_('Sent when the selected option changes.'),value=_('The new value of the button group.'));_items=OrderedDict()
	def _build_pair(A,index,choice):
		B=choice;D=f"{A.group}-{index}";C=input_(type='radio',name=A.group,id=D,value=B,classes=['invent-btn-check'])
		if B==A.value:C.checked=True
		C.addEventListener('change',create_proxy(A._on_radio_change));E=label(B,for_=D,classes=['invent-btn']);return C,E
	def on_choices_changed(A):
		A.element.replaceChildren();A._items=OrderedDict()
		for(E,B)in enumerate(A.choices):C,D=A._build_pair(E,B);A.element.append(C);A.element.append(D);A._items[B]=C,D
	def on_group_changed(A):
		for(D,(B,E))in enumerate(A._items.values()):C=f"{A.group}-{D}";B.name=A.group;B.id=C;E.for_=C
	def on_value_changed(A):
		for(B,(C,D))in A._items.items():C.checked=B==A.value
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
	def _on_radio_change(A,event):B=event.target.value;A.value=B;A.publish(A.changed,value=B)
	def render(B):A=div(classes=['invent-btn-group'],role='group');return A