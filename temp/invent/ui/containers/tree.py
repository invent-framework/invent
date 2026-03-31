from invent.i18n import _
from pyscript.web import nav,details,summary,div
from invent.ui.core import Widget,DictProperty
from invent.ui.widgets.label import Label
class Tree(Widget):
	data=DictProperty(_('The data to be displayed in the tree. Should be a nested dictionary.'),default_value={})
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M176,152h32a16,16,0,0,0,16-16V104a16,16,0,0,0-16-16H176a16,16,0,0,0-16,16v8H88V80h8a16,16,0,0,0,16-16V32A16,16,0,0,0,96,16H64A16,16,0,0,0,48,32V64A16,16,0,0,0,64,80h8V192a24,24,0,0,0,24,24h64v8a16,16,0,0,0,16,16h32a16,16,0,0,0,16-16V192a16,16,0,0,0-16-16H176a16,16,0,0,0-16,16v8H96a8,8,0,0,1-8-8V128h72v8A16,16,0,0,0,176,152ZM64,32H96V64H64ZM176,192h32v32H176Zm0-88h32v32H176Z"></path></svg>'
	def on_data_changed(A):A.element=A.render()
	def make_tree(B,parent,data):
		C=parent
		for(D,A)in data.items():
			if isinstance(A,dict):B.make_branch(C,D,A)
			else:B.make_leaf(C,D,A)
	def make_leaf(C,parent,key,value):
		A=value;B=div(classes=['invent-tree-leaf']);parent.append(B)
		if isinstance(A,Widget):B.append(A.render())
		else:B.append(Label(name=key,text=f"{A}").render())
	def make_branch(C,parent,label,subtree):A=label;B=details(summary(Label(name=A,text=A).render()));C.make_tree(B,subtree);parent.append(B)
	def render(A):B=nav(classes=['invent-tree']);A.make_tree(B,A.data);return B