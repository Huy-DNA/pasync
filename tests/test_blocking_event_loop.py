from contextlib import redirect_stdout
import io

from pasync.runner import Runner

async def hello_async():
    print("Hello async!")

async def bye_async():
    print("Bye async!")

async def greeting_async():
    await hello_async()
    await bye_async()

def test():
    with Runner() as runner, redirect_stdout(io.StringIO()) as f:
        runner.run(hello_async())
        runner.run(bye_async())
        runner.run(greeting_async())
    assert f.getvalue() == "Hello async!\nBye async!\nHello async!\nBye async!\n"
