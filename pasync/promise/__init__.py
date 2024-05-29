from typing import Callable, Awaitable, Optional

from src.event_loop import EventLoop

class Promise():
    def __init__(self, coro: Callable[..., Awaitable]):
        pass
