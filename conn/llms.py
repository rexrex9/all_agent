from langchain_openai import ChatOpenAI
from base import configs as gc

def get_llm():
    llm = ChatOpenAI(
            #model=gc.BASE_LLM,
            model = "deepseek-ai/DeepSeek-V3.2",
            base_url=gc.BASE_URL,
            temperature=0.1,
        )
    return llm
    # Qwen/Qwen3-30B-A3B-Instruct-2507
    # Qwen/Qwen3-Next-80B-A3B-Instruct
    # Qwen/Qwen3-Coder-30B-A3B-Instruct
    # Qwen/Qwen3-Omni-30B-A3B-Instruct

def get_small_llm():
    llm = ChatOpenAI(
            model='Qwen/Qwen3-30B-A3B-Instruct-2507',
            base_url=gc.BASE_URL,
            temperature=0.1,
        )
    return llm


def get_vlm():
    vlm = ChatOpenAI(
            model=gc.BASE_VLM,
            base_url=gc.BASE_URL,
    )
    return vlm

if __name__ == '__main__':
    # 用于测试
    #from dotenv import load_dotenv
    #load_dotenv()  # 默认加载当前目录下的 .env 文件
    model = get_llm()
    print(model.invoke("你好"))