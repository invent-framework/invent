from invent.i18n import _
from pyscript.web import progress
from invent.ui.core import Widget,Event,FloatProperty
class Progress(Widget):
	value=FloatProperty(_('The value to display.'),default_value=None);maximum=FloatProperty(_('The maximum allowed value.'),default_value=1e2);changed=Event(_('The value of the progress has changed.'),value=_('The new progress value.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M128 40a96 96 0 1 0 96 96a96.11 96.11 0 0 0-96-96m0 176a80 80 0 1 1 80-80a80.09 80.09 0 0 1-80 80m45.66-125.66a8 8 0 0 1 0 11.32l-40 40a8 8 0 0 1-11.32-11.32l40-40a8 8 0 0 1 11.32 0M96 16a8 8 0 0 1 8-8h48a8 8 0 0 1 0 16h-48a8 8 0 0 1-8-8"/></svg>'
	def on_value_changed(A):A.element.value=A.value;A.publish('changed',value=A.value)
	def on_maximum_changed(A):A.element.max=A.maximum
	def render(A):return progress(id=A.id)