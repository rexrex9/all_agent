from langchain.agents import create_agent
from langchain.tools import tool
from conn.llms import get_llm
import datetime
from pydantic import BaseModel, Field

# 使用pydantic定义参数schema
class Args(BaseModel):
    a: int = Field(description="第一个数")
    b: int = Field(description="第二个数")

@ tool(name_or_callable="add_two_numbers", description="把两个数加起来", args_schema=Args)
def add_two_numbers(a, b):
    return a + b

@ tool(name_or_callable="get_current_time", description="获取当前时间")
def get_current_time():
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