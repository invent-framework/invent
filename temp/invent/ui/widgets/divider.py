_A='invent-divider-horizontal'
from invent.i18n import _
from pyscript.web import hr
from invent.ui.core import Widget
from invent.ui.containers import Row
class Divider(Widget):
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 128a8 8 0 0 1-8 8H48a8 8 0 0 1 0-16h160a8 8 0 0 1 8 8Z"/></svg>'
	def render(B):A=hr(id=B.id);A.classes.add('invent-divider');A.classes.add(_A);return A
	@property
	def parent(self):return super().parent
	@parent.setter
	def parent(self,parent):B=parent;A=self;A._parent=B;A._parent_type=type(B).__name__;A.on_horizontal_align_changed();A.on_vertical_align_changed();A._update_orientation()
	def _update_orientation(A):
		B='invent-divider-vertical';A.element.classes.remove(_A);A.element.classes.remove(B)
		if isinstance(A._parent,Row):A.element.classes.add(B)
		else:A.element.classes.add(_A)