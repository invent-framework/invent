from pyscript.ffi import to_js
from pyscript.web import div
from.component import Component
from invent.i18n import _
from.property import ListProperty
from.measures import GAP_SIZES
class Container(Component):
	children=ListProperty(_('The child components of the container.'),default_value=None)
	def on_children_changed(A):
		A.element.replaceChildren()
		for B in A.children:B.parent=A;A.element.append(B.element)
	def _set_gap(A,gap,attr):B=GAP_SIZES;C=B.get(gap.upper(),'0px');A.element.style[attr]=C
	def append(A,item):B=item;B.parent=A;A.children.append(B);A.element.append(B.element)
	def insert(A,index,item):
		C=index;B=item;B.parent=A;A.children.insert(C,B)
		if B is A.children[-1]:A.element.appendChild(B.element)
		else:A.element.insertBefore(B.element,A.element.childNodes[C])
	def remove(B,item):A=item;A.parent=None;B.children.remove(A);A.element.remove()
	def __getitem__(A,index):return A.children[index]
	def __iter__(A):return iter(A.children)
	def __delitem__(A,item):A.remove(item)
	def contains(C,component):
		B=component
		for A in C.children:
			if A is B:return True
			if A.is_container:
				if A.contains(B):return True
		return False
	def render(B):A=div();A.classes.add(f"invent-{type(B).__name__.lower()}");return A