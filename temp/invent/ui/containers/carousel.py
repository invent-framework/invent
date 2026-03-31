_D='data-transition'
_C='leaving'
_B='fade'
_A='active'
from invent.i18n import _
from..core.component import Component
from invent.ui.core import ListProperty,ChoiceProperty,IntegerProperty
from pyscript import ffi
from pyscript.web import div,button
_CARET_RIGHT='<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>'
_CARET_LEFT='<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"></path></svg>'
class Carousel(Component):
	children=ListProperty(_('The child items to display in the carousel.'),default_value=None);current_index=IntegerProperty(_('The index of the currently displayed item in the carousel.'),default_value=0,minimum=0);transition=ChoiceProperty(_('The transition effect to use when moving between items.'),choices=[_B,'slide'],default_value=_B)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M192,48H64A16,16,0,0,0,48,64V192a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64A16,16,0,0,0,192,48Zm0,144H64V64H192V192ZM240,56V200a8,8,0,0,1-16,0V56a8,8,0,0,1,16,0ZM32,56V200a8,8,0,0,1-16,0V56a8,8,0,0,1,16,0Z"></path></svg>'
	def _on_prev(A,event):
		B=len(A.children)if A.children else 0
		if B:A.current_index=(A.current_index-1)%B
	def _on_next(A,event):
		B=len(A.children)if A.children else 0
		if B:A.current_index=(A.current_index+1)%B
	def _on_touch_start(A,event):A._touch_start_x=event.touches[0].clientX
	def _on_touch_end(A,event):
		B=event;C=B.changedTouches[0].clientX-A._touch_start_x
		if abs(C)>50:
			if C<0:A._on_next(B)
			else:A._on_prev(B)
	def _activate(B,index):
		for(C,A)in enumerate(B._item_slots):
			A.classes.remove(_A);A.classes.remove(_C)
			if C==index:A.classes.add(_A)
	def on_children_changed(A):
		A._track.replaceChildren();A._item_slots=[]
		if not A.children:return
		for C in A.children:C.parent=A;B=div(classes='invent-carousel-item');B.append(C.element);A._item_slots.append(B);A._track.append(B)
		A._prev_index=0;A._activate(0)
	def on_current_index_changed(A):
		if not A._item_slots:return
		D=len(A._item_slots);B=A.current_index;C=A._prev_index if A._prev_index<D else 0;G=B>C and not(C==0 and B==D-1)or C==D-1 and B==0;A.element.setAttribute('data-direction','forward'if G else'backward')
		for H in A._item_slots:H.classes.remove(_C)
		E=A._item_slots[C];F=A._item_slots[B]
		if E is not F:E.classes.remove(_A);E.classes.add(_C)
		F.classes.add(_A);A._prev_index=B
	def on_transition_changed(A):A.element.setAttribute(_D,A.transition)
	def render(A):F='click';E='aria-label';A._track=div(classes='invent-carousel-track');A._item_slots=[];A._prev_index=0;C=button(classes='invent-carousel-ctrl invent-carousel-ctrl--prev');C.innerHTML=_CARET_LEFT;C.setAttribute(E,_('Previous'));C.addEventListener(F,ffi.create_proxy(A._on_prev));D=button(classes='invent-carousel-ctrl invent-carousel-ctrl--next');D.innerHTML=_CARET_RIGHT;D.setAttribute(E,_('Next'));D.addEventListener(F,ffi.create_proxy(A._on_next));B=div(classes='invent-carousel');B.setAttribute(_D,_B);A._track.addEventListener('touchstart',ffi.create_proxy(A._on_touch_start));A._track.addEventListener('touchend',ffi.create_proxy(A._on_touch_end));B.append(A._track);B.append(C);B.append(D);return B