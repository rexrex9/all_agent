import asyncio

def tools(func):
    ts = asyncio.run(func())
    return ts