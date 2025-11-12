from agents_manager.mcps import tavily_search
from conn import llms
from configs.global_configs import WORK_P
def get_agent():
    return {
        "name": "network-agent",
        "description": "网络搜索相关的Agent,可以做网络所搜，提取等",
        "system_prompt": f"你是一位出色的网络搜索相关助手,工作路径在{WORK_P}",
        "tools": tavily_search.get_search_tools(),
        "model": llms.get_silicon()
    }