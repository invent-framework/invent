from invent.i18n import _
from..core.box import Box
from..core.property import ChoiceProperty
from..core.measures import COMPONENT_DISTRIBUTION
class Column(Box):
	vertical_align_content=ChoiceProperty(_('Alignment of child components in this column.'),choices=COMPONENT_DISTRIBUTION,map_to_style='justify-content',group='layout')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M104 32H64a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176H64V48h40Zm88-176h-40a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176h-40V48h40Z"/></svg>'
	def __init__(A,*B,**C):super().__init__(*B,**C);A.element.style['flex-direction']='column'