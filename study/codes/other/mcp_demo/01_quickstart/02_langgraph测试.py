# pip install langchain-mcp-adapters
from conn.llms import get_llm
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "demo": {
            "url": "http://127.0.0.1:8000/sse",
            "transport": "sse",
        }
    },
)


async def do():
    tools = await client.get_tools()# 获取MCP工具
    agent = create_agent(
        get_llm(),
        tools=tools
    )
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "2*3等于几"}]}
    )
    print(response["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(do())