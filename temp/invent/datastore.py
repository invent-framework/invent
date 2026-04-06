_A=None
import json
from pyscript import Storage,window
from.channels import Message,publish
class DataBackend:
	def clear(A):raise NotImplementedError
	def copy(A):return{A:B for(A,B)in A.items()}
	def get(A,key,default=_A):
		if key in A:return A[key]
		return default
	def items(A):
		for B in A.keys():C=A[B];yield(B,C)
	def keys(A):raise NotImplementedError
	def pop(A,key,default=_A):
		B=key
		if B in A:C=A[B];del A[B]
		else:C=default
		return C
	def popitem(A):raise NotImplementedError
	def setdefault(A,key,value=_A):
		C=value;B=key
		if B in A:return A[B]
		A[B]=C;return C
	async def sync(A):raise NotImplementedError
	def update(C,*D,**E):
		A={}
		for B in D:
			if isinstance(B,dict):A.update(B)
		A.update(E)
		for(F,G)in A.items():C[F]=G
	def values(A):
		B=[]
		for C in A.keys():B.append(A[C])
		return B
	def __len__(A):return len(list(A.keys()))
	def __setitem__(A,key,value):raise NotImplementedError
	def __getitem__(A,key):raise NotImplementedError
	def __delitem__(A,key):raise NotImplementedError
	def __iter__(A):return(A for A in A.keys())
	def __contains__(A,key):return key in A.keys()
class _FakeStorage(dict):
	@property
	def length(self):return len(self)
	def key(A,i):return list(A.keys())[i]
	def getItem(A,key):return A[key]
	def setItem(A,key,value):A[key]=value
	def removeItem(A,key):del A[key]
class LocalStorageBackend(DataBackend):
	def __init__(A,**B):
		A.namespace='invent-'
		try:A.store=window.localStorage
		except ImportError:A.store=_FakeStorage()
		if B:A.update(B)
	def clear(A):return A.store.clear()
	def keys(A):
		B=[];D=len(A.namespace)
		for E in range(0,A.store.length):
			C=A.store.key(E)
			if C.startswith(A.namespace):F=C[D:];B.append(F)
		return B
	async def sync(A):0
	def _namespace_key(A,key):return f"{A.namespace}{key}"
	def __getitem__(A,key):
		B=key
		if B in A:return json.loads(A.store.getItem(A._namespace_key(B)))
		else:raise KeyError(B)
	def __setitem__(A,key,value):B=A.store.setItem(A._namespace_key(key),json.dumps(value));return B
	def __delitem__(A,key):
		B=key
		if B in A:C=A.store.removeItem(A._namespace_key(B));return C
		else:raise KeyError(B)
class IndexDBBackend(Storage,DataBackend):...
class DataStore(DataBackend):
	DATASTORE_SET_CHANNEL='datastore:set';DATASTORE_DELETE_CHANNEL='datastore:delete'
	def __init__(C,_backend=_A,**B):
		A=_backend
		if A is _A:A=LocalStorageBackend(**B)
		else:A.update(**B)
		C.backend=A
	def clear(A):A.backend.clear()
	def keys(A):return A.backend.keys()
	async def sync(A):await A.backend.sync()
	def __getitem__(A,key):return A.backend[key]
	def __setitem__(A,key,value):B=value;A.backend[key]=B;publish(Message(subject=key,value=B),to_channel=A.DATASTORE_SET_CHANNEL)
	def __delitem__(A,key):del A.backend[key];publish(Message(subject=key),to_channel=A.DATASTORE_DELETE_CHANNEL)