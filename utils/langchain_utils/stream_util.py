from langchain.messages import AIMessageChunk
from utils.general_utils.loggers import logger

# 流式打印日志
def stream_log(agent, input):
    generator = agent.stream(input={"messages": {'role': 'user', 'content': input}})
    for chunk in generator:
        logger.info(chunk)

# 流式打印tokens
def stream_print_tokens(agent, input):
    generator = agent.stream(input={"messages": {'role': 'user', 'content': input}},stream_mode="messages")
    for chunk in generator:
        content = chunk[0].content
        if content:
            print(chunk[0].content, end="", flush=True)

# 流式打印所有(token和日志)
def stream_both(agent, input):
    def stream_output(generator):
        for r in generator:
            if r[0] == "updates":
                logger.info(r[1])
            if r[0] == "messages":
                if type(r[1][0])!=AIMessageChunk:
                    continue
                c = r[1][0].content
                if c:
                    yield c

    generator = agent.stream(input={"messages": {'role': 'user', 'content': input}},stream_mode=["messages", "updates"])
    for chunk in stream_output(generator):
        print(chunk, end="", flush=True)