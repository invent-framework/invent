# PyperCard - A Pythonic HyperCard for Beginner Programmers

View this repository [via GitHub pages](https://pyscript.github.io/pypercard/).

This project's documentation can be found [here](https://pypercard.rtfd.io).

This project started in 2019 as a re-implementation of 
[Adafruit's CircuitPython PYOA](https://github.com/adafruit/Adafruit_CircuitPython_PYOA)
module, but for non-CircuitPython computing environments. It was originally
written using the [Kivy](https://kivy.org/) framework for cross-platform
development. After successfully testing PyperCard for teaching and learning
purposes with the wonderful
[young folk](https://youngcodersmeetup.wixsite.com/ycm-uk) at the London
[Young Coders' Meetup](https://twitter.com/YCM_UK), development stalled because
of the COVID pandemic.

However, PyperCard is back in active development _with some significant
changes_:

* [PyScript](https://pyscript.net/) replaces Kivy as the underlying
  cross-platform framework for generating and running the user interface.
* [Nicholas](https://github.com/ntoll), the original developer and maintainer
  of PyperCard, has been hired by [Anaconda Inc](https://anaconda.com/) to work
  on PyScript, and so his work on this project is sponsored by his employer
  (hence the copyright changes).
* Ownership of the repository has been transferred to the
  [pyscript organisation](https://github.com/pyscript) on GitHub (the old
  repository will automatically redirect to the new one).
* Since this is a complete rewrite, the license has been changed from MIT
  to Apache2.

All the assets relating to the old version of the project can still be found
in the [old branch](https://github.com/pyscript/pypercard/tree/old) in this
repository.

## Developer setup

Git clone the repository:

```
git clone https://github.com/ntoll/pypercard.git
```

(Recommended) Upgrade local pip:

```
pip install --upgrade pip
```

Make a virtualenv, then install the requirements:

```
pip install -r requirements.txt
```

Most useful developer related tasks are automated by a `Makefile`:

```
$ make
There's no default Makefile target right now. Try:

make clean - reset the project and remove auto-generated assets.
make tidy - tidy up the code with the 'black' formatter.
make lint - check the code for obvious errors with flake8.
make lint-all - check all code for obvious errors with flake8.
make serve - serve the project at: http://0.0.0.0:8000/
make test - while serving the app, run the test suite in browser.
make docs - use Sphinx to create project documentation.
make dist - build the module as a package.
make publish-test - upload the package to the PyPI test instance.
make publish-live - upload the package to the PyPI LIVE instance.
```

To run the test suite:

```
$ make serve
```

Then visit
[http://localhost:8000/](http://localhost:8000/) and click the "Run the test
suite" button, or, in another console with the code still serving, `make test`.

The tests should open in your browser, and pass. ;-)

**Please use a width of 79 characters for source code files.**

## Example applications

Several example applications, demonstrating various different aspects of
PyperCard can be found in the `examples` subdirectory of this repository.

They are, in order of complexity (simple first):

* [hello](https://pyscript.github.io/pypercard/examples/hello/) - it displays "Hello, world!" with PyperCard.
* [hello interactive](https://pyscript.github.io/pypercard/examples/hello_interactive/) - a simple interactive application that prompts users to
  enter their name, and click a button for a friendly greeting.
* [temperatures](https://pyscript.github.io/pypercard/examples/temperature/) - convert between celsius and fahrenheit, whilst handling
  errors.
* [card carousel](https://pyscript.github.io/pypercard/examples/card_carousel/) - a demonstration of automatic advance to the next card
  after N seconds.
* [loosey goosey](https://pyscript.github.io/pypercard/examples/loosey_goosey/) - a goose based honking-as-a-service application to
  demonstrate PyperCard's audio capabilities.
* [turner](https://pyscript.github.io/pypercard/examples/turner/) - use the background properties of cards to display full screen
  images of some of Turner's paintings, to the music of Bach.
* [calculator]() - a simple calculator demonstrating a recursive single card
  app.
* [alchemyst](https://pyscript.github.io/pypercard/examples/alchemyst/) - an atmospheric point and click adventure game in the style of
  the classic Myst (built using the original HyperCard).
