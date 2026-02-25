from langchain.agents.middleware import AgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from conn.llms import get_llm


# ============ 极简任务工具 ============
tasks = {}  # 存储所有任务


@tool
def create_task(goal: str) -> str:
    """创建一个新任务"""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = {
        "goal": goal,
        "status": "待处理",
        "steps": []
    }
    return f"✅ 创建任务: {goal} (ID: {task_id})"


@tool
def update_status(task_id: str, status: str) -> str:
    """更新任务状态: 待处理/进行中/已完成"""
    if task_id in tasks:
        tasks[task_id]["status"] = status
        return f"✅ {task_id} 状态更新为: {status}"
    return f"❌ 任务不存在"


@tool
def list_tasks() -> str:
    """列出所有任务"""
    if not tasks:
        return "📭 暂无任务"

    result = "📋 当前任务:\n"
    for task_id, task in tasks.items():
        result += f"  • {task['goal']} [{task_id}] - {task['status']}\n"
    return result


# ============ 极简中间件 ============
class TaskMiddleware(AgentMiddleware):
    """极简任务中间件"""

    tools = [create_task, update_status, list_tasks]

    def __init__(self):
        print("🔧 任务中间件已加载")


# ============ 使用示例 ============



agent = create_agent(
    model=get_llm(),
    tools=[],  # 你的其他工具
    middleware=[TaskMiddleware()],
    system_prompt="你可以用create_task创建任务，用update_status更新状态"
)


res = agent.stream({
    "messages": [
        HumanMessage(content="学习python")
    ]
})

for chunk in res:
    print(chunk)