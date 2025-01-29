import asyncio
import upytest
import umock
from invent.tools import timing


# Schedule a function.
async def test_schedule():
    """
    Scheduling a function to run with the given arguments, after a delay, also
    means it is cleaned up after it runs.
    """
    fn_called = asyncio.Event()  # Used to wait for the result.

    result_args = None
    result_kwargs = None

    def my_fn(*args, **kwargs):
        nonlocal result_args, result_kwargs
        result_args = args
        result_kwargs = kwargs
        fn_called.set()

    delay = 10  # 10 milliseconds.

    handle = timing.schedule(my_fn, delay, "foo", bar="baz")

    fn_id = id(my_fn)
    assert fn_id in timing.SCHEDULED_FUNCTIONS, "Function not scheduled."
    assert timing.SCHEDULED_FUNCTIONS[fn_id] == handle, "Handle not stored."
    await fn_called.wait()
    assert result_args == ("foo",), result_args
    assert result_kwargs == {"bar": "baz"}, result_kwargs
    assert fn_id not in timing.SCHEDULED_FUNCTIONS, "Function still scheduled."


def test_schedule_invalid_func():
    """
    Scheduling a non-callable function should raise an error.
    """
    with upytest.raises(ValueError):
        timing.schedule("foo", 10)


def test_schedule_negative_delay():
    """
    Scheduling a function with a negative delay should raise an error.
    """
    with upytest.raises(ValueError):
        timing.schedule(lambda: None, -10)


def test_schedule_already_scheduled():
    """
    Scheduling a function that is already scheduled should raise an error.
    """

    def my_fn():
        pass

    timing.schedule(my_fn, 10)
    with upytest.raises(ValueError):
        timing.schedule(my_fn, 10)


# Schedule an event to repeat.


async def test_repeat():
    """
    Scheduling a function to run repeatedly with the given arguments, after a
    delay, also means it is cleaned up after it runs.
    """
    fn_called = asyncio.Event()  # Used to wait for the result.

    result_args = None
    result_kwargs = None
    counter = 0

    def my_fn(*args, **kwargs):
        nonlocal result_args, result_kwargs, counter
        counter += 1
        if counter == 3:
            result_args = args
            result_kwargs = kwargs
            fn_called.set()

    delay = 10  # 10 milliseconds.

    handle = timing.repeat(my_fn, delay, "foo", bar="baz")

    fn_id = id(my_fn)
    assert fn_id in timing.SCHEDULED_FUNCTIONS, "Function not scheduled."
    assert timing.SCHEDULED_FUNCTIONS[fn_id] == handle, "Handle not stored."
    await fn_called.wait()
    assert result_args == ("foo",), result_args
    assert result_kwargs == {"bar": "baz"}, result_kwargs
    assert counter == 3, counter
    assert fn_id in timing.SCHEDULED_FUNCTIONS, "Function not scheduled."
    timing.cancel(my_fn)


# Cancel an event.


def test_cancel():
    """
    Cancelling a scheduled function should remove it from the scheduled
    functions once the underlying JavaScript `clearTimeout` function is called.
    """

    def my_fn():
        pass

    handle = timing.schedule(my_fn, 10)
    fn_id = id(my_fn)
    assert fn_id in timing.SCHEDULED_FUNCTIONS, "Function not scheduled."
    cancelled_flag = False
    with umock.patch("invent.tools.timing:window") as mock_window:
        cancelled_flag = timing.cancel(my_fn)
        assert (
            fn_id not in timing.SCHEDULED_FUNCTIONS
        ), "Function still scheduled."
        assert cancelled_flag, "Function not cancelled."
        mock_window.clearTimeout.assert_called_once_with(handle)
