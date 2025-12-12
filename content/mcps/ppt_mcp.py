# https://github.com/samos123/pptx-mcp
from langchain_mcp_adapters.client import MultiServerMCPClient
from content.utils.mcp_tools_util import tools
from base import configs as gc
@ tools
async def get_tools():
    client = MultiServerMCPClient(
        {
            "ppt": {
                "url": gc.PPT_MCP_URL,
                "transport": "streamable_http",
            },
        },
    )
    return await client.get_tools()

if __name__ == '__main__':
    print(get_tools)