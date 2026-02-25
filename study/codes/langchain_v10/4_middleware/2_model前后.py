from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import before_model, after_model
import datetime
from conn.llms import get_llm
from common_utils import save_graph_img

@tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============ 中间件示例 ============

@before_model
def model_start(state,runtime):
    print("before model")
    return state

@after_model
def model_end(state,runtime):
    print("after model")
    return state

# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    # 传入中间件
    middleware=[
        model_start,
        model_end,
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