# 替代方案：使用LCEL创建异步agent
from major.models_manager import chat_model
from langchain_core.messages import HumanMessage
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
client = MultiServerMCPClient(
    {
        "fetch": {
            "url": "https://mcp.api-inference.modelscope.net/e11004ed8d7d48/mcp",
            "transport": "streamable_http",
        }

    },
)

async def stream_response_async():
    try:
        # 异步获取工具
        tools = await client.get_tools()

        # 获取模型
        model = chat_model.get_model()

        # 使用异步stream
        async for chunk in model.astream(
                [
                    HumanMessage(content="今天特朗普在干嘛"),
                    {"role": "assistant", "content": "让我来搜索一下最新信息..."}
                ],
                tools=tools
        ):
            if hasattr(chunk, 'content'):
                print(chunk.content, end="", flush=True)

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    asyncio.run(stream_response_async())