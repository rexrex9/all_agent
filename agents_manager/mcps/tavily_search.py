# pip install langchain-mcp-adapters
from langchain_mcp_adapters.client import MultiServerMCPClient
from env.serect import Tavily_SEARCH_KEY
import asyncio


def get_tools():
    client = MultiServerMCPClient(
        {
            "demo": {
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={Tavily_SEARCH_KEY}",
                "transport": "streamable_http",
            }
        },
    )
    tools = asyncio.run(client.get_tools())
    return tools