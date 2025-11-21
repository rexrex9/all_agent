from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings,OllamaLLM
def get_deepseek():
    from env import deepseek_envs
    llm = ChatOpenAI(
            model="deepseek-chat",
            base_url="https://api.deepseek.com/v1"
        )
    return llm

def get_embedding_model():
    embd_llm = OllamaEmbeddings(model="nomic-embed-text:latest", base_url="http://localhost:11434")
    return embd_llm

def get_ollama():
    llm = OllamaLLM(
            model="llama3.2:1b",
            base_url="http://localhost:11434"
        )
    return llm

def get_silicon():
    from env import silicon_envs
    # Qwen/Qwen3-30B-A3B-Instruct-2507
    # Qwen/Qwen3-Next-80B-A3B-Instruct
    # Qwen/Qwen3-Coder-30B-A3B-Instruct
    # Qwen/Qwen3-Omni-30B-A3B-Instruct

    llm = ChatOpenAI(
            model="Qwen/Qwen3-30B-A3B-Instruct-2507",
            base_url='https://api.siliconflow.cn/v1',
            temperature=0.1,
        )
    return llm

def get_vlm():
    # deepseek-ai/DeepSeek-OCR
    # Qwen/Qwen3-VL-30B-A3B-Instruct
    from env import silicon_envs
    vlm = ChatOpenAI(
            model="Qwen/Qwen3-VL-30B-A3B-Instruct",
            base_url='https://api.siliconflow.cn/v1',
    )
    return vlm

def get_small_llm():
    from env import silicon_envs
    llm = ChatOpenAI(
            model="Qwen/Qwen3-32B",
            base_url='https://api.siliconflow.cn/v1',
            temperature=0.1,
        )
    return llm

if __name__ == '__main__':
    # emb = get_embedding_model()
    # a = emb.embed_query("hello world")
    # print(len(a))

    llm = get_ollama()
    a = llm.invoke("hello world")
    print(a)
