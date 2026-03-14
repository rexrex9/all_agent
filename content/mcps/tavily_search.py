
# pip install langchain-mcp-adapters
from langchain_mcp_adapters.client import MultiServerMCPClient
from base.configs import TAVILY_SEARCH_KEY
from content.utils.mcp_tools_util import tools


@ tools
async def get_tools():
    client = MultiServerMCPClient(
        {
            "tavily_search": {
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_SEARCH_KEY}",
                "transport": "streamable_http",
            }
        },
    )
    return await client.get_tools()


