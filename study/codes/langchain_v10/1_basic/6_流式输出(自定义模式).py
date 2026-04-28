from langchain.agents import create_agent
from langchain.tools import tool
import datetime
from conn.llm import get_llm
from langgraph.config import get_stream_writer

@ tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    writer = get_stream_writer()
    writer("自定义模式")
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

agent = create_agent(
    model=get_llm(), # 传一个llm
    tools=[get_current_time], # 工具函数列表
    system_prompt="你是一个助手", # 系统提示
)

res = agent.stream(
    input={"messages": [{"role": "user", "content": "现在几点"}]}, # 用户输入
    stream_mode="custom"
)

for chunk in res:
    print(chunk)