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
    Synchronously schedule a asynchronous task whose result will end up in
    the datastore. This is a base class for all tasks in Invent, and the child
    classes should implement/reference the function to be awaited, along with
    any other context-appropriate capabilities.

    A Task is easy to teach (no need to know about Python await etc...) and the
    lifecycle of a Task is very simple to understand:

    1. Instantiate the task with an optional result_key (the key in the
       datastore where the result will be stored).
    2. Call task's the go() method with any arguments required by the
       underlying asynchronous function.
    3. The result of a Task is stored in the datastore if the result_key is
       provided, thus plugging into Invent's reactive data management.

    That's it. Simple, easy to understand, and powerful. Check the child
    classes for examples of how to implement a Task.
    """

    #: A reference to the asynchronous function to be awaited. This should be
    #: implemented / referenced by the child class.
    function = None

    def __init__(self, result_key=None):
        """
        Create a Task.

        The optional result_key is used to store the result of the function in
        the datastore.
        """
        self.result_key = result_key

    def go(self, *args, **kwargs):
        """
        Wrap the task's asynchronous function in a coroutine and schedule it to
        run.

        The args and kwargs are passed to the asynchronous function. If a
        result_key is provided, the result of the asynchronous function is
        stored in the datastore, thus plugging into Invent's reactive data
        management.
        """

        async def wrapper():
            result = await self.function(*args, **kwargs)
            if self.result_key:
                invent.datastore[self.result_key] = result

        asyncio.create_task(wrapper())
