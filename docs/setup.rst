Developer Setup
===============

The source code is hosted on GitHub. Fork the repository with the following
command::

  git clone https://github.com/ntoll/pypercard.git

**PyperCard does not and never will use or support Python 2**. You should use
Python 3.6 or above.

Windows, OSX, Linux
+++++++++++++++++++

Create a virtual environment via your command line::

    python3 -mvenv pypercardenv

Activate it::

    # Unix-y
    source pypercardenv/bin/activate

    # Windows
    pypercardenv\Scripts\activate

The name ``pypercard`` should appear at the start of each line of your command
line, to show you're in the active virtualenv.

Ensure you have the latest version of ``pip`` installed::

    pip install --upgrade pip

Install all the dependencies for PyperCard with::

    pip install -e ".[dev]"

Everything should be working if you can successfully run::

  make check

(You'll see the results from various code quality tools, the test suite and
code coverage.)

.. note::

    The PyperCard package distribution, as specified in ``setup.py``, declares
    both runtime and extra dependencies.

    The above mentioned ``pip install -e ".[dev]"`` installs all runtime
    dependencies and most development ones: it should serve nearly everyone.

    For the sake of completeness, however, here are a few additional details.
    The ``[dev]`` extra is actually the aggregation of the following extras:

    * ``[tests]`` specifies the testing dependencies, needed by ``make test``.
    * ``[docs]`` specifies the doc building dependencies, needed by ``make docs``.

    Addionionally, the following extras are defined:

    * ``[all]`` includes all the dependencies in all extras.


.. warning::

    Using a virtualenv will ensure your development environment is safely
    isolated from problematic version conflicts with your system wide version
    of Python.

    If you get into trouble, delete the virtualenv's directory (that's
    ``pypercardenv`` in the instructions above) and start again with a fresh
    install. The virtualenv is best thought of as a disposable sandbox in which
    you can safely do your development work on PyperCard.

Using ``make``
++++++++++++++

There is a Makefile that helps with most of the common workflows associated
with development. Typing ``make`` on its own will list the options thus::

    $ make

    There is no default Makefile target right now. Try:

    make clean - reset the project and remove auto-generated assets.
    make pyflakes - run the PyFlakes code checker.
    make pycodestyle - run the PEP8 style checker.
    make test - run the test suite.
    make coverage - view a report on test coverage.
    make tidy - tidy code with the 'black' formatter.
    make check - run all the checkers and tests.
    make dist - make a dist/wheel for the project.
    make publish-test - publish the project to PyPI test instance.
    make publish-live - publish the project to PyPI production.
    make docs - run sphinx to create project documentation.

.. note::

    On Windows there is a ``make.cmd`` file that works in a similar way to the
    ``make`` command on Unix-like operating systems.

Before Submitting
+++++++++++++++++

Before contributing code please make sure you've read :doc:`contributing` and
follow the checklist for contributing changes. We expect everyone participating
in the development of PyperCard to act in accordance with the PSF's
:doc:`code_of_conduct`.
