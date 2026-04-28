
from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage
from conn.llm import get_llm
from langchain.agents import AgentState
from langchain.agents.middleware import before_agent,after_model

# 需求，统计一下模型在一次请求中的调用次数
# 额外要求，模型调用次数的初始值不在invoke时设置

# 自定义一个State,中间有个记录模型调用次数的字段
class MYState(AgentState):
    model_count: int  # 模型调用次数

# 1. 给model_count初始值
@before_agent
def init_model_count(state: MYState, runtime):
    return {'model_count': 0}

# 2. model_count增加1
@after_model
def model_count_add(state: MYState, runtime):
    print(state['model_count'])
    return {'model_count': state['model_count'] + 1}

def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

agent = create_agent(
    model=get_llm(),
    tools=[get_weather],
    system_prompt="你是一个助手",
    middleware=[init_model_count, model_count_add], # 把中间件传入给Agent
    state_schema=MYState, # 把自定义的State传入给Agent
)


res = agent.invoke({"messages":[HumanMessage(content="南京什么天气？")]})
print(res["messages"][-1].content)
print(res['model_count'])