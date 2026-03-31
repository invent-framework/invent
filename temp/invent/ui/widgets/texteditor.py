_C='silent'
_B=False
_A=None
import asyncio,json,js
from pyscript import js_import
from pyscript.ffi import create_proxy
from pyscript.web import div
from invent.i18n import _
from invent.ui.core import Widget,DictProperty,Event,TextProperty
_DEBOUNCE_DELAY=.3
_QUILL_JS='https://esm.sh/quill@2.0.3'
_QUILL_CSS='https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css'
_DELTA_TO_MD_JS='https://esm.sh/quill-delta-to-markdown@0.6.0'
_MD_TO_DELTA_JS='https://esm.sh/markdown-to-quill-delta@1.0.1'
_DEFAULT_CONFIG={'modules':{'toolbar':[[{'header':[1,2,_B]}],['bold','italic','underline'],['image','code-block']]},'placeholder':'Compose an epic...','theme':'snow'}
class TextEditor(Widget):
	text=TextProperty(_('The textual content of the editor as Markdown.'),default_value='');delta=DictProperty(_('The underlying Quill Delta representation of the editor content.'),default_value={});min_height=TextProperty(_("Minimum height of the editor as a CSS length (e.g. '200px')."),default_value='200px',group='style');changed=Event(_('Fired when the user edits the text (debounced).'),text=_('The new Markdown textual content after the change.'))
	def __init__(A,config=_A,**C):B=config;A._config=B if B is not _A else _DEFAULT_CONFIG;A._quill=_A;A._updating=_B;A._debounce_task=_A;super().__init__(**C)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M128,96H232a8,8,0,0,1,0,16H128a8,8,0,0,1,0-16Zm104,32H128a8,8,0,0,0,0,16H232a8,8,0,0,0,0-16Zm0,32H80a8,8,0,0,0,0,16H232a8,8,0,0,0,0-16Zm0,32H80a8,8,0,0,0,0,16H232a8,8,0,0,0,0-16ZM96,144a8,8,0,0,0,0-16H88V64h32v8a8,8,0,0,0,16,0V56a8,8,0,0,0-8-8H32a8,8,0,0,0-8,8V72a8,8,0,0,0,16,0V64H72v64H64a8,8,0,0,0,0,16Z"/></svg>'
	def render(A):B=div();B.classList.add('invent-text-editor');A._mount=js.document.createElement('div');B._dom_element.appendChild(A._mount);asyncio.create_task(A._init_quill());return B
	async def _init_quill(A):
		if not js.document.querySelector(f'link[href="{_QUILL_CSS}"]'):B=js.document.createElement('link');B.rel='stylesheet';B.href=_QUILL_CSS;js.document.head.appendChild(B)
		C,D,E=await js_import(_QUILL_JS,_DELTA_TO_MD_JS,_MD_TO_DELTA_JS);F=C.default;A._delta_to_markdown=D.deltaToMarkdown;A._markdown_to_delta=E.default;G=js.JSON.parse(json.dumps(A._config));A._quill=F.new(A._mount,G);A.on_min_height_changed()
		if A.text:A._load_markdown(A.text)
		elif A.delta.get('ops'):A._load_delta(A.delta)
		def H(delta,old,source):
			if A._debounce_task:A._debounce_task.cancel()
			A._debounce_task=asyncio.create_task(A._debounced_sync())
		A._quill.on('text-change',create_proxy(H))
	async def _debounced_sync(A):
		try:await asyncio.sleep(_DEBOUNCE_DELAY)
		except asyncio.CancelledError:return
		if A._quill is _A:return
		B=A._quill.getContents().ops;C=str(A._delta_to_markdown(B));D=json.loads(str(js.JSON.stringify(B)));A._updating=True
		try:A.delta={'ops':D};A.text=C
		finally:A._updating=_B
		A.publish('changed',text=A.text)
	def _load_markdown(A,markdown):
		if A._quill is _A:return
		C=A._markdown_to_delta(markdown);B=js.Object.new();B.ops=C;A._quill.setContents(B,_C)
	def _load_delta(A,delta_dict):
		if A._quill is _A:return
		B=js.JSON.parse(json.dumps(delta_dict));A._quill.setContents(B,_C)
	def on_text_changed(A):
		if A._updating:return
		A._load_markdown(A.text)
	def on_delta_changed(A):
		if A._updating:return
		A._load_delta(A.delta)
	def on_min_height_changed(A):
		C='min-height';A.element.style[C]=A.min_height;B=A._mount.querySelector('.ql-editor')
		if B:B.style.setProperty(C,A.min_height)