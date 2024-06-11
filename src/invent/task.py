"""
Tasks get stuff done in the background.
"""

import asyncio
import invent


class Task:
    """
    Instances of this class represent a background task.
    """

    def __init__(
        self, function, key=None, handler=None, error=None, *args, **kwargs
    ):
        """
        Initialise with an awaitable `function`.

        The optional `key` in the datastore will be populated with the result
        of the awaitable function.

        If an optional `handler` function is provided it will also be called
        with the result of the awaitable.

        An optional `error` function will be called if awaiting the function
        results in an exception. The `error` function will be called with the
        exception as its single argument.

        All further arguments passed in at initialisation of the Task are
        passed into the awaitable function.

        Once instantiated, call the object's `go` method to start the task.
        """
        self.function = function
        self.key = key
        self.handler = handler
        self.error = error
        self.args = args
        self.kwargs = kwargs

    def go(self):
        """
        Schedule the defined task to start.

        If the ignore_no_result flag is set to True (default False), then
        false-y / empty / None results are ignored. Otherwise, handle any
        results.
        """
        async def wrapper():
            try:
                result = await self.function(*self.args, **self.kwargs)
                if self.key:
                    if self.handler:
                        result = self.handler(result)
                    invent.datastore[self.key] = result
            except Exception as ex:
                if self.error:
                    self.error(ex)
        asyncio.create_task(wrapper())
