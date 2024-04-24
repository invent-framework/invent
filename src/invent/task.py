"""
Tasks!
"""

import asyncio
import invent


class Task:
    """
    Represents an asynchronous task.

    1. Task is easy to teach (no need to know about Python await etc...)
    2. Lifecycle of a Task.
    3. Arbitrary messages emitted by a task (e.g. as part of a pipeline-ish).
    4. Setting of datastore value as the final result.
    """

    def __init__(
        self, function, key=None, indicator="", channel="", *args, **kwargs
    ):
        self.function = function
        self.key = key
        self.indicator = indicator
        self.channel = channel
        self.args = args
        self.kwargs = kwargs

    def go(self):
        async def wrapper():
            result = await self.function(self, *self.args, **self.kwargs)
            if self.key:
                invent.datastore[self.key] = result

        asyncio.create_task(wrapper())
