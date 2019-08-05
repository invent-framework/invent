# PyperCard - A Pythonic HyperCard for Beginner Programmers

A re-implementation of
[Adafruit's CircuitPython PYOA](https://github.com/adafruit/Adafruit_CircuitPython_PYOA)
module for non-CircuitPython computing environments. This module re-uses the
JSON specification used to create HyperCard like "stacks" of states between
which users transition in a choose-your-own-adventure style.

## Developer Setup

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
pip install -e ".[dev]"
```

Run the test suite:

```
make check
```

Try out some of the examples in the "examples" subdirectory (see the README
therein for more information).

## ToDo

* Packaging for mobile (Android and iOS).
