from langchain.agents import create_agent
import mytools as mt
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import TodoListMiddleware

def get_llm():
    llm = ChatOpenAI(
        model="Qwen/Qwen3.5-27B",
        #model ="Qwen/Qwen3.5-122B-A10B",
        base_url="https://api.siliconflow.cn/v1"
    )
    return llm


agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[mt.read_file, mt.write_file, mt.ls], # 工具集
    middleware=[TodoListMiddleware()],
    system_prompt="你是一个助手", # 系统提示词

)

# res = agent.stream({"messages":[{"role":"user","content":"做个小网站，html,css,script脚本分开写"}]})
# for chunk in res:
#     print(chunk)



