from demo_deepagent import agent
from deepagents import CompiledSubAgent
from deepagents import create_deep_agent
from conn.llm import get_llm

sub = CompiledSubAgent(name="超级助手", description="一个得力干将", runnable=agent)

agent = create_deep_agent(
    model=get_llm(),
    subagents=[sub],
    system_prompt="你是一个助手,但是你手下有一个名为超级助手得力干将，任何任务都让他干",
)

if __name__ == '__main__':
    res = agent.stream(
        input={"messages": [{"role": "user", "content": "现在几点"}]} # 用户输入
    )
    for chunk in res:
        print(chunk)
