# Getting PyperCard

PyperCard uses [PyScript](https://pyscript.com/), a browser based Python
platform.

It means that getting PyperCard is simply an addition to some HTML.

This ensures PyperCard is installed as a module in your browser-based Python
environment.

That's it!

## The simple way

The simplest way to build an app with PyperCard is to use
[pyscript.com](https://pyscript.com).

If you don't already have an account, it's possible to start using
[PyScript.com](https://pyscript.com) to create your Python projects with a free
but limited account. Once you've signed up and logged in, create a new project
and ensure PyperCard is referenced in the new project's `pyscript.toml` file
(used by PyScript to configure your project).

```toml
packages = ["pypercard", ]
```

Your new project's `main.py` file will contain your application’s Python code,
and the project's `index.html` file may contain HTML that defines how your
application will look (more on this later).

You're good to skip the next section and go [check your app works](#checking-the-app).

## The detailed way

If you're interested in the "under the hood" details, read on.

This section assumes you've referenced PyScript in the `<head>` of your HTML.

```HTML
<script defer src="https://pyscript.net/latest/pyscript.js"></script>
```

The `<py-config>...</py-config>` tag is how you configure your PyScript Python
environent.

This can be as simple as adding the following into the `<body>` of your HTML
document:

```HTML
<py-config>
packages = ["pypercard", ]
</py-config>
```

Alternatively, you could copy what PyScript.com does by default, and just
reference a separate `pyscript.toml` file:

```HTML
<py-config src="./pyscript.toml"></py-config>
```

In exactly the same way as the in-line `<py-config>` content, your TOML file
should include `pypercard` in the `packages`:

```TOML
packages = ["pypercard", ]
```

The source code for your PyperCard app could be written within a
`<py-script> ... </py-script>` tag within your HTML. However, a cleaner way to
write your code is to include it in a separate Python file and reference that
as the `src` of the `<py-script>` tag (as PyScript.com does):

```HTML
<py-script src="./main.py"></py-script>
```

That's it!

## Checking the app 

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
app.start()
```

If you can see "Hello, World!" in your preview window on PyScript.com or the
same is shown when you point your browser to your HTML file on the
local filesystem, then PyperCard works and is ready to go.
