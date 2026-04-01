_B='    '
_A='children'
from invent.ui.core import from_datastore
from invent.ui import Container
IMPORTS='\nimport invent\nfrom invent.ui import *\nfrom invent.ai import *\n'
INDEX_HTML='\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <title>{title}</title>\n\n    <!-- Recommended meta tags -->\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width,initial-scale=1.0">\n\n    <!-- PyScript -->\n    <link rel="stylesheet"\n      href="https://pyscript.net/releases/2024.7.1/core.css">\n    <script type="module"\n      src="https://pyscript.net/releases/2024.7.1/core.js"></script>\n\n    <!-- App CSS Styles -->\n    <link rel="stylesheet"\n      href="https://unpkg.com/papercss@1.9.2/dist/paper.min.css">\n</head>\n<body>\n  <script type="mpy" src="./main.py" config="./pyscript.toml" async></script>\n</body>\n</html>\n'
MAIN_PY_TEMPLATE='\n{imports}\n\n# Datastore ##################################################################\n\n{datastore}\n\n# Code #######################################################################\n\n{code}\n\n# User Interface #############################################################\n\n{app}\n\n# GO! ########################################################################\n\ninvent.go()\n\n'
PYSCRIPT_TOML_TEMPLATE='\nexperimental_create_proxy = "auto"\n\n[files]\n"https://invent.pyscriptapps-dev.com/invent/latest/invent.zip" = "./*"\n'
def as_pyscript_app(app,imports=IMPORTS,datastore='',code='',to_psdc=True):index_html=INDEX_HTML.format(title=app.name);main_py=MAIN_PY_TEMPLATE.format(imports=imports,datastore=datastore,code=code,app=_pretty_repr_app(app));pyscript_toml=PYSCRIPT_TOML_TEMPLATE.format(invent_src='https://mchilvers.pyscriptapps.com/invent/latest/invent'if to_psdc else'../../src/invent');return index_html,main_py,pyscript_toml
def as_dict(app,imports=IMPORTS,datastore='',code='',to_psdc=True):return dict(imports={},datastore={},blocks={},app=app.as_dict())
def from_dict(bundle_dict):app=_app_from_dict(bundle_dict['app']);return app
def _app_from_dict(app_dict):A='pages';from invent.ui.app import App;pages=[_component_from_dict(component_dict)for component_dict in app_dict[A]];app_dict[A]=pages;return App(**app_dict)
def _component_from_dict(component_dict):
	B='properties';A='type';from invent import ui;cls=getattr(ui,component_dict[A]);properties={}
	for(property_name,property_value)in component_dict[B].items():
		if issubclass(cls,Container)and property_name==_A:continue
		if type(property_value)is str and property_value.startswith('from_datastore('):property_value=eval(property_value,{},dict(from_datastore=from_datastore))
		properties[property_name]=property_value
	cls=getattr(ui,component_dict[A])
	if issubclass(cls,Container):
		property_value=component_dict[B][_A]
		if type(property_value)is str:children=eval(property_value,{},dict(from_datastore=from_datastore))
		else:children=[_component_from_dict(component_dict)for component_dict in property_value]
		properties[_A]=children
	return cls(**properties)
APP_TEMPLATE="\nApp(\n    name='{name}',\n    children=[\n{pages}\n    ],\n)\n"
def _pretty_repr_app(app):return APP_TEMPLATE.format(name=app.name,pages=_pretty_repr_pages(app.pages))
def _pretty_repr_pages(pages):
	lines=[]
	for page in pages:_pretty_repr_component(page,lines=lines,indent=' '*8)
	return'\n'.join(lines)
def _pretty_repr_component(component,lines,indent=''):
	lines.append(f"{indent}{type(component).__name__}(");_pretty_repr_component_properties(component,lines,indent+_B);_pretty_repr_component_layout(component.layout,lines,indent+_B)
	if isinstance(component,Container):_pretty_repr_container_children_property(component,lines,indent+_B)
	lines.append(f"{indent}),")
def _pretty_repr_component_properties(component,lines,indent):
	for(property_name,property_obj)in sorted(component.properties().items()):
		if isinstance(component,Container)and property_name==_A:continue
		from_datastore=component.get_from_datastore(property_name);property_value=from_datastore if from_datastore else getattr(component,property_name);lines.append(f"{indent}{property_name}={repr(property_value)},")
def _pretty_repr_component_layout(layout,lines,indent):
	layout_dict=layout if isinstance(layout,dict)else layout.as_dict()
	if layout_dict:dict_args=[f"{key}={value!r}"for(key,value)in sorted(layout_dict.items())];lines.append(f"{indent}layout=dict({", ".join(dict_args)}),")
def _pretty_repr_container_children_property(component,lines,indent):
	from_datastore=component.get_from_datastore(_A)
	if from_datastore:lines.append(f"{indent}children={repr(from_datastore)},")
	else:
		lines.append(f"{indent}children=[")
		for child in component.children:_pretty_repr_component(child,lines=lines,indent=indent+_B)
		lines.append(f"{indent}],")