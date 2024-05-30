from typing import Awaitable


class Task():
    def __init__(self, awaitable: Awaitable):
        self.coro = awaitable.__await__()
        self.last_result = None

    def step(self):
        try:
            self.last_result = self.coro.send(self.last_result)
        except StopIteration as e:
            self.last_result = e.value
            raise e
