import invent
from unittest import mock


def test_go():
    """
    Ensure the convenience "go" function starts the singleton app.
    """
    with mock.patch("invent.App") as mockApp:
        invent.go()
        mockApp.app().go.assert_called_once_with()
