from contextlib import redirect_stdout
import io

from pasync.runner import Runner
from pasync import Promise

def test_simple():
    def promise_callback(resolve, reject):
        print("start promise")
        print("end promise")
        resolve(None)
    
    with Runner() as runner, redirect_stdout(io.StringIO()) as f:
        promise = Promise(promise_callback)
        runner.run_task(promise)
    assert f.getvalue() == "start promise\nend promise\n"

def test_arithmetic():
    def promise_3(resolve, reject):
        resolve(3)

    def add_2(num):
        return num + 2
    
    with Runner() as runner:
        promise = Promise(promise_3)
        assert runner.run_task(promise) == 3
        promise_then = promise.then(add_2)
        assert runner.run_task(promise_then) == 5
        
        promise = Promise(promise_3).then(add_2)
        assert runner.run_task(promise) == 5
