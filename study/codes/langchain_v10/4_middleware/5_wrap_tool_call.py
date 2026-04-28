from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage
from langchain.agents.middleware import wrap_tool_call
from conn.llm import get_llm

TOOL_CALLS = 0

def get_weather(city: str) -> str:
    """获得天气的工具"""
    global TOOL_CALLS
    TOOL_CALLS += 1
    if TOOL_CALLS < 3:
        raise Exception("出错了")
    return f"它总是雨天在 {city}!"

@wrap_tool_call
def my_wrap_tool_call(request,handler):
    for i in range(3):
        try:
            res = handler(request)
            break
        except Exception as e:
            print(e)
            continue
    return res

agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[get_weather], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    middleware=[my_wrap_tool_call]
)


figure = agent.get_graph().draw_mermaid_png()
with open("wrap_tool_call.png", "wb+") as f:
    f.write(figure)
#
# # Run the agent
res = agent.invoke({"messages":[HumanMessage(content="南京什么天气？")]})
print(res["messages"][-1].content)




