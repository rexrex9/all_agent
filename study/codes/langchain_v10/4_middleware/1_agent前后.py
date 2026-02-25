from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import AgentState,before_agent, after_agent
import datetime
from conn.llms import get_llm
from common_utils import save_graph_img
from langgraph.runtime import Runtime

@tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============ 中间件示例 ============

# 1. @before_agent - 在 Agent 执行前运行
@before_agent
def agent_start(state:AgentState,runtime:Runtime):
    """在 Agent 开始执行前记录日志"""
    print(f"🚀 Agent 开始执行")
    print(f"state:",state)
    print(f"runtime:", runtime)
    return state


# 2. @after_agent - 在 Agent 执行后运行
@after_agent
def agent_end(state,runtime):
    """在 Agent 执行完成后记录日志"""
    print(f"✅ Agent 执行完成")
    print(f"state:",state)
    print(f"runtime:", runtime)
    return state

# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    # 传入中间件
    middleware=[
        agent_start,
        agent_end,
    ]
)

# 保存图
save_graph_img(agent, "agent.png")

# 执行
print("=" * 50)
res = agent.stream(
    input={"messages": [{"role": "user", "content": "现在几点"}]}
)
for chunk in res:
    print(chunk)