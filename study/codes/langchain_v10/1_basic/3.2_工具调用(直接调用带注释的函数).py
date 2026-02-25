from langchain.agents import create_agent
from conn.llms import get_llm
import datetime

agent = create_agent(
    model=get_llm(), # 传一个llm
    tools=[datetime.datetime.now], # 工具函数列表
    system_prompt="你是一个助手", # 系统提示
)

res = agent.invoke(
    input={"messages": [{"role": "user", "content": "现在几点"}]} # 用户输入
)

print(res) # 打印结果
print(res["messages"][-1].content) # 打印AI的回复