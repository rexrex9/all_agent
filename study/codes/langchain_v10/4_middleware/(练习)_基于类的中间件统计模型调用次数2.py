from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage
from conn.llm import get_llm
from mytools import *
from langchain.agents.middleware import AgentMiddleware,AgentState
import time
# 需求：
# 统计模型调用次数，如果调用次数大于等于2，则休眠2秒, 并调用次数清0

class MyState(AgentState):
    model_count: int  # 模型调用次数
class MyMiddleware(AgentMiddleware):

    state_schema = MyState

    def __init__(self,max_model_calls,sleep_time):
        """
        :param max_model_calls: 一轮休眠期最大模型调用次数
        :param sleep_time: 休眠时间
        """
        self.max_model_calls = max_model_calls
        self.sleep_time = sleep_time

    def before_agent(self, state, runtime):
        return {'model_count': 0}

    def after_model(self, state,runtime):
        return {'model_count': state['model_count'] + 1}

    def before_model(self, state, runtime):
        print('当前模型调用次数', state['model_count'])
        if state['model_count'] >= self.max_model_calls:
            print('模型调用次数大于等于max_model_calls，休眠sleep_time')
            # 当模型调用次数大于等于max_model_calls，则休眠sleep_time
            time.sleep(self.sleep_time)
            # 把模型调用次数清0
            return {'model_count': 0}

def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

agent = create_agent(
    model=get_llm(),
    tools=[get_weather, search, calculator, current_time, unit_converter],
    system_prompt="你是一个助手",
    middleware=[MyMiddleware(max_model_calls=2,sleep_time=2)],
)

res = agent.stream({"messages":[HumanMessage(content="姚明身高多少英尺？必须给我回答")]})
for chunk in res:
    print(chunk)
