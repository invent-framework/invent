_D='maximum'
_C='minimum'
_B='default_value'
_A=None
import asyncio,datetime,json,invent,collections
from invent.i18n import _
from invent.utils import iscoroutinefunction
class ValidationError(ValueError):...
class from_datastore:
	def __init__(A,key,with_function=_A):A.key=key;A.with_function=with_function
	def __repr__(A):
		B=f"from_datastore({A.key!r}"
		if A.with_function:B+=f", with_function={A.with_function.__name__}"
		B+=')';return B
class Property:
	_property_counter=0
	def __init__(A,description,default_value=_A,required=False,map_to_attribute=_A,map_to_style=_A,group=_A):A.description=description;A.required=required;A.default_value=A.validate(default_value);A.map_to_attribute=map_to_attribute;A.map_to_style=map_to_style;A.group=group
	def __set_name__(A,owner,name):B=name;A.name=B;A.private_name=f"_{B}";A.from_datastore_name=f"_{B}_from_datastore"
	def __get__(A,obj,objtype=_A):return getattr(obj,A.private_name,A.default_value)
	def __set__(A,obj,value):
		C=obj;B=value;E=A.get_from_datastore(C)
		if E and not isinstance(B,from_datastore):F=A.validate(B);invent.datastore[E.key]=F;return
		if isinstance(B,from_datastore):
			D=B.with_function
			def G(message):
				B=message
				if D is not _A:E=D(B.value)
				else:E=B.value
				setattr(C,A.private_name,A.validate(E));A._react_on_change(C,A.private_name)
			A.set_from_datastore(C,B,G);B=invent.datastore.get(B.key,A.default_value)
			if D is not _A:B=D(B)
		setattr(C,A.private_name,A.validate(B));A._react_on_change(C,A.private_name)
	def get_from_datastore(A,obj):return getattr(obj,A.from_datastore_name,_A)
	def set_from_datastore(B,obj,value,reactor=_A):
		E=reactor;C=value;A=obj;D=f"_{B.name}_reactor";F=B.get_from_datastore(A)
		if F:invent.unsubscribe(getattr(A,D),invent.datastore.DATASTORE_SET_CHANNEL,F.key);delattr(A,D)
		setattr(A,B.from_datastore_name,C)
		if C:invent.subscribe(E,invent.datastore.DATASTORE_SET_CHANNEL,C.key);setattr(A,D,E)
	def _react_on_change(B,obj,property_name):
		A=obj
		if B.map_to_attribute and A.element:A.update_attribute(B.map_to_attribute,getattr(A,B.private_name))
		if B.map_to_style and A.element:A.element.style[B.map_to_style]=getattr(A,B.private_name)
		C=getattr(A,'on'+property_name+'_changed',_A)
		if C:
			if iscoroutinefunction(C):asyncio.create_task(C())
			else:C()
	def coerce(A,value):return value
	def validate(B,value):
		A=value;A=B.coerce(A)
		if B.required and A is _A:raise ValidationError(_('This property is required.'))
		return A
	def as_dict(A):return{'property_type':A.__class__.__name__,'description':A.description,'required':A.required,_B:A.default_value,'group':A.group}
class NumericProperty(Property):
	def __init__(A,description,default_value=_A,minimum=_A,maximum=_A,**B):A.minimum=minimum;A.maximum=maximum;super().__init__(description,default_value,**B)
	def coerce(C,value):
		A=value
		if A is _A:return
		if'.'in str(A):
			try:B=float(A);return B
			except ValueError:pass
		else:
			try:B=int(A);return B
			except ValueError:pass
		raise ValueError(_('Not a valid number: ')+A)
	def validate(B,value):
		A=value;A=super().validate(B.coerce(A))
		if A is not _A:
			if B.minimum and A<B.minimum:raise ValidationError(_('The value is less than the minimum allowed.'),A,B.minimum)
			if B.maximum and A>B.maximum:raise ValidationError(_('The value is greater than the maximum.'),A,B.maximum)
		return A
	def as_dict(B):A=super().as_dict();A[_C]=B.minimum;A[_D]=B.maximum;return A
class IntegerProperty(NumericProperty):
	def coerce(B,value):A=value;return int(A)if A is not _A else _A
class FloatProperty(NumericProperty):
	def coerce(B,value):A=value;return float(A)if A is not _A else _A
class TextProperty(Property):
	def __init__(A,description,default_value=_A,min_length=_A,max_length=_A,**B):A.min_length=min_length;A.max_length=max_length;super().__init__(description,default_value,**B)
	def coerce(B,value):A=value;return str(A)if A is not _A else _A
	def validate(A,value):
		B=value;B=super().validate(A.coerce(B))
		if B is not _A:
			C=len(B)
			if A.min_length and C<A.min_length:raise ValidationError(_('The length of the value is less than minimum allowed.'))
			if A.max_length and C>A.max_length:raise ValidationError(_('The length of the value is more than maximum allowed.'))
		return B
	def as_dict(B):A=super().as_dict();A['min_length']=B.min_length;A['max_length']=B.max_length;return A
class BooleanProperty(Property):
	def coerce(B,value):A=value;return bool(A)if A is not _A else _A
