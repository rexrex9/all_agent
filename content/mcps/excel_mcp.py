# https://github.com/haris-musa/excel-mcp-server
from langchain_mcp_adapters.client import MultiServerMCPClient
from content.utils.mcp_tools_util import tools

@ tools
async def get_tools():
    client = MultiServerMCPClient(
        {
            "excel": {
                "command": "uvx",
                "args": [
                    "--index-url", "https://pypi.tuna.tsinghua.edu.cn/simple",
                    "excel-mcp-server",
                    "stdio"
                ],
                "transport": "stdio",
              }
        },
    )
    return await client.get_tools()
