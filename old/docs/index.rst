.. PyperCard documentation master file, created by
   sphinx-quickstart on Fri Jul 26 17:59:56 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyperCard - Easy GUIs for All
=============================

.. raw:: html

    <img alt="Splash image" src="_static/splash.png" style="border: none;">

PyperCard is a `HyperCard <https://en.wikipedia.org/wiki/HyperCard>`_ inspired
`Pythonic <https://www.python.org/dev/peps/pep-0020/>`_ 
`GUI <https://en.wikipedia.org/wiki/Graphical_user_interface>`_ framework for
beginner programmers.

What does that mean?

PyperCard makes it quick and easy to create software with a modern user
interface to use on your Windows, OSX, Linux, Android or iOS devices.

**The best place to start is by reading the** :doc:`tutorials`. If you want
further support, then please
`join our chat channel <https://gitter.im/pypercard/community>`_. We're a
friendly bunch and welcome questions from beginners. If you're more experienced
check out the :doc:`cheatsheet` for a quick summary of what's going on.

A simple temperature conversion example application built with PyperCard is
shown below. This only took just over
`40 lines of simple Python code <tutorial5.html>`_ 
to create.

.. image:: temperature.gif 

PyperCard was created in response to the work of the wonderful folks at
Adafruit who designed a `simple GUI library <https://learn.adafruit.com/circuit-python-your-own-adventure/overview>`_
for one of their CircuitPython based devices. PyperCard takes Adafruit's
original concept, refines it and makes it available on a large number of
computing platforms. To achieve this, PyperCard currently uses the
`Kivy UI framework <https://kivy.org/>`_ under the hood.

The following video explains the project's genesis:

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
    <iframe width="720" height="405" src="https://www.youtube-nocookie.com/embed/CIUQvp2Pnpk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

PyperCard is **deliberately constrained**. This makes it easy to learn ~ an
important consideration for beginner programmers.

If you find using PyperCard frustrating because you want to break free of the
constraints, then you're probably too advanced for PyperCard and should
graduate to a less constrained GUI framework such as
`PyQT <https://www.riverbankcomputing.com/software/pyqt/intro>`_,
`Toga <https://beeware.org/project/projects/libraries/toga/>`_ or
`Kivy <https://kivy.org/>`_.

.. note::

    **This documentation is for two sorts of readers**.

    1. Folks who want to use PyperCard to build cross platform GUI
    applications. If this is *you*, check out the :doc:`tutorials` first. If
    you're already quite technical, you should see the :doc:`cheatsheet`.

    2. Programmers who want to contribute to the development of PyperCard
    itself. If this is *you*, start with the :doc:`contributing`
    documentation.


Contents:
---------

.. toctree::
   :maxdepth: 2

   tutorials.rst
   cheatsheet.rst
   contributing.rst
   design.rst
   code_of_conduct.rst
   setup.rst
   api.rst
   license.rst

