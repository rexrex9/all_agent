# 定义异步函数
import asyncio
# 协程：协程是Python中的一种特殊类型，它可以在函数中定义，并且可以在函数中暂停和恢复执行。

async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)
    print("Task 1 completed")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 completed")

async def main():
    # 并行运行多个任务
    await asyncio.gather(task1(), task2())


asyncio.run(main())