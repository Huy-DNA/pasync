from contextlib import redirect_stdout
import io
import threading

from pasync.runner import Runner
from pasync import Promise

def test_simple():
    def promise_callback(resolve, reject):
        print("start promise")
        print("end promise")
    
    with Runner() as runner, redirect_stdout(io.StringIO()) as f:
        promise = Promise(promise_callback)
        runner.run_task(promise)
    assert f.getvalue() == "start promise\nend promise\n"

