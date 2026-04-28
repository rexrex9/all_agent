from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    llm = ChatOpenAI(
        model="Qwen/Qwen3.5-27B",
        #model ="Qwen/Qwen3.5-122B-A10B",
        base_url="https://api.siliconflow.cn/v1"
    )
    return llm

# deepagent的文件管理主要是通过filesystem_middleware来实现的
# filesystem_middleware中有个关键参数就是backend,它指向的后端系统

agent = create_deep_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    backend=FilesystemBackend(root_dir="/agent_files",virtual_mode=True)
)

# res = agent.stream({"messages":[{"role":"user","content":"写个a.txt,写一句hello world"}]})
# for chunk in res:
#     print(chunk)



