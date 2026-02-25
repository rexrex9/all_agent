from langchain.agents import create_agent
from file_tools import *
from langchain.agents.middleware import TodoListMiddleware
from langchain_openai import ChatOpenAI

def get_llm():
    llm = ChatOpenAI(
            model="Qwen/Qwen3-Next-80B-A3B-Instruct",
            base_url="https://api.siliconflow.cn/v1",
            temperature=0.1,
        )
    return llm


agent = create_agent(
    model=get_llm(), # 传一个llm
    tools=[write_file, read_file, list_files], # 工具函数列表
    system_prompt="你是一个助手", # 系统提示
    middleware=[TodoListMiddleware()]
)