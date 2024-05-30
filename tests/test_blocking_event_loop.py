from contextlib import redirect_stdout
import io

from pasync.runner import Runner

def test_simple():
    async def hello_async():
        print("Hello async!")

    async def bye_async():
        print("Bye async!")

    async def greeting_async():
        await hello_async()
        await bye_async()

    with Runner() as runner, redirect_stdout(io.StringIO()) as f:
        runner.run_all(hello_async())
        runner.run_all(bye_async())
        runner.run_all(greeting_async())
    assert f.getvalue() == "Hello async!\nBye async!\nHello async!\nBye async!\n"

def test_arithmetic():
    async def gen_3():
        return 3

    async def gen_2():
        return 2

    async def gen_5():
        three = await gen_3()
        two = await gen_2()
        return three + two

    with Runner() as runner:
        assert runner.run_task(gen_3()) == 3
        assert runner.run_task(gen_2()) == 2
        assert runner.run_task(gen_5()) == 5

        assert runner.run_all(gen_2(), gen_3(), gen_5()) == [2, 3, 5]