class ListProperty(Property):
	def __init__(B,description,default_value=_A,**A):super().__init__(description,default_value or list(),**A)
	def coerce(B,value):
		A=value
		if A is _A:return[]
		try:return list(A)
		except:raise ValidationError(_('Not a valid list.'),A)
class DictProperty(Property):
	def __init__(B,description,default_value=_A,**A):super().__init__(description,default_value or collections.OrderedDict(),**A)
	def coerce(E,value):
		B=value
		if B is _A:return collections.OrderedDict()
		try:
			A=collections.OrderedDict(B)
			for(D,C)in A.items():
				A[D]=C
				if isinstance(C,(dict,tuple,list)):
					try:A[D]=E.coerce(C)
					except ValueError:pass
			return A
		except:raise ValidationError(_('Not a valid dictionary.'),B)
class JSONProperty(Property):
	def coerce(B,value):
		A=value
		if isinstance(A,str):A=json.loads(A)
		return A
	def validate(B,value):
		A=value;A=super().validate(B.coerce(A))
		if type(A)not in(str,int,float,bool,list,dict,type(_A)):raise ValidationError(_('The value is not JSON serializable.'))
		return A
class ChoiceProperty(Property):
	def __init__(A,description,choices,**B):A.choices=choices;super().__init__(description,**B)
	def validate(B,value):
		A=value
		if isinstance(A,str):
			C=[A.lower()for A in B.choices if isinstance(A,str)]
			if A.lower()in C:return super().validate(A)
		elif A in B.choices or A is _A:return super().validate(A)
		raise ValidationError(_('The value is not one of the valid choices.'),A,B.choices)
	def as_dict(B):A=super().as_dict();A['choices']=B.choices;return A
class DateProperty(Property):
	def __init__(A,description,default_value=_A,minimum=_A,maximum=_A,**B):A.minimum=A.coerce(minimum);A.maximum=A.coerce(maximum);super().__init__(description,default_value,**B)
	def coerce(C,value):
		B='Not a valid date.';A=value
		if isinstance(A,datetime.date):return A
		elif isinstance(A,str):
			try:return datetime.date(*map(int,A.split('-')))
			except Exception:raise ValidationError(_(B),A)
		elif A is _A:return
		raise ValidationError(_(B),A)
	def validate(B,value):
		A=value;A=super().validate(B.coerce(A))
		if A is not _A:
			if B.minimum and A<B.minimum:raise ValidationError(_('The date is less than the minimum allowed.'),A,B.minimum)
			if B.maximum and A>B.maximum:raise ValidationError(_('The date is greater than the maximum allowed.'),A,B.maximum)
		return A
	def as_dict(B):A=super().as_dict();A[_B]=str(B.default_value);A[_C]=str(B.minimum);A[_D]=str(B.maximum);return A
	def __str__(A):return str(A.value)
class TimeProperty(Property):
	def __init__(A,description,default_value=_A,minimum=_A,maximum=_A,**B):A.minimum=A.coerce(minimum);A.maximum=A.coerce(maximum);super().__init__(description,default_value,**B)
	def coerce(C,value):
		B='Not a valid time.';A=value
		if isinstance(A,datetime.time):return A
		elif isinstance(A,str):
			try:return datetime.time(*map(int,A.split(':')))
			except Exception:raise ValidationError(_(B),A)
		elif A is _A:return
		raise ValidationError(_(B),A)
	def validate(B,value):
		A=value;A=super().validate(B.coerce(A))
		if A is not _A:
			if B.minimum and A<B.minimum:raise ValidationError(_('The time is less than the minimum allowed.'),A,B.minimum)
			if B.maximum and A>B.maximum:raise ValidationError(_('The time is greater than the maximum allowed.'),A,B.maximum)
		return A
	def as_dict(B):A=super().as_dict();A[_B]=str(B.default_value);A[_C]=str(B.minimum);A[_D]=str(B.maximum);return A
	def __str__(A):return str(A.value)
class DatetimeProperty(Property):
	def __init__(A,description,default_value=_A,minimum=_A,maximum=_A,**B):A.minimum=A.coerce(minimum);A.maximum=A.coerce(maximum);super().__init__(description,default_value,**B)
	def coerce(E,value):
		B='Not a valid datetime.';A=value
		if isinstance(A,datetime.datetime):return A
		elif isinstance(A,str):
			try:C,D=A.split(' ');return datetime.datetime(*map(int,C.split('-')),*map(int,D.split(':')))
			except Exception:raise ValidationError(_(B),A)
		elif A is _A:return
		raise ValidationError(_(B),A)
	def validate(B,value):
		A=value;A=super().validate(B.coerce(A))
		if A is not _A:
			if B.minimum and A<B.minimum:raise ValidationError(_('The datetime is less than the minimum allowed.'),A,B.minimum)
			if B.maximum and A>B.maximum:raise ValidationError(_('The datetime is greater than the maximum allowed.'),A,B.maximum)
		return A
	def as_dict(B):A=super().as_dict();A[_B]=str(B.default_value);A[_C]=str(B.minimum);A[_D]=str(B.maximum);return A
	def __str__(A):return str(A.value)