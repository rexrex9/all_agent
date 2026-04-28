from mcp.server.fastmcp import FastMCP
import datetime
mcp = FastMCP("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数相加"""
    print("正在执行加法运算...")
    return a + b

@mcp.tool()
def current_time():
    """返回时间的工具"""
    print("正在获取时间...")
    return datetime.datetime.now()

if __name__ == "__main__":
    print(1)
    mcp.run(transport='stdio')
    print(2)