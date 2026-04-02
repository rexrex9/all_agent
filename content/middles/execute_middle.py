from langchain.agents.middleware import AgentMiddleware
from langchain.messages import ToolMessage
import re
from langchain.tools import tool
import subprocess
from content.utils import runtime_util as rt


@ tool
def execute(command: str):
    """
    运行终端命令
    :param command: 命令
    :return: 运行结果
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text= True)
    stdout, stderr = process.communicate()
    s = f'''
    正常输出：{stdout},
    错误输出：{stderr}
    '''
    return s


def find_path(text):
    pattern = r'(?:[a-zA-Z]:)?[\\/](?:[^\\/:*?"<>|\s，。；：！？、,;:!?()\[\]{}]+[\\/])*[^\\/:*?"<>|\s，。；：！？、,;:!?()\[\]{}]+(?=[\s，。；：！？、,;:!?()\[\]{}]|$)'
    paths = re.findall(pattern, text)
    return  paths

def change_command_path(command):
    paths = find_path(command)
    for path in paths:
        changed_path = rt.change_file_path(path)
        command = command.replace(path, changed_path)
    return command

class ExecuteMiddleware(AgentMiddleware):

    tools = [execute]

    def __init__(self):
        """初始化中间件，创建MinIO连接"""
        super().__init__()



    async def awrap_tool_call(self, request, handler):
        field = 'command'
        # 在工具调用前：将相对路径转换为绝对路径
        if field in request.tool_call['args']:
            if request.tool_call['args'][field]:
                # 使用change_file_path将相对路径转为当前线程的绝对路径
                request.tool_call['args'][field] = change_command_path(
                    request.tool_call['args'][field]
                )

        try:
            # 执行实际工具调用
            tool_result = await handler(request)
        except Exception as e:
            # 捕获异常并返回错误信息
            return ToolMessage(
                content=f"Error: {e}",
                tool_call_id=request.tool_call['id'],
                name=request.tool_call['name']
            )

        # 在工具调用后：将绝对路径转换回相对路径
        if isinstance(tool_result, ToolMessage):
            # 只转换内容中的路径，其他信息保持不变
            tool_result.content = rt.get_out_path(tool_result.content)

        return tool_result

if __name__ == '__main__':
    print(change_command_path('python D:/code/langchain-demo/datas/filepaths.py'))