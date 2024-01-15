import pytest
from pyscript import document, window
from invent.pubsub import _pubsub


@pytest.fixture(autouse=True)
def before_tests():
    """
    Ensure browser storage is always reset to empty. Remove the app
    placeholder. Reset the page title.
    """
    _pubsub.clear()
    window.localStorage.clear()
    test_placeholder = document.querySelector("test-app")
    if test_placeholder:
        test_placeholder.remove()
