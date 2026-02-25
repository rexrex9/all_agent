from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command
import datetime
from conn.llms import get_llm
from common_utils import save_graph_img
from typing import Callable
@tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============ 中间件示例 ============

@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    print(f"实行工具调用: {request.tool_call['name']}")
    print(f"参数: {request.tool_call['args']}")
    try:
        result = handler(request)
        print(f"工具调用成功")
        return result
    except Exception as e:
        print(f"工具调用失败: {e}")
        raise


# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    # 传入中间件
    middleware=[
        monitor_tool,
    ]
)

# 保存图，此时图中没有中间件节点
save_graph_img(agent, "agent.png")

# 执行
print("=" * 50)
res = agent.stream(
    input={"messages": [{"role": "user", "content": "现在几点"}]}
)
for chunk in res:
    print(chunk)