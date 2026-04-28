from mcp.server.fastmcp import FastMCP
import datetime
mcp = FastMCP("Demo",host="0.0.0.0",port = 1200)

@ mcp.tool()
def add(a: int, b: int) -> int:
    """两个数相加
    Args:
        a: 第1个加数
        b: 第2个加数
    """
    return a + b

@ mcp.tool()
def current_time():
    """返回当前时间"""
    return datetime.datetime.now()

if __name__ == "__main__":
    mcp.run(transport="sse")