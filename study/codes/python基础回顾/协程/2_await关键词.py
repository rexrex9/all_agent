import asyncio

async def task1():
    print("任务1开始")

async def task2():
    await task1()

asyncio.run(task2())

