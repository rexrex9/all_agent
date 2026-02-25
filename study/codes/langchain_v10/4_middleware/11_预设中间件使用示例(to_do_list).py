from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from conn.llms import get_llm
from common_utils import save_graph_img

# ============ 定义工具 ============

@tool
def analyze_code(file_path: str) -> str:
    """分析代码质量并发现问题"""
    return f"已分析 {file_path}：发现 3 个代码异味，2 个安全问题"


@tool
def refactor_code(file_path: str, changes: str) -> str:
    """按照指定的更改重构代码"""
    return f"已重构 {file_path}：{changes}"


@tool
def write_tests(file_path: str) -> str:
    """为指定文件编写测试"""
    return f"已为 {file_path} 编写单元测试"


# ============ 创建带 TodoList 的 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[analyze_code, refactor_code, write_tests],
    middleware=[
        TodoListMiddleware()  # 预设的任务列表中间件
    ]
)
save_graph_img(agent, "agent.png")

# ============ 执行复杂的多步骤任务 ============



response = agent.stream({
    "messages": [
        HumanMessage(
            "我需要重构我的认证模块。"
            "首先分析它，然后建议改进，最后实施更改并编写测试。"
        )
    ]
})

# 仅打印 todos
for chunk in response:
    if "tools" in chunk and "todos" in chunk["tools"]:
        print("\n" + "=" * 50)
        print("📝 当前任务列表：")
        print("-" * 50)
        for todo in chunk["tools"]['todos']:
            print(f"- {todo}")