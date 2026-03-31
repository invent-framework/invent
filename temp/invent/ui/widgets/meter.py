_A='display'
from invent.i18n import _
from pyscript.web import meter
from invent.ui.core import Widget,Event,FloatProperty,TextProperty
class Meter(Widget):
	value=FloatProperty(_('The value to display.'),default_value=5e1);minimum=FloatProperty(_('The minimum allowed value.'),default_value=.0);maximum=FloatProperty(_('The maximum allowed value.'),default_value=1e2);low=FloatProperty(_('The value below which the meter is considered low.'),default_value=33.,group=_A);high=FloatProperty(_('The value above which the meter is considered high.'),default_value=66.,group=_A);optimum=FloatProperty(_('The value considered to be the optimum value.'),default_value=5e1,group=_A);title=TextProperty(_('The title of the meter, displayed when the mouse hovers over it.'),default_value='');changed=Event(_('The value of the meter has changed.'),value=_('The new value of the meter.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M80 96a8 8 0 0 1-8 8H24a8 8 0 0 1 0-16h48a8 8 0 0 1 8 8m-8 24H24a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32H24a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32H24a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m80-64h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m80-96h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m-48-16h48a8 8 0 0 0 0-16h-48a8 8 0 0 0 0 16m48 48h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16"/></svg>'
	def on_value_changed(A):A.element.value=A.value;A.publish('changed',value=A.value)
	def on_minimum_changed(A):A.element.min=A.minimum
	def on_maximum_changed(A):A.element.max=A.maximum
	def on_low_changed(A):A.element.low=A.low
	def on_high_changed(A):A.element.high=A.high
	def on_optimum_changed(A):A.element.optimum=A.optimum
	def on_title_changed(A):A.element.title=A.title
	def render(A):return meter(id=A.id)