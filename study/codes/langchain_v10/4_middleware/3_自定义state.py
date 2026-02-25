from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import before_model, after_model,AgentState
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


# ============ 自定义 State ============

class CustomAgentState(AgentState): #继承AgentState
    """自定义 Agent 状态"""
    call_count: int  # 自定义：模型调用次数


# ============ 中间件示例 ============

@before_model
def model_start(state: CustomAgentState, runtime):
    """在调用模型前增加计数"""
    # 更新自定义字段
    return {'call_count': state.get('call_count', 0) + 1}


@after_model
def model_end(state: CustomAgentState, runtime):
    """在模型返回后打印信息"""
    print(f"after model - 累计调用次数: {state['call_count']}")

# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    state_schema=CustomAgentState,  # 使用自定义 State
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
    input={
        "messages": [{"role": "user", "content": "现在几点"}],
        "call_count": 0  # 初始化自定义字段
    }
)
for chunk in res:
    print(chunk)
    # 可以看到 call_count 的变化
    if 'call_count' in chunk:
        print(f"📊 模型调用次数: {chunk['call_count']}")
