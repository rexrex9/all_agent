from agents_manager.mytools import minio_tools
from conn import llms
from configs.global_configs import WORK_P
def get_agent():
    return {
        "name": "minio-agent",
        "description": "控制minio的agent",
        "system_prompt": f"你是一位出色的minio管理助手,工作路径在{WORK_P},存于minio后会把下载地址返回",
        "tools": minio_tools.get_minio_tools(),
        "model": llms.get_silicon()
    }