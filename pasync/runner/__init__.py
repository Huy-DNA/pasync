from typing import Awaitable
from pasync.event_loop import EventLoop
from pasync.task import Task as _Task


class Runner():
    def __init__(self, *, event_loop = None, non_blocking = False):
        self.__event_loop = event_loop or EventLoop()
        self.__non_blocking = non_blocking
        self.__is_non_blocking_running = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_msg):
        self.close()
        return False

    def close(self):
        if self.__is_non_blocking_running and self.__event_loop.thread:
            self.__event_loop.signal_stop()
            self.__event_loop.thread.join()

    def gather(self, *awaitables: Awaitable):
        tasks = [_Task(awaitable) for awaitable in awaitables]
        if self.__non_blocking:
            self.__run_non_blocking(*tasks)
        else:
            self.__run_blocking(*tasks)
            return [task.last_result for task in tasks]

    def run_task(self, awaitable: Awaitable):
        task = _Task(awaitable)
        if self.__non_blocking:
            self.__run_non_blocking(task)
        else:
            self.__run_blocking(task)
            return task.last_result
        
    def __run_blocking(self, *tasks: _Task):
        [self.__event_loop.queue(task) for task in tasks]
        self.__event_loop.run_blocking()

    def __run_non_blocking(self, *tasks: _Task):
        [self.__event_loop.queue(task) for task in tasks]
        if not self.__is_non_blocking_running:
            self.__event_loop.run_non_blocking()
            self.__is_non_blocking_running = True 
