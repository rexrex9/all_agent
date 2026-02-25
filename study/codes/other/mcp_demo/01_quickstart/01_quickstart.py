from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo",host="0.0.0.0",port=1200)

@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数相加"""
    print("正在执行加法运算...")
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """两个数相乘"""
    print("正在执行乘法运算...")
    return a * b

if __name__ == "__main__":
    mcp.run(transport='sse')