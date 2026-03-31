_A=None
from pyscript import js_import
from pyscript.ffi import to_js
from pyscript.web import div,style,page
from invent.i18n import _
from invent.ui.core import Widget,TextProperty,BooleanProperty
_default='\ndef hello(name="world"):\n    return f"Hello, {name}"\n'
_THEMES={'light':'github-light','dark':'github-dark'}
_SHIKI_CSS="\n@media (prefers-color-scheme: dark) {\n    .shiki, .shiki span {\n        color: var(--shiki-dark) !important;\n        background-color: var(--shiki-dark-bg) !important;\n    }\n\n    /* Re-assert highlight on the line and all token spans within it. */\n    pre.shiki .line.highlighted,\n    pre.shiki .line.highlighted span {\n        background-color: rgba(255, 200, 0, 0.12) !important;\n    }\n}\n\n/* Line numbers: CSS counter on Shiki's generated .line spans.\n   The line-numbers class on <pre> acts as the toggle. */\npre.shiki.line-numbers {\n    counter-reset: line;\n}\n\npre.shiki.line-numbers .line::before {\n    counter-increment: line;\n    content: counter(line);\n    display: inline-block;\n    /* Enough width for 3-4 digit line counts. */\n    width: 2rem;\n    margin-right: 1rem;\n    text-align: right;\n    /* Muted so numbers don't compete with code. */\n    color: #888;\n    user-select: none;\n}\n\n/* Highlighted lines: neutral tint with a subtle left accent. Works in\n   both light and dark mode without needing separate colour values. */\npre.shiki .line.highlighted {\n    background-color: rgba(255, 200, 0, 0.15) !important;\n    /* Inset box-shadow gives the left accent without affecting layout. */\n    box-shadow: inset 3px 0 0 rgba(255, 200, 0, 0.6);\n}\n"
_shiki=_A
_shiki_transformers=_A
_shiki_css_injected=False
async def _ensure_shiki():
	global _shiki,_shiki_transformers,_shiki_css_injected
	if _shiki is _A:_shiki,_shiki_transformers=await js_import('https://esm.sh/shiki@3','https://esm.sh/@shikijs/transformers')
	if not _shiki_css_injected:page.head.append(style(_SHIKI_CSS));_shiki_css_injected=True
class Code(Widget):
	code=TextProperty(_('The code to display.'),default_value=_default);language=TextProperty(_('The language of the code.'),default_value='python');line_numbers=BooleanProperty(_('Flag for displaying line numbers.'),default_value=False);highlight=TextProperty(_("Lines to highlight, e.g. '1' or '1,3-5'."),default_value=_A)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M69.12 94.15L28.5 128l40.62 33.85a8 8 0 1 1-10.24 12.29l-48-40a8 8 0 0 1 0-12.29l48-40a8 8 0 0 1 10.24 12.3m176 27.7l-48-40a8 8 0 1 0-10.24 12.3L227.5 128l-40.62 33.85a8 8 0 1 0 10.24 12.29l48-40a8 8 0 0 0 0-12.29m-82.39-89.37a8 8 0 0 0-10.25 4.79l-64 176a8 8 0 0 0 4.79 10.26A8.14 8.14 0 0 0 96 224a8 8 0 0 0 7.52-5.27l64-176a8 8 0 0 0-4.79-10.25"/></svg>'
	async def _highlight_code(A):
		await _ensure_shiki();B={'lang':A.language,'themes':_THEMES}
		if A.highlight:B['meta']={'__raw':'{'+A.highlight+'}'};B['transformers']=[_shiki_transformers.transformerMetaHighlight()]
		B=to_js(B);C=await _shiki.codeToHtml(A.code,B);A._container.replaceChildren();A._container._dom_element.innerHTML=C;A._update_line_numbers()
	def _update_line_numbers(A):
		D='line-numbers';B=A._container.find('pre')
		if not B:return
		C=B[0]
		if A.line_numbers:C.classes.add(D)
		else:C.classes.remove(D)
	async def on_code_changed(A):await A._highlight_code()
	async def on_language_changed(A):await A._highlight_code()
	def on_line_numbers_changed(A):A._update_line_numbers()
	async def on_highlight_changed(A):await A._highlight_code()
	def render(A):A._container=div(id=A.id);return A._container