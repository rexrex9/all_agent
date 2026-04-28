# 连接大模型的脚本
# conn的作用从文件夹管理角度来说用来存放连接外部服务的脚本的
from langchain_openai import ChatOpenAI

# 作用：在项目根目录中找名为”.env"的文件，读取里面的内容，并加载到环境变量中。
from base import config as cfg
def get_llm():
    llm = ChatOpenAI(
        model=cfg.BASE_LLM,
        #model = 'Qwen/Qwen3.5-9B',
        base_url=cfg.MODEL_API_BASE_URL
    )
    return llm
    # model ="Qwen/Qwen3.5-122B-A10B",

def get_vlm():
    vlm = ChatOpenAI(
        model=cfg.BASE_VLM,
        base_url=cfg.MODEL_API_BASE_URL
    )
    return vlm

if __name__ == "__main__":
    llm = get_llm()
    #llm = llm.bind_tools([get_current_weather])
    res = llm.invoke("你好？")
    print(res)


