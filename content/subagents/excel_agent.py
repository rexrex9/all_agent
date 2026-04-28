from conn import llm
from content.mcps import excel_mcp
from content.middles import file_manager_middle,wait_rate_limit

def get_agent():
    return {
        "name": "excel-agent",
        "description": "制作Excel的助手",
        "system_prompt": "你是一个制作Excel的助手",
        "tools": excel_mcp.get_tools(),
        "model": llm.get_llm(),
        "middleware" : [file_manager_middle.FileManagerMiddleware(),wait_rate_limit.wait_rate_limit]
    }