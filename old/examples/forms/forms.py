from pypercard import Inputs, Card, CardApp


cards = [
    Card(
        "TextBox",
        form=Inputs.TEXTBOX,
        text="A single line textbox",
        buttons=[{"label": "Next", "target": "TextArea"}],
    ),
    Card(
        "TextArea",
        form=Inputs.TEXTAREA,
        text="A multi line text area",
        buttons=[{"label": "Next", "target": "MultiChoice"}],
    ),
    Card(
        "MultiChoice",
        form=Inputs.MULTICHOICE,
        options=["Ham", "Eggs", "Bacon", "Sausage"],
        text="A multiple choice selection",
        buttons=[{"label": "Next", "target": "Select"}],
    ),
    Card(
        "Select",
        form=Inputs.SELECT,
        options=["Red", "Green", "Yellow", "Blue"],
        text="A single choice collection",
        buttons=[{"label": "Next", "target": "Slider"}],
    ),
    Card(
        "Slider",
        form=Inputs.SLIDER,
        options=(-100, 100, 10),
        text="A slider with min/max/step",
        buttons=[{"label": "Next", "target": "TextBox"}],
    ),
]

app = CardApp("Examples of form elements...")
for card in cards:
    app.add_card(card)
app.run()
