_A=None
from pyscript import js_import,storage
from.channels import Message,subscribe,publish,unsubscribe
from.datastore import DataStore,IndexDBBackend
from.i18n import _,load_translations
from.media import Media,set_media_root,get_media_root
from.app import App
from.utils import show_page,is_micropython,set_theme
__all__=['Message','subscribe','publish','unsubscribe','datastore','_','load_translations','Media','set_media_root','get_media_root','App','show_page','is_micropython','set_theme','go','init','marked','purify']
datastore=_A
datastore_name='invent'
async def start_datastore(_backend=_A,**C):
	A=_backend;global datastore
	if not datastore:
		if A is _A:B=_A
		elif A==IndexDBBackend:B=await storage(datastore_name,storage_class=A)
		else:B=A()
		datastore=DataStore(_backend=B,**C)
marked=_A
purify=_A
async def load_js_modules():global marked,purify;marked,purify=await js_import('https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js','https://esm.run/dompurify')
media=Media([],'media')
async def setup(_databackend=_A,**A):await start_datastore(_databackend,**A);await load_js_modules()
def go():App.app().go()