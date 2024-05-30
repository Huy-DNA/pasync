from enum import Enum
import threading
from typing import Awaitable, Optional, Union
from collections import deque
from threading import Thread

from pasync.task import Task as _Task

class _RunMode(Enum):
    IDLE = 0
    BLOCKING = 1
    NON_BLOCKING = 2
    STOP_SIGNALLED = 3

class EventLoop():
    def __init__(self, *tasks: Union[Awaitable, _Task]):
        self.__task_queue = deque([_Task(task) if not isinstance(task, _Task) else task for task in tasks])
        self.__run_mode = _RunMode.IDLE
        self.__push_cv = threading.Condition()
        self.__thread = None

    def queue(self, task: Union[Awaitable, _Task]):
        if self.__run_mode == _RunMode.STOP_SIGNALLED:
            raise Exception("Queuing a task on an event queue that was signalled to stop has no effect") 

        if self.__run_mode == _RunMode.BLOCKING:
            raise Exception("Can not queue a task on an already running blocking event loop")

        if not isinstance(task, _Task):
            self.__queue(_Task(task))
        else:
            self.__queue(task)
        
        if self.__run_mode == _RunMode.NON_BLOCKING:
            with self.__push_cv:
                self.__push_cv.notify()

    def signal_stop(self):
        self.__run_mode = _RunMode.STOP_SIGNALLED
        if self.__run_mode == _RunMode.NON_BLOCKING:
            with self.__push_cv:
                self.__push_cv.notify()

    def run_non_blocking(self):
        if self.__run_mode != _RunMode.IDLE:
            raise Exception("The event loop is already running")
        self.__run_mode = _RunMode.NON_BLOCKING

        def run_continously():
            with self.__push_cv:
                while len(self.__task_queue) or self.__run_mode != _RunMode.STOP_SIGNALLED:
                    task = self.__dequeue()
                    if not task:
                        self.__push_cv.wait()
                        task = self.__dequeue()
                        if not task:
                            break
                    try:
                        task.step()
                        self.__queue(task)
                    except StopIteration:
                        pass

            self.__run_mode = _RunMode.IDLE

        self.__thread = Thread(target = run_continously) 
        self.__thread.start()

    def run_blocking(self):
        if self.__run_mode != _RunMode.IDLE:
            raise Exception("The event loop is already running")
        self.__run_mode = _RunMode.BLOCKING

        while task := self.__dequeue():
            try:
                task.step()
                self.__queue(task)
            except StopIteration:
                pass
        
        self.__run_mode = _RunMode.IDLE

    @property
    def thread(self) -> Optional[Thread]:
        return self.__thread

    def __queue(self, task: _Task):
        self.__task_queue.append(task)

    def __dequeue(self) -> Optional[_Task]:
        if len(self.__task_queue) == 0:
            return None
        return self.__task_queue.popleft()
 
