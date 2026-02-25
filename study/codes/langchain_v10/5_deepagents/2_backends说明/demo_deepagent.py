from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import datetime
import dotenv
dotenv.load_dotenv()

from deepagents.backends import FilesystemBackend # 导入FilesystemBackend

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
    model=get_llm(),
    tools=[],
    system_prompt="你是一个助手",
    backend=FilesystemBackend(root_dir="/agent_files",virtual_mode=True) # 设置后端
)

if __name__ == '__main__':
    for chunk in agent.stream({"messages": [{"role": "user", "content": "做个b.txt,写个hello world."}]}):
        print( chunk)