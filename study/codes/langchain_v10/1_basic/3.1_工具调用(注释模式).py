from langchain.agents import create_agent
from conn.llms import get_llm
import datetime
from langchain.tools import tool

@ tool
def add_two_numbers(a, b):
    """
    把两个数加起来.
    :param a: 第一个数.
    :param b: 第二个数.
    :return: 相加的和.
    """
    return a + b

@ tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

agent = create_agent(
    model=get_llm(), # 传一个llm
    tools=[get_current_time, add_two_numbers], # 工具函数列表
    system_prompt="你是一个助手", # 系统提示
)

res = agent.invoke(
    input={"messages": [{"role": "user", "content": "1+2等于几"}]} # 用户输入
)

print(res) # 打印结果
print(res["messages"][-1].content) # 打印AI的回复