from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain.tools import tool
import datetime
from conn.llms import get_llm

# ============ 原有工具 ============
@tool
def get_current_time():
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============ 定义中间件注入的工具 ============
@ tool
def log_message(message: str, level: str = "INFO") -> str:
    """记录日志消息"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_text = f"[{timestamp}] [{level}] {message}"
    print(log_text)
    return f"✅ 已记录: {message}"

# ============ 带工具的中间件 ============
class LoggingMiddleware(AgentMiddleware):
    """自动注入日志工具的中间件"""
    # 直接在类属性中定义工具
    tools = [log_message]


# ============ 创建 Agent ============
agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],  # 只传入基础工具
    system_prompt="你是一个助手。当执行重要操作时，使用 log_message 记录日志",
    middleware=[
        LoggingMiddleware()  # 中间件会自动注入 tools
    ]
)

# ============ 执行测试 ============

print("=" * 60)
print("🎬 测试场景：Agent 使用中间件注入的日志工具")
print("=" * 60 + "\n")

response = agent.invoke({
    "messages": [{"role": "user", "content": "现在几点？请记录这次查询"}]
})

print("💬 最终回复")
print(response["messages"][-1].content)

