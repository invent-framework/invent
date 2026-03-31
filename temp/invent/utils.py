import inspect,sys
from pyscript.web import div,page,link,style
from.app import App
from.i18n import _
is_micropython='micropython'in sys.version.lower()
WEEKDAYS=_('Mon'),_('Tue'),_('Wed'),_('Thu'),_('Fri'),_('Sat'),_('Sun')
MONTHS=_('Jan'),_('Feb'),_('Mar'),_('Apr'),_('May'),_('Jun'),_('Jul'),_('Aug'),_('Sep'),_('Oct'),_('Nov'),_('Dec')
def show_page(page_id):App.app().show_page(page_id)
def getmembers_static(cls):
	A=cls
	if is_micropython:return[(B,getattr(A,B))for(B,C)in inspect.getmembers(A)]
	return inspect.getmembers_static(A)
def iscoroutinefunction(obj):
	A=obj
	if is_micropython:
		B=repr(A)
		if'<closure <generator>'in B:return True
		if'<bound_method'in B and'<generator>'in B:return True
		return inspect.isgeneratorfunction(A)
	return inspect.iscoroutinefunction(A)
def capitalize(s):return s[0].upper()+s[1:].lower()
def sanitize(raw):A=div();A.innerText=raw;return A.innerHTML
def from_markdown(raw_markdown):
	A=raw_markdown;B=A;from.import marked as C,purify as D
	if C:B=D.default().sanitize(C.parse(A))
	return B
def _hex_to_rgb(hex_colour):A=hex_colour.lstrip('#');return int(A[0:2],16),int(A[2:4],16),int(A[4:6],16)
def _linearise(channel):
	A=channel/255
	if A<=.04045:return A/12.92
	return((A+.055)/1.055)**2.4
def _luminance(r,g,b):return .2126*_linearise(r)+.7152*_linearise(g)+.0722*_linearise(b)
def _rgb_to_hsl(r,g,b):
	r,g,b=r/255,g/255,b/255;A=max(r,g,b);B=min(r,g,b);D=(A+B)/2
	if A==B:return 0,0,D
	C=A-B;F=C/(2-A-B)if D>.5 else C/(A+B)
	if A==r:E=(g-b)/C+(6 if g<b else 0)
	elif A==g:E=(b-r)/C+2
	else:E=(r-g)/C+4
	return E*60,F,D
def _hue_to_rgb(p,q,t):
	if t<0:t+=1
	if t>1:t-=1
	if t<1/6:return p+(q-p)*6*t
	if t<1/2:return q
	if t<2/3:return p+(q-p)*(2/3-t)*6
	return p
def _hsl_to_hex(h,s,l):
	if s==0:B=int(l*255);return f"#{B:02x}{B:02x}{B:02x}"
	A=l*(1+s)if l<.5 else l+s-l*s;C=2*l-A;D=h/360;E=_hue_to_rgb(C,A,D+1/3);F=_hue_to_rgb(C,A,D);G=_hue_to_rgb(C,A,D-1/3);return f"#{int(E*255):02x}{int(F*255):02x}{int(G*255):02x}"
def contrast_colours(hex_bg):
	H='link';G='text';B,C,D=_hex_to_rgb(hex_bg);I=_luminance(B,C,D);J=I<=.179;A,E,K=_rgb_to_hsl(B,C,D)
	if E<.1:A=210
	F=max(E,.55)
	if J:return{G:'#f0f0f0',H:_hsl_to_hex(A,F,.85)}
	return{G:'#1a1a1a',H:_hsl_to_hex(A,F,.25)}
def humanise_timestamp(dt):A=dt;B=WEEKDAYS[A.weekday()];C=MONTHS[A.month-1];D='AM'if A.hour<12 else'PM';E=A.hour%12 or 12;return f"{B} {A.day:02d} {C} {A.year}, {E}:{A.minute:02d} {D}"
def set_theme(theme):
	C='invent-theme';B=theme;D=page.find('#loader')
	for A in D:A.remove()
	E=page.find('#invent-theme')
	for A in E:A.remove()
	try:
		with open(f"./invent/themes/{B}",'r')as F:G=F.read()
		page.head.append(style(G,id=C))
	except OSError:page.head.append(link(rel='stylesheet',href=B,id=C))