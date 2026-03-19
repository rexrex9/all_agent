from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from tool import execute
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()  # 默认加载当前目录下的 .env 文件
def get_llm():
    llm = ChatOpenAI(
            model = "deepseek-ai/DeepSeek-V3.2",
            base_url="https://api.siliconflow.cn/v1",
            temperature=0.1,
        )
    return llm

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/agent_files"),
    skills=["skills"],
    model=get_llm(),
    tools= [execute],
    system_prompt="""
    注意:
    1. skill的name并非工具名字。
    2. 直到满足用户需求前都不要停止。
    """
    #     2. 你在windows环境中
)

result = agent.stream(
    {"messages": [{"role": "user", "content": "现在几点？"}]},
    config={"configurable": {"thread_id": "1"}},
)

for i in result:
    print(i)