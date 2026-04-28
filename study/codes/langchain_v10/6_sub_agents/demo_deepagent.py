from deepagents import create_deep_agent
from conn.llm import get_llm
from sub_agent_random import get_agent as get_random_agent # 导入随机数的子Agent
from sub_agent_time import get_agent as get_time_agnet # 导入获取时间的子Agent

agent = create_deep_agent(
    model=get_llm(),
    tools=[],
    system_prompt="你是一个助手",
    subagents = [get_time_agnet(),get_random_agent()]
)

if __name__ == '__main__':
    res = agent.stream(
        input={"messages": [{"role": "user", "content": "给我一个随机数"}]} # 用户输入
    )
    for chunk in res:
        print(chunk)