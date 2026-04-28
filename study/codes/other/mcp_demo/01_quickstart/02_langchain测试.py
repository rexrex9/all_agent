# pip install langchain-mcp-adapters
from conn.llm import get_llm
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent



client = MultiServerMCPClient(
    {
        "aaa": {
            "url": "http://127.0.0.1:1200/sse",
            "transport": "sse",
        },
    },
)

async def do():
    tools = await client.get_tools()# 获取MCP工具,是一个异步方法

    agent = create_agent(
        get_llm(),
        tools=tools
    )
    # 并且mcp的工具本身也都是异步工具，所以agent在调用时必须异步调用，ainvode或者astream
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "现在几点"}]}
    )
    print(response["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(do())