from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    llm = ChatOpenAI(
        model="Qwen/Qwen3.5-27B",
        #model ="Qwen/Qwen3.5-122B-A10B",
        base_url="https://api.siliconflow.cn/v1"
    )
    return llm


agent = create_deep_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[], # 工具集
    system_prompt="你是一个助手", # 系统提示词
)

# res = agent.stream({"messages":[{"role":"user","content":"写个a.txt,写一句hello world"}]})
# for chunk in res:
#     print(chunk)



