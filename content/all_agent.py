from deepagents import create_deep_agent
from conn.llm import get_llm
from base import config as cfg
from content.others import mybackend
#from content.others import mybackend_easy
from content.mytools import globle_tools as gt,read_doc_tools as rdt,write_doc_tools as wdt
from content.mytools import vlm_tool,gen_image
from content.middles.file_manager_middle import FileManagerMiddleware
from content.middles.minio_middle import MinioMiddle
from content.middles.wait_rate_limit import wait_rate_limit
from content.middles.excute_middle import ExcuteMiddleware
from content.middles import my_skill_middle
from content.mcps import travily_search
if cfg.USE_EXCEL:
    from content.subagents import excel_agent
if cfg.USE_PPT:
    from content.subagents import ppt_agent

class AllAgent():

    def __init__(self):
        prompt = f'''
         你是一个通用智能体，
         要执行终端命令操作，则使用execute工具，
         搜新闻时先用工具确认一下今天是哪天。
         读取ppt,doc,xls,pdf等文件时优先使用get_file_content,
         做图文需求时,如无特殊说明，则先做md,然后转换为pdf,要特别注意图片引用路径。
         直到完成任务前，都不要停止。
         回答用户用中文。
         '''
        if cfg.USE_EXCEL:
            prompt+='\n制作Excel的需求，优先使用子代理中的excel-agent。'
        if cfg.USE_PPT:
            prompt+='\n制作PPT的需求，优先使用子代理中的ppt-agent。注意：ppt-agent不是工具的名字，它是子智能体的名字，调工具应该是调用名为task的工具。'

        self.agent = create_deep_agent(
            model=get_llm(), # 模型, 传一个llm实例
            tools=self._get_tools(), # 工具集
            system_prompt=prompt, # 系统提示词
            backend=mybackend.backend_factory,
            middleware=self._get_middles(),
            subagents = self._get_subagents()
        )

    def _get_middles(self):
        middles = [FileManagerMiddleware(), wait_rate_limit, MinioMiddle(), ExcuteMiddleware()]
        middles.append(my_skill_middle.MySkillsMiddleware(backend=mybackend.backend_factory, sources=[cfg.SKILL_DIR_PATH]))
        return middles


    def _get_tools(self):
        tools = [gt.get_current_time, rdt.get_file_content, wdt.convert_file]
        tools.append(vlm_tool.read_image)
        tools.append(gen_image.generate_image)
        if cfg.TAVILY_SEARCH_KEY: # 是否存在TAVILY_SEARCH_KEY来开关这个功能
            tools.extend(travily_search.get_tools())
        return tools

    def _get_subagents(self):
        subagent = []
        if cfg.USE_EXCEL:
            subagent.append(excel_agent.get_agent())
        if cfg.USE_PPT:
            subagent.append(ppt_agent.get_agent())
        return subagent








if __name__ == '__main__':
    agent = AllAgent().agent
    # from utils.langchain_utils.common_utils import save_graph_img
    # save_graph_img(agent, "all_agent.png")
    from utils.langchain_utils import stream_util as su
    m = su.Memery()
    # 控制台agent聊天工具，控制台只输出AI的回复。日志文件里记录Agent
    while True:
        user_input = input("用户：")
        m.stream_both_with_memory(agent, user_input)
        print()


