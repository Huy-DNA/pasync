# pasync - A simple event loop for async python

This minimal package is mainly used to explore implementing an async runtime in Python.

## Usage

### Runner

The main construct that you'll often work with is `Runner`.

A runner is actually a wrapper around an event loop.

It comes with two flavors: non-blocking runner and blocking runner.

* A blocking runner will run all the tasks till end, blocking the main thread.
  When given a set of tasks, it will refuse to accept any task in the meaning time.
* A non-blocking runner will run all the tasks in another thread.
  Unlike a blocking runenr, it can accepts additional tasks in the meaning time.

By default, a runner is blocking.

* Blocking runner
  ```py
  async def gen_num(n):
    return n
  
  with Runner() as runner:
    assert runner.run(gen_num(1)) == 1
    assert runner.gather(gen_num(1), gen_num(2)) == [1, 2]
  ```

* Non-blocking runner
  ```py
  async def gen_num(n):
    return n
  
  with Runner(non_blocking = True) as runner:
    assert runner.run(gen_num(1)) == None                  # Not support returning results yet
    assert runner.gather(gen_num(1), gen_num(2)) == None   # Not support returning results yet
  ```

## Pitfalls

1. Currently, non-blocking runner cannot return results of tasks yet.
   This can be worked around by making the top-level task return `None`, while all the subtasks's results are consumed inside the top-level task
