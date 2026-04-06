_I='.cm-editor'
_H='extensions'
_G='change'
_F='min-height'
_E='python'
_D='(prefers-color-scheme: dark)'
_C='auto'
_B=False
_A=None
import asyncio,js
from pyscript import js_import
from pyscript.ffi import create_proxy,to_js
from pyscript.web import div
from invent.i18n import _
from invent.ui.core import Widget,BooleanProperty,ChoiceProperty,Event,TextProperty
_DEBOUNCE_DELAY=.3
_cm=_A
_cm_state=_A
_cm_dark=_A
_lang_packs={}
_LANG_URLS={_E:'https://esm.sh/@codemirror/lang-python'}
def register_language(name,url):_LANG_URLS[name]=url
async def _load_cm():
	global _cm,_cm_state,_cm_dark
	if _cm is not _A:return
	_cm,_cm_state,_cm_dark=await js_import('https://esm.sh/codemirror','https://esm.sh/@codemirror/state','https://esm.sh/@codemirror/theme-one-dark')
async def _load_lang_pack(language):
	A=language
	if A in _lang_packs:return _lang_packs[A]
	B=_LANG_URLS.get(A)
	if not B:return
	C,=await js_import(B);_lang_packs[A]=C;return C
class CodeEditor(Widget):
	code=TextProperty(_('The code content of the editor.'),default_value='');language=TextProperty(_('The language for syntax highlighting.'),default_value=_E);readonly=BooleanProperty(_('Whether the editor content can be edited.'),default_value=_B);min_height=TextProperty(_("Minimum height of the editor as a CSS length (e.g. '200px')."),default_value='200px',group='style');theme=ChoiceProperty(_('The colour theme of the editor.'),default_value=_C,choices=['light','dark',_C],group='style');changed=Event(_('Fired when the user edits the code (debounced).'),code=_('The new code content after the change.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M58.34,101.66l-32-32a8,8,0,0,1,0-11.32l32-32A8,8,0,0,1,69.66,37.66L43.31,64,69.66,90.34a8,8,0,0,1-11.32,11.32Zm40,0a8,8,0,0,0,11.32,0l32-32a8,8,0,0,0,0-11.32l-32-32A8,8,0,0,0,98.34,37.66L124.69,64,98.34,90.34A8,8,0,0,0,98.34,101.66ZM200,40H176a8,8,0,0,0,0,16h24V200H56V136a8,8,0,0,0-16,0v64a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V56A16,16,0,0,0,200,40Z"></path></svg>'
	def __init__(A,**B):A._view=_A;A._setting_code=_B;A._debounce_task=_A;A._update_proxy=create_proxy(A._on_cm_update);A._mq_proxy=_A;super().__init__(**B)
	def render(A):B=div(classes=['invent-code-editor']);B.style[_F]=A.min_height;asyncio.create_task(A._init_editor());return B
	def _is_dark(A):
		if A.theme=='dark':return True
		if A.theme==_C:return js.window.matchMedia(_D).matches
		return _B
	def _remove_mq_listener(A):
		if A._mq_proxy is _A:return
		js.window.matchMedia(_D).removeEventListener(_G,A._mq_proxy);A._mq_proxy.destroy();A._mq_proxy=_A
	async def _build_extensions(A):
		B=[_cm.basicSetup]
		if A._is_dark():B.append(_cm_dark.oneDark)
		C=await _load_lang_pack(A.language)
		if C:
			D=getattr(C,A.language,_A)
			if D:B.append(D())
		if A.readonly:B.append(_cm.EditorView.editable.of(_B))
		B.append(_cm.EditorView.updateListener.of(A._update_proxy))
		if A.theme==_C and A._mq_proxy is _A:A._mq_proxy=create_proxy(lambda _e:asyncio.create_task(A._reconfigure()));js.window.matchMedia(_D).addEventListener(_G,A._mq_proxy)
		return to_js(B)
	async def _init_editor(A):
		await _load_cm();C=await A._build_extensions();D=_cm_state.EditorState.create(to_js({'doc':A.code or'',_H:C}));A._view=_cm.EditorView.new(to_js({'state':D,'parent':A.element._dom_element}));B=A.element._dom_element.querySelector(_I)
		if B:B.style.height=A.min_height
	async def _reconfigure(A):
		if A._view is _A:return
		B=await A._build_extensions();C=A._view.state.doc.toString();D=_cm_state.EditorState.create(to_js({'doc':C,_H:B}));A._view.setState(D)
	def _on_cm_update(A,update):
		if not update.docChanged:return
		if A._debounce_task:A._debounce_task.cancel()
		A._debounce_task=asyncio.create_task(A._emit_changed())
	async def _emit_changed(A):await asyncio.sleep(_DEBOUNCE_DELAY);A._setting_code=True;A.code=A._view.state.doc.toString();A._setting_code=_B;A.publish(A.changed,code=A.code)
	def on_code_changed(A):
		if A._setting_code or A._view is _A:return
		A._view.dispatch(to_js({'changes':{'from':0,'to':A._view.state.doc.length,'insert':A.code or''}}))
	def on_min_height_changed(A):
		if A.element is _A:return
		A.element.style[_F]=A.min_height;B=A.element._dom_element.querySelector(_I)
		if B:B.style.height=A.min_height
	def on_language_changed(A):asyncio.create_task(A._reconfigure())
	def on_readonly_changed(A):asyncio.create_task(A._reconfigure())
	def on_theme_changed(A):A._remove_mq_listener();asyncio.create_task(A._reconfigure())