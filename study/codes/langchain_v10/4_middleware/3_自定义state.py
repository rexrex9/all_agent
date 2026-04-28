from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage
from conn.llm import get_llm
from langchain.agents import AgentState
class MYState(AgentState):
    model_count:int
def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[get_weather], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    state_schema = MYState,
)


res = agent.invoke({"messages":[HumanMessage(content="南京什么天气？")],'model_count':0})
print(res["messages"][-1].content)
print(res['model_count'])




