"""
This script simply shows all the known core widgets to aid eyeball mk.1 testing
of them.
"""
import invent
from pyscript import document, display


app = invent.ui.App(name="Widget Zoo")
p = invent.ui.Page()
app.content.append(p)

for name, component in invent.ui.AVAILABLE_COMPONENTS.items():
    c = component()
    p.append(c)

invent.go()
