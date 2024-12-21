import invent
import upytest
import umock


# An alternative way to discern the Python interpreter.
interpreter = "unknown"
try:
    from platform import python_implementation

    interpreter = python_implementation().lower()
except ImportError:
    interpreter = "micropython"


@upytest.skip(
    "Only works on MicroPython", skip_when=interpreter != "micropython"
)
def test_is_micropython_true():
    assert invent.is_micropython is True, "Interpreter is not MicroPython"


@upytest.skip("Only runs on Pyodide", skip_when=interpreter == "micropython")
def test_is_micropython_false():
    assert invent.is_micropython is False, "Interpreter is not Pyodide"


def test_show_page():
    page_name = "test_page"
    with umock.patch("invent.utils:App") as mockApp:
        invent.show_page(page_name)
        mockApp.app().show_page.assert_called_once_with(page_name)


def test_getmembers_static():
    """
    Test that getmembers_static returns the expected members of a class.
    """

    class TestClass:
        foo = 1
        bar = 2

        def __init__(self):
            pass

        def baz(self):
            pass

    expected = [
        ("foo", 1),
        ("bar", 2),
        ("__init__", TestClass.__init__),
        ("baz", TestClass.baz),
    ]
    actual = invent.utils.getmembers_static(TestClass)
    for member in expected:
        assert (
            member in actual
        ), f"Expected member {member} not found in {actual}"


def test_iscoroutinefunction():
    """
    Test that iscoroutinefunction returns True for a coroutine function.
    """

    async def coro():
        pass

    assert (
        invent.utils.iscoroutinefunction(coro) is True
    ), "Coroutine function not recognized"


def test_iscoroutinefunction_with_closure():
    """
    Test that iscoroutinefunction returns True for a coroutine function
    as a closure.
    """
    x = 1

    async def coro():
        return x + 1

    assert (
        invent.utils.iscoroutinefunction(coro) is True
    ), "Coroutine function as closure not recognized"


def test_iscoroutinefunction_false():
    """
    Test that iscoroutinefunction returns False for a non-coroutine function.
    """

    def func():
        pass

    assert (
        invent.utils.iscoroutinefunction(func) is False
    ), "Non-coroutine function recognized as coroutine"


def test_capitalize():
    """
    Test that capitalize capitalizes the first letter of a string.
    """
    assert (
        invent.utils.capitalize("hello") == "Hello"
    ), "String not capitalized"


def test_sanitize():
    """
    Test that sanitize returns an HTML safe version of a string.
    """
    raw = "<script>alert('xss');</script>"
    expected = "&lt;script&gt;alert('xss');&lt;/script&gt;"
    assert invent.utils.sanitize(raw) == expected, "String not sanitized"
