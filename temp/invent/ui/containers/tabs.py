_A='htmlFor'
from pyscript.web import div,input_,label
from invent.i18n import _
from..core.container import Container
class Tabs(Container):
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M255.66 165.7a.2.2 0 0 0 0-.08L233.37 91.4A15.89 15.89 0 0 0 218.05 80H208a8 8 0 0 0 0 16h10.05l19.2 64H206l-20.63-68.6A15.89 15.89 0 0 0 170.05 80H160a8 8 0 0 0 0 16h10.05l19.2 64H158l-20.63-68.6A15.89 15.89 0 0 0 122.05 80H38a15.89 15.89 0 0 0-15.37 11.4L.37 165.6v.13A8.1 8.1 0 0 0 0 168a8 8 0 0 0 8 8h240a8 8 0 0 0 7.66-10.3M38 96h84.1l19.2 64H18.75Z"/></svg>'
	def on_children_changed(A):
		A.element.replaceChildren()
		for(B,C)in enumerate(A.children):D=f"{A.id}-tab-{B}";E=label(C.name,classes='invent-tabs-label');setattr(E._dom_element,_A,D);A.element.append(input_(type='radio',id=D,name=A.id,checked=B==0,classes='invent-tabs-radiotab'),E,div(C.element,classes='invent-tabs-panel'))
	def on_id_changed(A):
		super().on_id_changed()
		for(C,B)in enumerate(A.element.find('input[type=radio]')):D=f"{A.id}-tab-{C}";B.id=D;B.name=A.id
		for(C,B)in enumerate(A.element.find('label')):D=f"{A.id}-tab-{C}";setattr(B._dom_element,_A,D)