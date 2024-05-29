from typing import Callable, Awaitable, Optional

from pasync.event_loop import EventLoop

class Promise():
    def __init__(self, coro: Callable[..., Awaitable]):
        pass
