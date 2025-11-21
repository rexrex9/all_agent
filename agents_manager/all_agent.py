from deepagents import create_deep_agent
from conn.llms import get_silicon
from agents_manager.mytools import gen_image,read_doc_tools,globle_tools as gt
#from agents_manager.mcps import tavily_search
#from agents_manager.sub_agents import ppt_agent
from agents_manager.middles import object_storage_middle,wait_rate_limit,file_download_middle
from agents_manager.others import mybackend
from utils.general_utils.loggers import logger
import asyncio



class ReceptionAgent:
    def __init__(self):
        prompt = f'''
        你是一个通用智能体，
        '''

        #写ppt的需求则先基于python - pptx写python脚本，然后终端运行python脚本生成ppt, 注意生成的ppt也许在工作路径下
        self.agent = create_deep_agent(
            model=get_silicon(), # 传一个llm
            #subagents=self._get_subagent(),
            tools=self._get_tools(), # 工具函数列表
            backend=mybackend.create_session_backend,
            middleware=self._get_middlewares(),
            system_prompt=prompt,
        )

    def _get_subagent(self):
        return [ppt_agent.get_agent()]

    def _get_tools(self):
        tools = [gen_image.generate_image,read_doc_tools.get_file_content]
        tools.extend(gt.get_tools())
        #tools.extend(tavily_search.get_tools())
        return tools

    def _get_middlewares(self):
        return [
            file_download_middle.FileDownloadMiddleware(),
            object_storage_middle.ObjectStorageMiddleware(),
            #warp_vlm.call_vlm,
            #wait_rate_limit.wait_rate_limit,
        ]

    def chat(self,messages):
        res = self.agent.stream({"messages": messages},
            stream_mode = ["updates","messages"])
        return res

    def steam_try(self,user_input,thread_id):
        messages = [{"role": "user", "content": user_input}]
        return self.agent.astream({"messages": messages},config={"configurable":{"thread_id":thread_id}})

if __name__ == '__main__':
    from utils.general_utils.steam_util import astream_print_log

    agent = ReceptionAgent()

    p = '''
    做一个a.txt,随便写点什么
    '''
    #p = r'D:\agent_file_system'
    asyncio.run(astream_print_log(agent.steam_try(p,"ssss")))
    #from langchain.messages import HumanMessage
    #HumanMessage(content=p)
    #agent.agent.stream({"messages": [{"role": "user", "content": p}]},)

