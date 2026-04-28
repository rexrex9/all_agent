from deepagents import create_deep_agent
from conn.llm import get_llm
import subprocess
from deepagents.backends.filesystem import FilesystemBackend


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

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/",virtual_mode= True),
    skills=["skills"],
    model=get_llm(),
    tools= [execute],
    system_prompt=""",
    注意:
    1. skill的name并非工具名字。
    """
)

for chunk in agent.stream({"messages": [{"role": "user", "content": "现在几点？"}]}):
    print(chunk)


# from utils.langchain_utils import stream_util as su
#
# while True:
#     user = input("用户:")
#     su.stream_both(agent,user)
