from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.tools import tool
import datetime
from conn.llms import get_llm
from common_utils import save_graph_img

# ============ 定义工具 ============
@tool
def get_current_time():
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============ 创建 Agent（使用预设的 ModelCallLimitMiddleware） ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    middleware=[
        ModelCallLimitMiddleware(
            run_limit=2,          # 单次执行最多调用次数(可手动调整该值体验)
            exit_behavior="end"   # 达到限制时优雅退出（或用 "error" 抛出异常）
        )
    ]
)

save_graph_img(agent, "agent.png")

# ============ 执行测试 ============
result = agent.invoke(
    {"messages": [{"role": "user", "content": "现在几点？"}]},
)
print(f"📤 最终回复: {result['messages'][-1].content}\n")



