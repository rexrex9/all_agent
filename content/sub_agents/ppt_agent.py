from conn import llms
from content.mcps import ppt_mcp
from content.mytools import gen_image
from content.middles import file_manager_middle,wait_rate_limit
def get_agent():
    return {
        "name": "ppt-agent",
        "description": "做ppt的助手",
        "system_prompt": f"你是一个做ppt的助手",
        "middleware":[file_manager_middle.FileMiddleware(),wait_rate_limit.wait_rate_limit] ,
        "tools": ppt_mcp.get_tools + [gen_image.generate_image],
        "model": llms.get_llm()
    }
