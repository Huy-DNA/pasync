from contextlib import redirect_stdout
import io
import threading

from pasync.runner import Runner
from pasync import Promise

def test_simple():
    def promise_callback(resolve, reject):
        def delayed_call():
            print("about to resolve!")
            resolve(True)

        print("start promise, waiting 3 seconds")
        threading.Timer(3, delayed_call, None, None)
        print("waiting for promise end")
    
    with Runner() as runner, redirect_stdout(io.StringIO()) as f:
        promise = Promise(promise_callback)
        runner.run_task(promise)
    assert f.getvalue() == "start promise, waiting 3 seconds\nwaiting for promise end\n"
