from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import before_agent, after_agent, before_model,after_model, wrap_model_call, wrap_tool_call
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

# 1. @before_agent - 在 Agent 执行前运行
@before_agent
def log_agent_start(state,runtime):
    """在 Agent 开始执行前记录日志"""
    print(f"🚀 Agent 开始执行")
    print(f"📥 输入消息: {state['messages'][-1]['content']}")
    return state  # 可以修改 state


# 2. @after_agent - 在 Agent 执行后运行
@after_agent
def log_agent_end(state,runtime):
    """在 Agent 执行完成后记录日志"""
    print(f"✅ Agent 执行完成")
    print(f"📤 输出消息: {state['messages'][-1]['content']}")
    return state  # 可以修改 state


# 3. @before_model - 在调用 LLM 前运行
@before_model
def log_model_input(messages):
    """在调用模型前记录输入"""
    print(f"🤖 准备调用模型")
    print(f"💬 输入消息数: {len(messages)}")
    return messages  # 可以修改消息


# 4. @after_model - 在调用 LLM 后运行
@after_model
def log_model_output(response):
    """在模型返回后记录输出"""
    print(f"🤖 模型返回结果")
    print(f"📝 响应内容: {response.content[:50]}...")  # 只显示前50字符
    return response  # 可以修改响应


# 5. @wrap_model_call - 包装整个模型调用
@wrap_model_call
def retry_on_error(call_model, messages):
    """为模型调用添加重试逻辑"""
    max_retries = 3
    for i in range(max_retries):
        try:
            print(f"🔄 模型调用尝试 {i + 1}/{max_retries}")
            response = call_model(messages)
            print(f"✅ 调用成功")
            return response
        except Exception as e:
            print(f"❌ 调用失败: {e}")
            if i == max_retries - 1:
                raise


# 6. @wrap_tool_call - 包装工具调用
@wrap_tool_call
def log_tool_execution(call_tool, tool_name, tool_input):
    """记录工具调用的详细信息"""
    print(f"🔧 开始调用工具: {tool_name}")
    print(f"📥 工具输入: {tool_input}")

    result = call_tool(tool_name, tool_input)

    print(f"📤 工具输出: {result}")
    return result


# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    # 传入中间件
    middleware=[
        log_agent_start,
        log_agent_end,
        log_model_input,
        log_model_output,
        retry_on_error,
        log_tool_execution,
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