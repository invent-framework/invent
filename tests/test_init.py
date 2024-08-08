import invent
import pytest
from unittest import mock


@pytest.mark.asyncio
async def test_go():
    """
    Ensure the convenience "go" function starts the singleton app.
    """
    with mock.patch("invent.App") as mockApp:
        await invent.go()
        mockApp.app().go.assert_called_once_with()
