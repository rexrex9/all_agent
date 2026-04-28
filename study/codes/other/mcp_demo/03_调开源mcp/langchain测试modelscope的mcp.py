# pip install langchain-mcp-adapters
from conn.llm import get_llm
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "fetch": {
          "transport": "streamable_http",
          "url": "https://mcp.api-inference.modelscope.net/bae2f7018fd944/mcp"
        }
    },
)

async def stream_response():
    tools = await client.get_tools()
    print(tools)

    agent = create_agent(
        get_llm(),
        tools=tools
    )
    response = agent.astream(
        {"messages": [{"role": "user", "content": "给我查查看南京今天到苏州的车票"}]}
    )
    async for chunk in response:
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(stream_response())