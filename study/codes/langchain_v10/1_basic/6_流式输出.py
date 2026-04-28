from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage

from conn.llm import get_llm
def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[get_weather], # 工具集
    system_prompt="你是一个助力", # 系统提示词
)

# Run the agent
result = agent.stream({"messages":[HumanMessage(content="南京什么天气？")]},stream_mode='updates')
for res in result:
    print(res)




