from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import AgentMiddleware
import datetime
from conn.llms import get_llm
from common_utils import save_graph_img


# ============ 定义工具 ============

@tool
def get_current_time():
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============ 类式中间件（包含全部 6 种钩子） ============

class CompleteMid(AgentMiddleware):
    """完整的中间件示例，包含所有 6 种钩子"""

    # 1. before_agent - Agent 开始前（执行 1 次）
    def before_agent(self, state, runtime):
        print("\n" + "=" * 50)
        print("1️⃣ before_agent - Agent 开始")
        return None

    # 2. before_model - 模型调用前（每次调用执行）
    def before_model(self, state, runtime):
        print("\n🤖 before_model - 准备调用模型")
        print(f"   当前消息数: {len(state['messages'])}")
        return None

    # 3. wrap_model_call - 包装模型调用（完全控制）
    def wrap_model_call(self, request, handler):
        print("\n🔄 wrap_model_call - 模型调用包装")
        print(f"   模型: {request.model}")

        # 实际调用模型
        response = handler(request)
        return response

    # 4. after_model - 模型调用后（每次调用执行）
    def after_model(self, state, runtime):
        print("\n✅ after_model - 模型调用完成")
        last_msg = state['messages'][-1]
        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
            print(f"   模型要调用工具: {last_msg.tool_calls[0]['name']}")
        else:
            print(f"   模型响应: {last_msg.content[:50]}...")
        return None

    # 5. wrap_tool_call - 包装工具调用（完全控制）
    def wrap_tool_call(self, request, handler):
        print("\n🔧 wrap_tool_call - 工具调用包装")
        # 实际调用工具
        result = handler(request)
        print(f"   工具返回: {result.content}")
        return result

    # 6. after_agent - Agent 结束后（执行 1 次）
    def after_agent(self, state, runtime):
        print("\n" + "=" * 50)
        print("6️⃣ after_agent - Agent 结束")
        print(f"   最终输出: {state['messages'][-1].content[:50]}...")
        print("=" * 50 + "\n")
        return None


# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    middleware=[CompleteMid()]  # 传入中间件实例
)

# 保存图
save_graph_img(agent, "agent.png")

# ============ 执行测试 ============

print("\n🎬 开始执行 Agent...\n")

res = agent.stream(
    input={"messages": [{"role": "user", "content": "现在几点"}]}
)

for chunk in res:
    # 不打印，中间过程由中间件打印
    if 'messages' in chunk:
        pass  # 中间件已经处理了日志

print("\n✨ 执行完成！\n")