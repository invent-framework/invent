import pyscript


async def fetch(url, json=True):
    """
    Fetch a URL and return the JSON result. If json flag is set to False,
    returns a plain string. If the response is not OK, raises a
    ConnectionError.
    """
    response = await pyscript.fetch(url)
    if response.ok:
        if json:
            result = await response.json()
        else:
            result = await response.text()
        return result
    else:
        raise ConnectionError(f"Failed to fetch {url}: {response.status}")
