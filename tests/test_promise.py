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

    def promise_5(resolve, reject):
        reject(5)

    def add_2(num):
        return num + 2
    
    with Runner() as runner:
        promise = Promise(promise_3)
        assert runner.run_task(promise) == 3
        promise_then = promise.then(add_2)
        assert runner.run_task(promise_then) == 5
        
        promise = Promise(promise_3).then(add_2)
        assert runner.run_task(promise) == 5

        promise = Promise(promise_5).then(lambda num: num, add_2)
        assert runner.run_task(promise) == 7
        
        promise = Promise(promise_5).then(lambda num: num + 1).catch(add_2)
        assert runner.run_task(promise) == 7

        promise = Promise(promise_3).then(lambda num: num + 1).catch(add_2)
        assert runner.run_task(promise) == 4

def test_throw_in_promise():
    def throw_3(resolve, reject):
        raise Exception(3)

    with Runner() as runner:
        promise = Promise(throw_3).then(lambda num: num + 1).catch(lambda e: e)
        assert f"{runner.run_task(promise)}" == "3"
