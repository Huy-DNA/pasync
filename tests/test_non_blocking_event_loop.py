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
        runner.run(hello_async())
        runner.run(bye_async())
        runner.run(greeting_async())
