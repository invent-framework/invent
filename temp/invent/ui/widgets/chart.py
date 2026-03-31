_B='The data to display in the chart.'
_A=None
import asyncio
from pyscript import js_import,window
from pyscript.web import div,canvas
from pyscript.ffi import to_js,create_proxy
from invent.i18n import _
from invent.ui.core import Widget,Event,ChoiceProperty,JSONProperty
_CHARTS=['bar','bubble','doughnut','line','pie','polarArea','radar','scatter']
_chart_js=_A
async def _ensure_chart_js():
	global _chart_js
	if _chart_js is _A:_chart_js,=await js_import('https://esm.run/chart.js/auto')
class Chart(Widget):
	chart_type=ChoiceProperty(_('The type of chart to display.'),default_value='bar',choices=_CHARTS);data=JSONProperty(_(_B),default_value={});options=JSONProperty(_('The options to use when rendering the chart.'),default_value={});chart_updated=Event(_('The chart has been updated.'),chart_type=_('The type of chart to render.'),data=_(_B),options=_('The options used to render the chart.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="48px" height="48px" viewBox="0 0 256 256"><path fill="#000" d="M232 208a8 8 0 0 1-8 8H32a8 8 0 0 1-8-8V48a8 8 0 0 1 16 0v94.37L90.73 98a8 8 0 0 1 10.07-.38l58.81 44.11L218.73 90a8 8 0 1 1 10.54 12l-64 56a8 8 0 0 1-10.07.38l-58.81-44.09L40 163.63V200h184a8 8 0 0 1 8 8"/></svg>'
	def __init__(A,*B,**C):A.chart_canvas=_A;A.chart_instance=_A;super().__init__(*B,**C)
	def on_data_changed(A):A._update_chart()
	def on_options_changed(A):A._update_chart()
	def _update_chart(A):
		if A.parent:
			B={'data':A.data,'responsive':True,'maintainAspectRatio':False}
			if A.chart_type:B['type']=A.chart_type
			if A.options:B['options']=A.options
			if A.chart_instance:A.chart_instance.data=to_js(A.data);A.chart_instance.options=to_js(A.options);A.chart_instance.update()
			else:A.chart_instance=_chart_js.Chart.new(A.chart_canvas._dom_element,to_js(B))
			A.publish('chart_updated',chart_type=A.chart_type,data=A.data,options=A.options)
	async def _init_chart(A):await _ensure_chart_js();window.requestAnimationFrame(create_proxy(lambda x:A._update_chart()))
	def render(A):B=div(id=A.id,style={'max-width':'100%','overflow':'hidden','display':'block','min-width':'0','position':'relative'});A.chart_canvas=canvas();B.append(A.chart_canvas);asyncio.create_task(A._init_chart());return B