from typing import Awaitable


class Task():
    def __init__(self, awaitable: Awaitable):
        self.coro = awaitable.__await__()
        self.last_result = None

    def step(self):
        self.last_result = self.coro.send(self.last_result)
