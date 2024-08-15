import invent
import umock


async def test_go():
    """
    Ensure the convenience "go" function starts the singleton app.
    """
    mockApp = umock.Mock()
    mockApp.app = umock.Mock()
    with umock.patch("invent:App") as mockApp:
        await invent.go()
        mockApp.app().go.assert_called_once()
