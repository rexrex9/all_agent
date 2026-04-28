from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import datetime

def get_llm():
    llm = ChatOpenAI(
            model="Qwen/Qwen3.5-122B-A10B",
            base_url="https://api.siliconflow.cn/v1",
            temperature=0.1,
        )
    return llm

@ tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

agent = create_agent(
    model=get_llm(), # 传一个llm
    tools=[get_current_time], # 工具函数列表
    system_prompt="你是一个助手", # 系统提示
)