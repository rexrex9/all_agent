from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call, AgentMiddleware,AgentState,before_agent
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from conn.llm import get_llm

# ============ 自定义 State ============
class CustomState(AgentState):
    stop_reason: str  # 自定义：停止原因

# ============ 定义工具 ============
@tool
def stop_command():
    """停止命令"""
    return "已停止"

@before_agent
def init_state(state: CustomState, runtime):
    return {"stop_reason": ""}

@wrap_tool_call
def auto_stop(request,handler) -> ToolMessage | Command:
    tool_name = request.tool_call['name']

    # 如果是 stop_command，结束并更新自定义字段
    if tool_name == "stop_command":
        print("🛑 检测到停止命令，直接结束")
        return Command(
            goto="__end__",
            update={"stop_reason": "用户叫停止的"}  # 更新自定义字段
        )
    # 其他工具正常执行
    return handler(request)


# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[stop_command],
    system_prompt="你是一个助手",
    state_schema=CustomState,
    middleware=[auto_stop]
)

# ============ 测试 ============
res2 = agent.invoke({
    "messages": [{"role": "user", "content": "停止"}],
    "stop_reason": ""
})
print(f"结果: {res2['messages'][-1].content}")
print(f"停止原因: {res2.get('stop_reason')}")  # 查看自定义字段