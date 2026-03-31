__all__=['set_media_root','get_media_root','Media']
__root__='.'
def set_media_root(root):global __root__;__root__=root
def get_media_root():global __root__;return __root__
class Media:
	def __init__(A,path,name):A._path=path;A._name=name
	def __getattr__(A,attr_name):return Media(A._path+[A._name],attr_name)
	def __str__(A):global __root__;B=[__root__]+A._path;return'/'.join(B)+'.'+A._name