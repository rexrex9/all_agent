from conn import llm
from langchain.tools import tool
from langchain.agents import create_agent
from deepagents import create_deep_agent
from deepagents import CompiledSubAgent # 从deepagents导入CompiledSubAgent类，用于创建编译后的子代理
import datetime

@ tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_agent():
    # 创建基础的Agent实例
    agent = create_agent(
        model=llm.get_llm(),
        tools=[get_current_time],
        system_prompt="你是一个获取时间的助手"
    )

    # 将基础Agent包装为CompiledSubAgent，使其可以作为子代理被主代理调用
    return CompiledSubAgent(
        name="time-agent",  # 子代理的名称，主代理可以通过此名称调用该子代理
        description="获取时间的助手",  # 子代理的功能描述
        runnable=agent  # 实际执行的Agent实例
    )
