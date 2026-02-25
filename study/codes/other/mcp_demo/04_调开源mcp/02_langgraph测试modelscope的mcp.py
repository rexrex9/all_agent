# pip install langchain-mcp-adapters
from major.models_manager import chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "bing-cn-mcp-server": {
          "transport": "streamable_http",
          "url": "https://mcp.api-inference.modelscope.net/541f75f2102d44/mcp"
        }
    },
)


async def stream_response():
    tools = await client.get_tools()
    print(tools)

    agent = create_react_agent(
        chat_model.get_model(),
        tools=tools
    )
    response = agent.astream(
        {"messages": [{"role": "user", "content": "今天特朗普在干嘛"}]}
    )
    async for chunk in response:
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(stream_response())