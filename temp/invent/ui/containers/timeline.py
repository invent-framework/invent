_A='latest-at-top'
from invent.i18n import _
from..core.property import ListProperty,ChoiceProperty
from.column import Column
class Timeline(Column):
	direction=ChoiceProperty(_('The direction of the timeline entries'),choices=[_A,'latest-at-bottom'],default_value=_A)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M216 80h-32V48a16 16 0 0 0-16-16H40a16 16 0 0 0-16 16v128a8 8 0 0 0 13 6.22L72 154v30a16 16 0 0 0 16 16h93.59L219 230.22a8 8 0 0 0 5 1.78a8 8 0 0 0 8-8V96a16 16 0 0 0-16-16M66.55 137.78L40 159.25V48h128v88H71.58a8 8 0 0 0-5.03 1.78M216 207.25l-26.55-21.47a8 8 0 0 0-5-1.78H88v-32h80a16 16 0 0 0 16-16V96h32Z"/></svg>'
	def on_direction_changed(A):
		B='flex-direction'
		if A.direction==_A:A.element.style[B]='column-reverse'
		else:A.element.style[B]='column'