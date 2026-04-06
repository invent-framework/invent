from invent.i18n import _
from pyscript.web import div,table,caption,thead,tbody,tr,th,td
from invent.ui.core import Widget,ListProperty,TextProperty,BooleanProperty
class Table(Widget):
	data=ListProperty(_('The text/numeric data to display in the table.'),default_value=[['Header 1','Header 2'],['Row 1, Cell 1','Row 1, Cell 2'],['Row 2, Cell 1','Row 2, Cell 2']]);label=TextProperty(_('An optional label for the table.'),default_value='');column_headers=BooleanProperty(_('A flag to indicate if the first row of the table is a header row.'),default_value=True,group='style');row_headers=BooleanProperty(_('A flag to indicate if the first item in each row is a header.'),default_value=False,group='style')
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M224 48H32a8 8 0 0 0-8 8v136a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a8 8 0 0 0-8-8M40 112h40v32H40Zm56 0h120v32H96Zm120-48v32H40V64ZM40 160h40v32H40Zm176 32H96v-32h120z"/></svg>'
	def _tabulate(A):
		A._table_head._dom_element.replaceChildren();A._table_body._dom_element.replaceChildren()
		if A.data:
			B=A.data[:]
			if A.column_headers:A._table_head.append(tr(*[th(A)for A in B[0]]));B=B[1:]
			if A.row_headers:A._table_body.append([tr(th(A[0]),*[td(A)for A in A[1:]])for A in B])
			else:A._table_body.append([tr(*[td(A)for A in A])for A in B])
	def on_data_changed(A):A._tabulate()
	def on_column_headers_changed(A):A._tabulate()
	def on_row_headers_changed(A):A._tabulate()
	def on_label_changed(A):A._caption.innerText=A.label
	def render(A):A._caption=caption(A.label);A._table_head=thead();A._table_body=tbody();return div(table(A._caption,A._table_head,A._table_body,id=A.id),style={'overflow-x':'auto','max-width':'100%'})