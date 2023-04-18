# Getting PyperCard

The simplest way to build an app with PyperCard is to use
[pyscript.com](https://pyscript.com) (we'll cover further options later on).

## PyScript.com

If you don't already have an account, it's possible to start using
[PyScript.com](https://pyscript.com) to create your Python projects with a free
but limited account. Once you've signed up and logged in, create a new project
and ensure PyperCard is referenced in the new project's `pyscript.toml` file
(used by PyScript to configure your project).

This is simply done by adding `pypercard` to the list of `packages` your app
needs, like this:

```python
packages = ["pypercard", ]
```

The `main.py` file will contain your application's Python code, and the
`index.html` file _may_ contain HTML that defines how your application will
look.

## Standard Python

If you're happy using 

## Checking the installation

A simple "hello world" application is sufficient to check that everything is
working. Assuming the default settings and project layout, as described above,
then your `main.py` file should look like this:

```python
"""
The simplest possible app. It displays, "Hello, World!".
"""
from pypercard import App, Card

# Create an app, with a single "hello" card.
app = App(
    cards=[
        Card(name="hello", template="Hello, world!"),
    ],
)
# Start the app.
app.start()
```

If you can see "Hello, World!" in your preview window on PyScript.com or the
same is shown when you point your browser to your `index.html` file on the
local filesystem, then PyperCard works and is ready to go.
