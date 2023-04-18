"""
The simplest possible app. It displays, "Hello, World!".
"""
from pypercard import App, Card

# Create an app, with a single "hello" card.
app = App(
    cards=[
        # The card is named "hello", and will display the template's content.
        Card(name="hello", template="Hello, world!"),
    ],
)
# Start the app.
app.start()
