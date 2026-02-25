import asyncio

async def task1():
    print("任务1开始")
    await asyncio.sleep(1)
    print("任务1结束")

async def task2():
    print("任务2开始")
    asyncio.create_task(task1())
    print("任务2结束")

asyncio.run(task2())