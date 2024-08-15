"""
Tasks are units of work that can be executed asynchronously, but started from
synchronous code. They are a way to make asynchronous programming easier to
understand and teach.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import invent


class Task:
    """
    Represents an asynchronous task.

    A Taskask is easy to teach (no need to know about Python await etc...). The
    lifecycle of a Task is very simple to understand. The result of a Task is
    stored in the datastore if a key is provided, thus plugging into Invent's
    reactive data management.
    """

    def __init__(self, function, key=None, *args, **kwargs):
        """
        Create a Task. The function is an async function to await. The key
        is used to store the result of the function in the datastore. The
        args and kwargs are passed to the function when go() is called.
        """
        self.function = function
        self.key = key
        self.args = args
        self.kwargs = kwargs

    def go(self):
        """
        Wrap the function in a coroutine and schedule it to run.
        """

        async def wrapper():
            result = await self.function(*self.args, **self.kwargs)
            if self.key:
                invent.datastore[self.key] = result

        asyncio.create_task(wrapper())
