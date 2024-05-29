from typing import Awaitable
from pasync.event_loop import EventLoop


class Runner():
    def __init__(self, *, event_loop = None, non_blocking = False):
        self.__event_loop = event_loop or EventLoop()
        self.__non_blocking = non_blocking
        self.__is_non_blocking_running = False

    def run(self, awaitable: Awaitable, *awaitables: Awaitable):
        if self.__non_blocking:
            self.__run_non_blocking(awaitable, *awaitables)
        else:
            self.__run_blocking(awaitable, *awaitables)
        
    def __run_blocking(self, *awaitables: Awaitable):
        [self.__event_loop.queue(task) for task in awaitables]
        self.__event_loop.run_blocking()

    def __run_non_blocking(self, *awaitables: Awaitable):
        [self.__event_loop.queue(task) for task in awaitables]
        if not self.__is_non_blocking_running:
            self.__event_loop.run_non_blocking()
            self.__is_non_blocking_running = True 
