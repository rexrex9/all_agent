from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import datetime
import dotenv
dotenv.load_dotenv()

def get_llm():
    llm = ChatOpenAI(
            model="Qwen/Qwen3-Next-80B-A3B-Instruct",
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




agent = create_deep_agent(
    model=get_llm(), # 传一个llm
    tools=[], # 工具函数列表
    system_prompt="你是一个助手"# 系统提示
)

if __name__ == '__main__':
    res = agent.invoke(
        input={"messages": [{"role": "user", "content": "现在几点"}]} # 用户输入
    )
    print(res["messages"][-1].content) # 打印AI的回复