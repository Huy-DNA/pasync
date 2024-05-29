from typing import List, Optional
from collections import deque
from threading import Thread

from pasync.task import Task

class EventLoop():
    def __init__(self, *tasks: List[Task]):
        self.__task_queue = deque(tasks) 

    def push(self, task: Task):
        self.__task_queue.append(task)

    def __pop(self) -> Optional[Task]:
        if len(self.__task_queue) == 0:
            return None
        return self.__task_queue.popleft()
    
    def run(self, *, thread: Optional[Thread] = None):
        pass 
