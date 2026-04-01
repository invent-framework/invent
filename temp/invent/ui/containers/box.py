from invent.i18n import _
from..core.container import Container
from..core.property import ChoiceProperty
from..core.measures import TSHIRT_SIZES,MEDIUM
class Box(Container):
	gap=ChoiceProperty(_('The gap between items in the container'),choices=TSHIRT_SIZES,default_value=MEDIUM,group='style')
	def render(B):A=super().render();A.style['display']='flex';return A
	def on_gap_changed(A):A._set_gap(A.gap,'gap')