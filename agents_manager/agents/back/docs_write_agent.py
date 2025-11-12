from agents_manager.mytools import terminal_control
from conn import llms
from configs.global_configs import WORK_P
def get_agent():
    return {
        "name": "docs-write-agent",
        "description": "写各种文档的助手例如pdf,docx,ppt等",
        "system_prompt": f"先写md格式文件，工作路径在{WORK_P},然后使用pandoc命令转换成指定的文件，注意中文字体问题",
        "tools": [terminal_control.run_command],
        "model": llms.get_silicon()
    }