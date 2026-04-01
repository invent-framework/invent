import asyncio
from.utils import iscoroutinefunction
__all__=['Message','subscribe','publish','unsubscribe','when']
_channels={}
class Message:
	def __init__(A,subject,**B):
		A._subject=subject
		for(C,D)in B.items():setattr(A,C,D)
	def __str__(A):B=A._subject+' ';B+=str({A:B for(A,B)in A.__dict__.items()if not A.startswith('_')});return B
def subscribe(handler,to_channel,when_subject):
	B=when_subject;A=to_channel
	if isinstance(A,str):A=[A]
	if isinstance(B,str):B=[B]
	for C in A:
		if C not in _channels:_channels[C]={}
		for D in B:E=_channels[C].get(D,set());E.add(handler);_channels[C][D]=E
def publish(message,to_channel):
	B=to_channel;A=message
	if isinstance(B,str):B=[B]
	for E in B:
		D=_channels.get(E,{})
		if A._subject in D:
			for C in D[A._subject]:
				if iscoroutinefunction(C):asyncio.create_task(C(A))
				else:C(A)
def unsubscribe(handler,from_channel,when_subject):
	E=handler;B=when_subject;A=from_channel
	if isinstance(A,str):A=[A]
	if isinstance(B,str):B=[B]
	for F in A:
		C=_channels.get(F)
		if C:
			for D in B:
				if D in C and E in C[D]:C[D].remove(E)
				else:raise ValueError(f"Cannot unsubscribe from unknown message type: {D}")
		else:raise ValueError(f"Cannot unsubscribe from unknown channel: {F}")