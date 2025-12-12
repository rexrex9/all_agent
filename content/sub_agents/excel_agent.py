from conn import llms
from content.mcps import excel_mcp
from content.middles import monitor_tool_middle,wait_rate_limit
def get_agent():
    return {
        "name": "excel-agent",
        "description": "做excel的助手",
        "system_prompt": f"你是一个做excel的助手",
        "middleware":[monitor_tool_middle.monitor_tool,wait_rate_limit.wait_rate_limit] ,
        "tools": excel_mcp.get_tools,
        "model": llms.get_llm()
    }