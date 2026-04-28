
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from base import config as cfg


def get_tools():
    client = MultiServerMCPClient(
        {
            "tavily": {
              "transport": "streamable_http",
              "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={cfg.TAVILY_SEARCH_KEY}"
            }
        },
    )
    return asyncio.run(client.get_tools())