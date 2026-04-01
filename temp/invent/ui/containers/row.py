from invent.i18n import _
from.box import Box
from..core.property import ChoiceProperty
from..core.measures import COMPONENT_DISTRIBUTION
class Row(Box):
	horizontal_align_content=ChoiceProperty(_('Alignment of child components in this row.'),choices=COMPONENT_DISTRIBUTION,map_to_style='justify-content',group='layout')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 136H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-40a16 16 0 0 0-16-16m0 56H48v-40h160zm0-144H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m0 56H48V64h160z"/></svg>'
	def __init__(A,*B,**C):super().__init__(*B,**C);A.element.style['flex-direction']='row';A.element.style['flex-wrap']='wrap'