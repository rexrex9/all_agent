import datetime
from langchain.tools import tool
import subprocess

@tool
# 获得当前时间的函数
def get_current_time():
    """
    获取当前时间
    :return: 当前时间
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

@ tool
# 终端运行函数
def run_command(command: str):
    """
    运行终端命令
    :param command: 命令
    :return: 运行结果
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8',text= True)
    stdout, stderr = process.communicate()
    s = f'''
    正常输出：{stdout},
    错误输出：{stderr}
    '''
    return s






