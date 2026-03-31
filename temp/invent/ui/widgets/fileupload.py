from invent.i18n import _
from pyscript.web import input_
from pyscript.ffi import create_proxy
from invent.ui.core import Widget,ListProperty
class FileUpload(Widget):
	_files_={}
	@classmethod
	def get_file_by_name(A,filename):return A._files_.get(filename)
	@classmethod
	def get_filenames(A):return A._files_.keys()
	files=ListProperty(_('The files to upload'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><g fill="currentColor"><path d="M208 88h-56V32Z" opacity="0.2"/><path d="m213.66 82.34l-56-56A8 8 0 0 0 152 24H56a16 16 0 0 0-16 16v176a16 16 0 0 0 16 16h144a16 16 0 0 0 16-16V88a8 8 0 0 0-2.34-5.66M160 51.31L188.69 80H160ZM200 216H56V40h88v48a8 8 0 0 0 8 8h48zm-42.34-77.66a8 8 0 0 1-11.32 11.32L136 139.31V184a8 8 0 0 1-16 0v-44.69l-10.34 10.35a8 8 0 0 1-11.32-11.32l24-24a8 8 0 0 1 11.32 0Z"/></g></svg>'
	def on_change(B,event):A=event.target.files.item(0);FileUpload._files_[A.name]=A;B.files=B.files+[A.name]
	def render(A):B=input_(type='file',id=A.id);B.addEventListener('change',create_proxy(A.on_change));return B