from langchain.agents.middleware import AgentMiddleware
import subprocess
import re,os
from content.utils import runtime_util as ru

def execute(command: str):
    """
    运行终端命令
    :param command: 命令
    :return: 运行结果
    """
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text= True,
                               encoding='utf-8')
    stdout, stderr = process.communicate()

    s = f'''
    正常输出：{stdout},
    错误输出：{stderr}
    '''
    return s

class ExcuteMiddleware(AgentMiddleware):
    tools = [execute]
    async def awrap_tool_call(self,request,handler):
        if request.tool_call['args'].get('command'): # 通过工具调用时是否存在command这个参数来判断，此时是不是在调用终端命令工具
            request.tool_call['args']['command'] = self._change_command_path(request.tool_call['args']['command'])
        return await handler(request)

    # 1. 用正则识别到路径字符串
    def _find_path(self,text):
        pattern = r'(?:[a-zA-Z]:)?[\\/](?:[^\\/:*?"<>|\s，。；：！？、,;:!?()\[\]{}]+[\\/])*[^\\/:*?"<>|\s，。；：！？、,;:!?()\[\]{}]+(?=[\s，。；：！？、,;:!?()\[\]{}]|$)'
        paths = re.findall(pattern, text)
        return paths

    # 2. 在正则路径字符串替换为加上root_dir的字符串
    def _change_command_path(self,command):
        command = os.path.normpath(command)  # 规划化路径字符串
        paths = self._find_path(command)  # 先找到路径字符串 /aaa/a.py
        for p in paths:
            changed_path = ru.change_file_path( p)
            command = command.replace(p, changed_path)  # 最后把原来的命令字符串中的 路径字符串替换为 root_dir替换后的字符串
        return os.path.normpath(command)  # 规划化路径字符串