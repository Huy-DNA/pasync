from typings import Optional, Callable, Awaitable

import utils
import runner
import stream

from event_loop import EventLoop

def run(coro: Callable[..., Awaitable], *, event_loop: Optional[EventLoop] = None):
    pass
