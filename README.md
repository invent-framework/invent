# PyperCard - A Pythonic HyperCard for Beginner Programmers

This project's documentation can be found [here](https://pypercard.rtfd.io).

This started, in 2019, as a re-implementation of 
[Adafruit's CircuitPython PYOA](https://github.com/adafruit/Adafruit_CircuitPython_PYOA)
module, but for non-CircuitPython computing environments. It was originally
written using the [Kivy](https://kivy.org/) framework for cross-platform
development. After successfully using PyperCard for teaching purposes,
development stalled because of the COVID pandemic.

However, PyperCard is back in active development _with some significant
changes_:

* [PyScript](https://pyscript.net/) replaces Kivy as the underlying framework
  for generating and running the user interface.
* [Nicholas](https://github.com/ntoll), the original core developer of
  PyperCard, has been hired by [Anaconda Inc](https://anaconda.com/) to work
  on PyScript, and so his work on this project is sponsored by his employer
  (hence some of the copyright changes).
* Ownership of the repository will be transferred to the
  [pyscript organisation](https://github.com/pyscript) on GitHub (the old
  repository will automatically redirect to the new one).
* Since this is a complete rewrite, the license has been changed from MIT
  to Apache2.

All the assets relating to the old version of the project can still be found
in the `old` directory in this repository.

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
make serve - serve the project at: http://0.0.0.0:8000/
make test - while serving the app, run the test suite in browser.
```

To run the test suite:

```
$ make serve
```

Then visit
[http://localhost:8000/tests.html](http://localhost:8000/tests.html) or, in
another console with the code still serving, `make test`.

The tests should open in your browser, and pass. ;-)

## Example applications

Several example applications, demonstrating various different aspects of
PyperCard can be found in the `examples` subdirectory of this repository.

They are, in order of complexity (simple first):

* `hello` - a very simple and raw "hello" application that prompts users to
  enter their name, and click a button for a friendly greeting.
