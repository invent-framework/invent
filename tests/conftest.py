from pyscript.web import page

import invent
import invent.app
import invent.ui
from invent.channels import _channels


async def setup():
    """
    Ensure the datastore is always reset to empty. Clear all the channels.
    Remove the app placeholder from the page. Nullify the singleton instance of
    the App class and reset the media root. Reset counters for required
    Component based classes.
    """
    if invent.datastore is None:
        await invent.start_datastore()
    invent.datastore.clear()
    await invent.datastore.sync()
    _channels.clear()
    test_placeholder = page.find("test-app")
    if test_placeholder:
        test_placeholder.remove()
    invent.app.__app__ = None
    invent.set_media_root(".")
    invent.ui.Page._counter = 0
