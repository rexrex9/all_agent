# pip install langchain-mcp-adapters
import os

from conn.llm import get_llm
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.tools import tool

from dotenv import load_dotenv
load_dotenv()

client = MultiServerMCPClient(
    {
        "fetch": {
          "transport": "streamable_http",
          "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_SEARCH_KEY')}"
        }
    },
)
import datetime
@ tool
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

async def stream_response():
    tools = await client.get_tools()
    print(tools)
    tools.append(get_current_time)
    print(tools)
    agent = create_agent(
        get_llm(),
        tools=tools,
        system_prompt="搜新闻时先用工具确认一下今天是哪天。"
    )
    response = agent.astream(
        {"messages": [{"role": "user", "content": "特朗普今天在干嘛"}]}
    )
    async for chunk in response:
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(stream_response())