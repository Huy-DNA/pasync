from pasync.runner import Runner

async def hello_async():
    print("Hello async!")

with Runner() as runner:
    runner.run(hello_async())
