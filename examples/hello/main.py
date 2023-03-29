"""
The simplest possible app. It says, "Hello, World!".
"""
from pypercard import App, Card

# Create an app, called "Hello", with a single "hello" card.
app = App(
    # The optional name of the app become's the page title, in the browser.
    name="Hello",
    # The optional card_list contains the initial stack of cards.
    card_list=[
        # The card is named "hello", and will display the template's content.
        Card(name="hello", template="Hello, world!"),
    ],
)
# Start the app with the "hello" card.
app.start("hello")
