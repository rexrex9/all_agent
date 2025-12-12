from langchain_openai import ChatOpenAI
from base import configs as gc
def get_llm():
    # Qwen/Qwen3-30B-A3B-Instruct-2507
    # Qwen/Qwen3-Next-80B-A3B-Instruct
    # Qwen/Qwen3-Coder-30B-A3B-Instruct
    # Qwen/Qwen3-Omni-30B-A3B-Instruct
    llm = ChatOpenAI(
            model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
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
    from dotenv import load_dotenv

    # 加载 .env 文件
    load_dotenv(r'D:\workspace\pythonworkspace\projects\all_agent\.env')  # 默认加载当前目录下的 .env 文件
    print(gc.BASE_URL)
    model = get_llm()
    print(model.invoke("hello world"))