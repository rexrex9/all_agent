from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import AgentMiddleware, AgentState
import datetime
from conn.llms import get_llm


# ============ 自定义 State ============

class CustomState(AgentState):
    """自定义 State，添加统计字段"""
    model_call_count: int  # 自定义：模型调用次数

# ============ 定义工具 ============

@tool
def get_current_time():
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============ 可配置的类式中间件 ============

class CallCounterMiddleware(AgentMiddleware):
    """调用次数统计中间件 - 支持配置和状态管理"""
    state_schema = CustomState
    def __init__(self, max_model_calls=2):
        """
        初始化配置
        :param max_model_calls: 最大模型调用次数
        """
        self.max_model_calls = max_model_calls
        print(f"📊 调用计数器已启用")


    def before_model(self, state, runtime):
        """模型调用前 - 记录即将调用"""
        current_count = state.get('model_call_count', 0)
        print(f"🤖 模型调用 #{current_count + 1}")
        return {"model_call_count": current_count + 1}

    def after_model(self, state, runtime):
        """模型调用后 - 更新统计并检查限制"""

        # 打印统计
        print(f"✅ 模型调用完成")
        print(f"   累计模型调用: {state['model_call_count']} 次")

        # 检查是否超限
        if state['model_call_count'] >= self.max_model_calls:
            print(f"⚠️  警告: 模型调用次数已达上限 {self.max_model_calls} 次!")

        print()
        return None


# ============ 创建 Agent ============

agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    system_prompt="你是一个助手",
    middleware=[
        # 配置调用次数限制
        CallCounterMiddleware(
            max_model_calls=2,  # 最多调用 2 次
        )
    ]
)


# ============ 执行测试 ============

print("=" * 50)
print("🎬 开始执行 Agent")
print("=" * 50 + "\n")

res = agent.stream(
    input={
        "messages": [{"role": "user", "content": "现在几点"}],
        "model_call_count": 0,  # 初始化模型调用次数
    }
)

for chunk in res:
    # 流式输出，中间件会打印统计信息
    pass

print("=" * 50)
print("✨ 执行完成")
print("=" * 50)