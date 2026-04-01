_A='worker'
from invent.i18n import _
from pyscript.web import script,page
from invent.ui.core import Widget,TextProperty
_INTERPRETERS={'py','mpy'}
class Terminal(Widget):
	evaluate=TextProperty(_('Dynamically evaluated Python code to execute in the terminal.'),default_value=None)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M128,128a8,8,0,0,1-3,6.25l-40,32a8,8,0,1,1-10-12.5L107.19,128,75,102.25a8,8,0,1,1,10-12.5l40,32A8,8,0,0,1,128,128Zm48,24H136a8,8,0,0,0,0,16h40a8,8,0,0,0,0-16Zm56-96V200a16,16,0,0,1-16,16H40a16,16,0,0,1-16-16V56A16,16,0,0,1,40,40H216A16,16,0,0,1,232,56ZM216,200V56H40V200H216Z"></path></svg>'
	def __init__(A,**B):
		A._init_code=B.pop('code',None);A._src_path=B.pop('src',None)
		if A._src_path and A._init_code:raise ValueError("Cannot specify both 'code' and 'src' for Terminal widget.")
		A._worker_flag=B.pop(_A,True);A._interpreter=B.pop('interpreter','py')
		if A._interpreter not in _INTERPRETERS:raise ValueError(f"Invalid interpreter '{A._interpreter}'. Valid options are: {_INTERPRETERS}")
		super().__init__(**B)
	def on_evaluate_changed(A):
		B=page.find(f"{A.id}")
		if B:B._dom_element.process(A.evaluate)
	def render(A):
		B=script();B.setAttribute('type',A._interpreter);B.setAttribute('terminal','')
		if A._worker_flag:B.setAttribute(_A,'')
		if A._src_path:B.setAttribute('src',A._src_path)
		if A._init_code:B.innerHTML=A._init_code
		return B