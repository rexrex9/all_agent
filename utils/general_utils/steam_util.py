from langchain.messages import AIMessageChunk
from utils.general_utils.loggers import logger
# 流式打印所有(token和日志)
def stream_print_all(generator):
    stream_print(steam_output( generator))


def steam_output(generator):
    for r in generator:
        if r[0] == "updates":
            logger.info(r[1][0])
        if r[0] == "messages":
            if type(r[1][0])!=AIMessageChunk:
                continue
            c = r[1][0].content
            if c:
                yield c

# 流式打印
def stream_print(generator):
    for chunk in generator:
        print(chunk, end="", flush=True)

def stream_print_log(generator):
    for chunk in generator:
        print(chunk, flush=True)

async def astream_print_log(generator):
    async for chunk in generator:
        print(chunk, flush=True)
async def astream_print(generator):
    async for chunk in generator:
        print(chunk, end="", flush=True)
