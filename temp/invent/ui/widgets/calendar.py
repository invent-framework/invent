_B='events'
_A='click'
from invent.i18n import _
from invent.ui.core import Widget,DictProperty,IntegerProperty,Event
from datetime import date,datetime,timedelta
from pyscript import web
from pyscript.ffi import create_proxy
MONTH_NAMES=['',_('January'),_('February'),_('March'),_('April'),_('May'),_('June'),_('July'),_('August'),_('September'),_('October'),_('November'),_('December')]
_DAY_NAMES=[_('Mon'),_('Tue'),_('Wed'),_('Thu'),_('Fri'),_('Sat'),_('Sun')]
class Calendar(Widget):
	MONDAY=0;TUESDAY=1;WEDNESDAY=2;THURSDAY=3;FRIDAY=4;SATURDAY=5;SUNDAY=6;year=IntegerProperty(_('The year to display.'),default_value=date.today().year);month=IntegerProperty(_('The month to display (1=January, 2=February, ..., 12=December).'),default_value=date.today().month);appointments=DictProperty(_('A dictionary of individual appointments to be displayed on the calendar. The keys should be ISO datetime strings, and the values should be content to display.'),default_value={});first_day_of_week=IntegerProperty(_('The first day of the week. 0=Monday, 1=Tuesday, ..., 6=Sunday.'),default_value=MONDAY);event_clicked=Event(_('Triggered when a calendar event is clicked.'),date=_('The date of the event.'),time=_('The time of the event.'),content=_('The content of the event.'));date_clicked=Event(_('Triggered when a date is clicked.'),date=_('The date that was clicked.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Zm-68-76a12,12,0,1,1-12-12A12,12,0,0,1,140,132Zm44,0a12,12,0,1,1-12-12A12,12,0,0,1,184,132ZM96,172a12,12,0,1,1-12-12A12,12,0,0,1,96,172Zm44,0a12,12,0,1,1-12-12A12,12,0,0,1,140,172Zm44,0a12,12,0,1,1-12-12A12,12,0,0,1,184,172Z"></path></svg>'
	def _days_in_month(C,year,month):
		A=month
		if A==12:B=date(year+1,1,1)
		else:B=date(year,A+1,1)
		return(B-timedelta(days=1)).day
	def _day_names(B,first_weekday=MONDAY):A=first_weekday;return _DAY_NAMES[A:]+_DAY_NAMES[:A]
	def _group_by_date(F,events):
		A={}
		for(C,D)in events.items():B=datetime.fromisoformat(C);A.setdefault(B.date(),[]).append(((B.hour,B.minute),D))
		for E in A:A[E].sort()
		return A
	def calendar_weeks(E,year,month,events,first_weekday=MONDAY):
		C=month;B=year;G=E._group_by_date(events);H=(date(B,C,1).weekday()-first_weekday)%7;D=[];A=[None]*H
		for I in range(1,E._days_in_month(B,C)+1):
			F=date(B,C,I);A.append({'date':F,_B:G.get(F,[])})
			if len(A)==7:D.append(A);A=[]
		if A:D.append(A+[None]*(7-len(A)))
		return D
	def _format_time(C,hm):
		A,B=hm
		if A==0 and B==0:return'All day'
		return f"{A:02d}:{B:02d}"
	def _day_cell(A,cell,today):
		B=cell['date'];C=cell[_B];D=['calendar-day']
		if C:D.append('has-events')
		if B==today:D.append('calendar-today')
		E=web.div(web.span(str(B.day),classes=['calendar-day-num']));E.addEventListener(_A,create_proxy(lambda e,date=B:A.publish(A.date_clicked,date=date)))
		if C:
			F=[]
			for(G,H)in C:I=web.li(web.time(A._format_time(G)),f" {H}");I.addEventListener(_A,create_proxy(lambda e,hm=G,description=H:A.publish(A.event_clicked,date=B,time=hm,content=description)));F.append(I)
			E.append(web.ul(*F,classes=['calendar-events']))
		return web.td(E,classes=D)
	def render_table(A,*L,**M):
		E=date.today();F=MONTH_NAMES[A.month];G=A.calendar_weeks(A.year,A.month,A.appointments,A.first_day_of_week);H=web.tr(*[web.th(A)for A in A._day_names(A.first_day_of_week)]);I=web.nav(A.previous_button,web.h2(f"{F} {A.year}"),A.next_button,classes=['invent-calendar-nav']);C=[]
		for J in G:
			B=[]
			for D in J:
				if D is None:B.append(web.td(classes=['calendar-empty']))
				else:B.append(A._day_cell(D,E))
			C.append(web.tr(*B))
		K=web.table(web.thead(H),web.tbody(*C));A.element.replaceChildren();A.element.append(I);A.element.append(K)
	on_appointments_changed=render_table;on_year_changed=render_table;on_month_changed=render_table;on_first_day_of_week_changed=render_table
	def previous(A,event):
		if A.month==1:A.month=12;A.year-=1
		else:A.month-=1
	def next(A,event):
		if A.month==12:A.month=1;A.year+=1
		else:A.month+=1
	def render(A):A.previous_button=web.button('‹',classes=['calendar-prev']);A.previous_button.addEventListener(_A,create_proxy(A.previous));A.next_button=web.button('›',classes=['calendar-next']);A.next_button.addEventListener(_A,create_proxy(A.next));return web.div(classes=['invent-calendar'])