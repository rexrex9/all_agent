import asyncio
import os # operator system 操作系统，操作系统级的文件操作天生都是线程阻塞操作

def add(a,b):
    return a+b

async def do():
    a = await asyncio.to_thread(add,1,2)
    print(a)
# 把一个同步函数转为异步函数

if __name__ == "__main__":
    asyncio.run(do())