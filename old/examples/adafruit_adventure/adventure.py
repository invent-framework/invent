from pypercard import CardApp


app = CardApp("Adafruit Adventure")
app.load("cyoa.json")
app.run()
