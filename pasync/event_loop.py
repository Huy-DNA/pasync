from enum import Enum
import threading
from typing import List, Optional
from collections import deque
from threading import Thread

from pasync.task import Task

class _RunMode(Enum):
    IDLE = 0
    BLOCKING = 1
    NON_BLOCKING = 2
    STOP_SIGNALLED = 3

class EventLoop():
    def __init__(self, *tasks: List[Task]):
        self.__task_queue = deque(tasks) 
        self.__run_mode = _RunMode.IDLE
        self.__push_cv = threading.Condition()

    def queue(self, task: Task):
        if self.__run_mode == _RunMode.STOP_SIGNALLED:
            raise Exception("Warning: Queuing a task on an event queue that was signalled to stop has no effect") 

        self.__queue(task)
        
        if self.__run_mode == _RunMode.NON_BLOCKING:
            self.__push_cv.notify()

    def signal_stop(self):
        self.__run_mode = _RunMode.STOP_SIGNALLED
        if self.__run_mode == _RunMode.NON_BLOCKING:
            self.__push_cv.notify()

    def run_non_blocking(self):
        if self.__run_mode != _RunMode.IDLE:
            raise Exception("The event loop is already running")
        self.__run_mode = _RunMode.NON_BLOCKING

        def run_continously():
            while self.__run_mode != _RunMode.STOP_SIGNALLED:
                task = self.__dequeue()
                if not task:
                    self.__push_cv.wait()
                    task = self.__dequeue()
                    if not task:
                        break
                try:
                    task.step()
                    self.__queue(task)
                except StopAsyncIteration:
                    pass

            self.__run_mode = _RunMode.IDLE

        Thread(target = run_continously) 

    def run_blocking(self):
        if self.__run_mode != _RunMode.IDLE:
            raise Exception("The event loop is already running")
        self.__run_mode = _RunMode.BLOCKING

        while task := self.__dequeue():
            try:
                task.step()
                self.__queue(task)
            except StopAsyncIteration:
                pass
        
        self.__run_mode = _RunMode.IDLE

    def __queue(self, task: Task):
        self.__task_queue.append(task)

    def __dequeue(self) -> Optional[Task]:
        if len(self.__task_queue) == 0:
            return None
        return self.__task_queue.popleft()
    
