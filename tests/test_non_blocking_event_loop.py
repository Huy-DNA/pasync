from pasync.runner import Runner

def test_simple():
    async def hello_async():
        print("Hello async!")

    async def bye_async():
        print("Bye async!")

    async def greeting_async():
        await hello_async()
        await bye_async()

    with Runner(non_blocking = True) as runner:
        runner.gather(hello_async())
        runner.gather(bye_async())
        runner.gather(greeting_async())
