#from env import anthropic_env
from deepagents import create_deep_agent
from conn.llms import get_silicon
from agents_manager.mytools import terminal_control,gen_image
from agents_manager.mcps import tavily_search
from agents_manager.agents import minio_agent
from agents_manager.middles import wait_rate_limit,query_change
from deepagents.backends import FilesystemBackend
from configs.global_configs import WORK_P
import asyncio

class ReceptionAgent:
    def __init__(self):

        prompt = f'''
        你是一个通用智能体,工作路径在{WORK_P}，
        遇到写文件相关需求时，先写md文件，然后可通过pandoc命令转换成指定的文件，注意中文字体问题。
        但一般情况下不用转换，直接输出md即可。
        
        提示：把用户要的文件利用子agent"minio-agent"上传至对象存储数据库，然后把下载路径给用户
        '''

        self.agent = create_deep_agent(
            model=get_silicon(), # 传一个llm
            subagents=self._get_subagent(),
            tools=self._get_tools(), # 工具函数列表
            backend=FilesystemBackend(root_dir=WORK_P),
            middleware=self._get_middlewares(),
            system_prompt=prompt
        )

    def _get_subagent(self):
        return [minio_agent.get_agent()]

    def _get_tools(self):
        tools = [terminal_control.run_command]
        tools.extend(tavily_search.get_search_tools())
        tools.append(gen_image.generate_image)
        return tools

    def _get_middlewares(self):
        return [query_change.query_change,
                wait_rate_limit.wait_rate_limit]

    def chat(self,messages):
        res = self.agent.stream({"messages": messages},
            stream_mode = ["updates","messages"])
        return res

    def steam_try(self,user_input):
        messages = [{"role": "user", "content": user_input}]
        return self.agent.astream({"messages": messages})

if __name__ == '__main__':
    from utils.general_utils.steam_util import astream_print_log
    print(2)
    agent = ReceptionAgent()
    print(1)
    p = '''
    把这个内容给我整理成一个笔记
    https://docs.siliconflow.cn/cn/userguide/capabilities/multimodal-vision
    '''
    #p = r'D:\agent_file_system'
    asyncio.run(astream_print_log(agent.steam_try(p)))

