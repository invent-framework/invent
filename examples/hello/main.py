"""
The simplest possible app. It says, "Hello, World!".
"""
from pypercard import App, Card

# Create an app, with a single "hello" card.
app = App(
    cards=[
        # The card is named "hello", and will display the template's content.
        Card(name="hello", template="Hello, world!"),
    ],
)
# Start the app with the "hello" card.
app.start("hello")
