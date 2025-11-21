from agents_manager.mytools import terminal_control
from conn import llms
from configs.global_configs import ROOT_PATH_AGENT
from deepagents.backends import FilesystemBackend
def get_agent():
    return {
        "name": "ppt-agent",
        "description": "写ppt的助手",
        "system_prompt": f"你是一个做ppt的助手，工作路径在{ROOT_PATH_AGENT},先根据用户需求基于python-pptx写python脚本，然后终端运行python脚本生成ppt",
        "backend":FilesystemBackend(root_dir=ROOT_PATH_AGENT),
        "tools": [terminal_control.run_command],
        "model": llms.get_silicon()
    }