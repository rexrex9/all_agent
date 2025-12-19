from conn import llms
from content.mcps import excel_mcp
from content.middles import file_manager_middle,wait_rate_limit
def get_agent():
    return {
        "name": "excel-agent",
        "description": "做excel的助手",
        "system_prompt": f"你是一个做excel的助手",
        "middleware":[file_manager_middle.FileMiddleware(),wait_rate_limit.wait_rate_limit] ,
        "tools": excel_mcp.get_tools,
        "model": llms.get_llm()
    }