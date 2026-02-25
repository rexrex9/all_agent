
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo",host="0.0.0.0",port = 8000)



@mcp.tool(description="两个数相加的工具")
def add(a: int, b: int) -> int:
    """两个数相加
    Args:
        a: 第一个加数
        b: 第二个加数
    """
    return a + b


@mcp.resource("greeting://{name}") # 定义资源
def get_greeting(name: str) -> str:
    return f"你好你好你好你好, {name}!"




@mcp.prompt() # 定义prompt
def greet_user() -> str:
    prompt = '''
    先跟用户打招呼，并且用greeting://{name}里的打招呼模板。再回答用户问题。
    '''
    return prompt


if __name__ == "__main__":
    mcp.run(transport='streamable-http')