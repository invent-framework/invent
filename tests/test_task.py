import invent
import asyncio
from umock import Mock


def test_task_init():
    """
    Ensure the Task class is initialized correctly.
    """
    task = invent.Task("key")
    assert task.result_key == "key", "Task key not set correctly"


async def test_task_go():
    """
    Ensure the Task class go method works correctly.
    """

    async def coro(*args, **kwargs):
        return args, kwargs

    task = invent.Task("key")
    task.function = coro
    task.go(1, 2, 3, foo="bar")
    await asyncio.sleep(0.1)
    assert "key" in invent.datastore, "Expected key not found in datastore"
    assert invent.datastore["key"] == (
        (1, 2, 3),
        {"foo": "bar"},
    ), "Task result not stored in datastore"


async def test_task_go_no_key():
    """
    Ensure the Task class go method works correctly with no key.
    """
    spy = Mock()

    async def coro(*args, **kwargs):
        spy(*args, **kwargs)
        return args, kwargs

    task = invent.Task()
    task.function = coro
    task.go(1, 2, 3, foo="bar")
    await asyncio.sleep(0.1)
    assert (
        len(invent.datastore) == 0
    ), f"Unexpected key found in datastore {invent.datastore}"
    spy.assert_called_once_with(1, 2, 3, foo="bar")
