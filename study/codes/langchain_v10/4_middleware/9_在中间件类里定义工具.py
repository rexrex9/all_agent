from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage,AIMessage,ToolMessage
from conn.llm import get_llm
from langchain.agents.middleware import AgentMiddleware

def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

class MyMiddleware(AgentMiddleware):
    tools = [get_weather] # 把工具传入给中间件类中


agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    middleware=[MyMiddleware()]
)
# figure = agent.get_graph().draw_mermaid_png()
# with open("sss.png", "wb+") as f:
#     f.write(figure)
#

res = agent.stream({"messages":[HumanMessage(content="南京什么天气？")]})
for r in res:
    print(r)




