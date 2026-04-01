from invent.i18n import _
from..core.container import Container
from..core.property import ChoiceProperty,IntegerProperty
from..core.measures import TSHIRT_SIZES,MEDIUM
class Grid(Container):
	column_gap=ChoiceProperty(_('The gap between columns in the grid.'),choices=TSHIRT_SIZES,default_value=MEDIUM,group='style');row_gap=ChoiceProperty(_('The gap between rows in the grid.'),choices=TSHIRT_SIZES,default_value=MEDIUM,group='style');columns=IntegerProperty(_('Number of columns.'),4,group='layout')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 48H40a16 16 0 0 0-16 16v128a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m-112 96v-32h48v32Zm48 16v32h-48v-32ZM40 112h48v32H40Zm64-16V64h48v32Zm64 16h48v32h-48Zm48-16h-48V64h48ZM88 64v32H40V64Zm-48 96h48v32H40Zm176 32h-48v-32h48z"/></svg>'
	def on_column_gap_changed(A):A._set_gap(A.column_gap,'column-gap')
	def on_row_gap_changed(A):A._set_gap(A.row_gap,'row-gap')
	def on_columns_changed(A):A.element.style['grid-template-columns']='auto '*A.columns
	def render(B):A=super().render();A.style['display']='grid';return A