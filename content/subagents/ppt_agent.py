from conn import llm
from content.mcps import ppt_mcp
from content.middles import file_manager_middle,wait_rate_limit
from content.mytools import gen_image
def get_agent():
    return {
        "name": "ppt-agent",
        "description": "制作PPT的助手",
        "system_prompt": "你是一个制作PPT的助手",
        "tools": ppt_mcp.get_tools()+[gen_image.generate_image],
        "model": llm.get_llm(),
        "middleware" : [file_manager_middle.FileManagerMiddleware(),wait_rate_limit.wait_rate_limit]
    }