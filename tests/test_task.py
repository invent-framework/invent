import invent
import asyncio
from umock import Mock


def test_task_init():
    """
    Ensure the Task class is initialized correctly.
    """

    async def coro():
        pass

    task = invent.Task(coro, "key", 1, 2, 3, foo="bar")
    assert task.function == coro, "Task function not set correctly"
    assert task.key == "key", "Task key not set correctly"
    assert task.args == (1, 2, 3), "Task args not set correctly"
    assert task.kwargs == {"foo": "bar"}, "Task kwargs not set correctly"


async def test_task_go():
    """
    Ensure the Task class go method works correctly.
    """

    async def coro(*args, **kwargs):
        return args, kwargs

    task = invent.Task(coro, "key", 1, 2, 3, foo="bar")
    task.go()
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

    task = invent.Task(coro, None, 1, 2, 3, foo="bar")
    task.go()
    await asyncio.sleep(0.1)
    assert (
        len(invent.datastore) == 0
    ), f"Unexpected key found in datastore {invent.datastore}"
    spy.assert_called_once_with(1, 2, 3, foo="bar")
