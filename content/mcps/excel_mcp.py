from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


def get_tools():
    client = MultiServerMCPClient(
        {
            "excel": {
              "command": "uvx",
              "args": ["--index-url", "https://pypi.tuna.tsinghua.edu.cn/simple", "excel-mcp-server", "stdio"],
              "transport": "stdio",
            }
        },
    )
    return asyncio.run(client.get_tools())


if __name__ == "__main__":
    print(get_tools())
