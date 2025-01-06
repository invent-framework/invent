import asyncio
import invent
import json
from invent import tasks


async def test_simple_get_with_json_response():
    """
    A simple GET request that returns JSON, results in the expected JSON in the
    datastore at the specified key.
    """
    url = "https://www.swapi.tech/api/people/1"  # Luke Skywalker ;-)
    result_key = "skywalker_info"
    got_result_from_website = asyncio.Event()  # Used to wait for the result.

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    tasks.WebRequest(result_key).go(url, json=True)

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore."
    assert (
        invent.datastore[result_key]["result"]["properties"]["name"]
        == "Luke Skywalker"
    ), "Task result not stored in datastore."


async def test_simple_get_with_text_response():
    """
    A simple GET request that returns text, results in the expected text in the
    datastore at the specified key.
    """
    url = "https://www.swapi.tech/api/people/1"  # Luke Skywalker ;-)
    result_key = "skywalker_info"
    got_result_from_website = asyncio.Event()  # Used to wait for the result.

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    tasks.WebRequest(result_key).go(url)

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore"
    # The response is just a text string (but containing JSON).
    assert isinstance(
        invent.datastore[result_key], str
    ), "Task result not stored in datastore as text."
    # Check the text string contains the expected JSON.
    decoded = json.loads(invent.datastore[result_key])
    assert (
        decoded["result"]["properties"]["name"] == "Luke Skywalker"
    ), "Task result not stored in datastore."


async def test_simple_post_with_payload():
    """
    A simple POST request with a payload results in the expected JSON echo of
    the POST request information in the datastore at the specified key.
    """
    url = "https://httpbin.org/post"
    result_key = "echoed_payload"
    payload = {"key": "value"}
    body = json.dumps(payload)
    got_result_from_website = asyncio.Event()  # Used to wait for the result.

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    tasks.WebRequest(result_key).go(url, method="POST", body=body, json=True)

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore"
    assert (
        invent.datastore[result_key]["url"] == url
    ), "Task result not stored in datastore."
    assert (
        invent.datastore[result_key]["json"]["key"] == "value"
    ), "Task result not stored in datastore."
