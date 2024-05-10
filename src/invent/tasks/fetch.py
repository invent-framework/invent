import invent
import pyscript


async def fetch(task, url, json=True):
    """
    Fetch a URL and return the JSON result. If json flag is set to False,
    returns a plain string. The indicator argument should contain the name of
    a datastore key to act as a flag to indicate the task is in flight.
    """
    if task.indicator:
        invent.datastore[task.indicator] = True

    response = await pyscript.fetch(url)
    if task.indicator:
        invent.datastore[task.indicator] = False
    if response.ok:
        if json:
            result = await response.json()
        else:
            result = await response.text()
        return result
    else:
        raise RuntimeError
