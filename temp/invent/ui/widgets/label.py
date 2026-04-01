from invent.i18n import _
from invent.utils import from_markdown
from invent.ui.core import Widget,TextProperty
from pyscript.web import div
class Label(Widget):
	text=TextProperty(_('The content to display.'),default_value='Text')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176zM184 96a8 8 0 0 1-8 8H80a8 8 0 0 1 0-16h96a8 8 0 0 1 8 8m0 32a8 8 0 0 1-8 8H80a8 8 0 0 1 0-16h96a8 8 0 0 1 8 8m0 32a8 8 0 0 1-8 8H80a8 8 0 0 1 0-16h96a8 8 0 0 1 8 8"/></svg>'
	def on_text_changed(A):A.element.innerHTML=from_markdown(A.text)
	def render(A):B=div(innerHTML=from_markdown(A.text),id=A.id);return B