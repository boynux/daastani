import asyncio
import concurrent.futures


class Event:
    def __init__(self):
        self._handlers = []

    def add(self, handler):
        self._handlers.append(handler)

        return self

    def remove(self, handler):
        self._handlers.remove(handler)

        return self

    def fire(self, sender, args=[]):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            loop = asyncio.get_running_loop()
            return [loop.run_in_executor(pool, handler, sender, *args) for handler in self._handlers]
        # for handler in self._handlers:
        #     asyncio.create_task(wrap())

    __iadd__ = add
    __isub__ = remove
    __call__ = fire
