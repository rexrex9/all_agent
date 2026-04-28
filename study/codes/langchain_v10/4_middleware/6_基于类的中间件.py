
from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage
from conn.llm import get_llm
from langchain.agents.middleware import AgentMiddleware

# 所谓的中间件类就是自定义一个类去继承AgentMiddleware
class MyMiddleware(AgentMiddleware):

    def before_agent(self, state, runtime):
        print('before_agent')

    def after_model(self, state, runtime):
        print('after_model')

    def before_model(self, state, runtime):
        print('before_model')

    def after_agent(self, state, runtime):
        print('after_agent')

    def wrap_model_call(self,request,handler):
        print('wrap_model_call')
        result = handler(request)
        return  result

    def wrap_tool_call(self,request,handler):
        print('wrap_tool_call')
        result = handler(request)
        return  result

def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

agent = create_agent(
    model=get_llm(),
    tools=[get_weather],
    system_prompt="你是一个助手",
    middleware=[MyMiddleware()], # 把中间件类的实例传给Agent
)

res = agent.invoke({"messages":[HumanMessage(content="南京什么天气？")]})
print(res["messages"][-1].content)
