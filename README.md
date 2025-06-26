# Invent - an app framework for beginners

View this repository
[via GitHub pages](https://invent-framework.github.io/invent/).

This project's documentation can be found
[here](https://invent-framework.rtfd.io).

This project started in 2019 as "PyperCard" ~ a re-implementation of 
[Adafruit's CircuitPython PYOA](https://github.com/adafruit/Adafruit_CircuitPython_PYOA)
module, but for non-CircuitPython computing environments. It was originally
written using the [Kivy](https://kivy.org/) framework for cross-platform
development. After successfully testing PyperCard for teaching and learning
purposes with the wonderful
[young folk](https://youngcodersmeetup.wixsite.com/ycm-uk) at the London
[Young Coders' Meetup](https://twitter.com/YCM_UK), development stalled because
of the COVID pandemic.

The project name has since been changed to "Invent" to remove any HyperCard
related expectations. There are further significant changes:

* [PyScript](https://pyscript.net/) replaces Kivy as the underlying
  cross-platform framework for generating and running the user interface.
* [Nicholas](https://github.com/ntoll), the original developer and maintainer
  of Invent/PyperCard, has been hired by [Anaconda Inc](https://anaconda.com/)
  to work on PyScript, and so his work on this project is sponsored by his
  employer.
* Ownership of the repository has been transferred to the
  [invent framework organisation](https://github.com/invent-framework) on
  GitHub (the old repository will automatically redirect to the new one).
* Since this is a complete rewrite, the license has been changed from MIT
  to Apache2.

All the assets relating to the old version of the project can still be found
in the [old branch](https://github.com/invent-framework/invent/tree/old) in this
repository.

## Developer setup

Git clone the repository:

```
git clone https://github.com/invent-framework/invent.git
```

(Recommended) Upgrade local pip:

```
pip install --upgrade pip
```

Make a virtualenv, then install the requirements:

```
pip install -r requirements.txt
```

Most useful developer related tasks are automated by a `Makefile`. Type `make`
for a list of the available commands.

To run the test suite:

```
$ make serve
```

Then visit [http://localhost:8000/](http://localhost:8000/).

The tests should open in your browser, and pass. ;-)

**Please use a width of 79 characters for source code files.**

## Example applications

Coming soon...

## Supporters

Invent is an independent open source project.

However, its core contributors are currently employed by Anaconda to work on
PyScript and Invent. We would like to acknowledge and celebrate Anaconda's
continued support of this project. Thank you [Anaconda Inc](https://anaconda.com/)!
