# pip install langchain-mcp-adapters
from conn.llm import get_llm
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "demo_serve": {
            "url": "http://127.0.0.1:8001/mcp",
            "transport": "streamable_http",
        },

    },
)

async def do():
    tools = await client.get_tools()

    agent = create_agent(
        get_llm(),
        tools,
    )
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "现在几点"}]}
    )
    print(response["messages"][-1].content)
if __name__ == "__main__":
    import asyncio
    asyncio.run(do())