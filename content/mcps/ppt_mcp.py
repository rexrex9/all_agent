
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from base import config as cfg

def get_tools():
    client = MultiServerMCPClient(
        {
            "ppt-mcp": {
              "transport": "streamable_http",
              "url": cfg.PPT_MCP_URL,
            }
        },
    )
    return asyncio.run(client.get_tools())




if __name__ == "__main__":
    print(get_tools())