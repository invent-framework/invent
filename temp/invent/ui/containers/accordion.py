from pyscript.web import div,input_
from invent.i18n import _
from.column import Column
class Accordion(Column):
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 88H48a16 16 0 0 0-16 16v96a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-96a16 16 0 0 0-16-16m0 112H48v-96h160zM48 64a8 8 0 0 1 8-8h144a8 8 0 0 1 0 16H56a8 8 0 0 1-8-8m16-32a8 8 0 0 1 8-8h112a8 8 0 0 1 0 16H72a8 8 0 0 1-8-8"/></svg>'
	def on_children_changed(A):
		A.element.replaceChildren()
		for(C,B)in enumerate(A.children):D=div(input_(type='checkbox',name=A.id,checked=C==0),div(B.name,classes='invent-accordion-title'),div(B.element,classes='invent-accordion-content'),classes='invent-accordion-item');A.element.append(D)
	def on_id_changed(A):super().on_id_changed();A.on_children_changed()