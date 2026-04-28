from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage,AIMessage,ToolMessage
from conn.llm import get_llm
from langchain.agents.middleware import before_agent,after_agent
from langchain.agents import AgentState
from langgraph.runtime import Runtime

def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

@before_agent
def before_agent_middleware(state:AgentState,runtime:Runtime):
    print('before_agent')
    print(state)
    print(runtime)

@after_agent
def after_agent_middleware(state:AgentState,runtime:Runtime):
    print('after_agent')
    print(state)
    print(runtime)

#

agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[get_weather], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    middleware=[before_agent_middleware,after_agent_middleware]
)
# figure = agent.get_graph().draw_mermaid_png()
# with open("sss.png", "wb+") as f:
#     f.write(figure)
#

res = agent.stream({"messages":[HumanMessage(content="南京什么天气？")]})
for r in res:
    print(r)




