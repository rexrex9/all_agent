from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call,ModelRequest,ModelResponse
from typing import Callable
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

# 包装整个模型调用
@wrap_model_call
def retry_on_error(request: ModelRequest, handler:Callable[[ModelRequest], ModelResponse])-> ModelResponse:
    """为模型调用添加重试逻辑"""
    max_retries = 3
    for i in range(max_retries):
        try:
            print(f"🔄 模型调用尝试 {i + 1}/{max_retries}")
            response = handler(request)
            print(f"✅ 调用成功")
            return response
        except Exception as e:
            print(f"❌ 调用失败: {e}")
            if i == max_retries - 1:
                raise

# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    # 传入中间件
    middleware=[
        retry_on_error
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