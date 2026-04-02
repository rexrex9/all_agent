from deepagents import create_deep_agent
from conn.llms import get_llm
from content.mytools import (gen_image,
                             read_doc_tools,
                             globle_tools as gt,
                             write_doc_tools,
                             vlm_tool)
from content.middles import (wait_rate_limit,
                             file_manager_middle,
                             execute_middle,
                             my_skill_middle)
from content.others import mybackend
from deepagents.backends import FilesystemBackend
from base import configs as gc
import requests


# 如果要搜新闻则先使用get_current_time确认当前时间，
class AllAgent:
    def __init__(self):
        prompt = f'''
        你是一个通用智能体，
        读取ppt,doc,xls,pdf等文件时优先使用get_file_content,
        注意调用write_file与edit_file时，需要有file_path和content参数，content是文件内容，也就是说你需要先写内容，然后调用write_file保存文件，或者用edit_file修改文件；
        注意skill的name并非工具名字。
        做图文需求时,如无特殊说明，则先做md,然后转换为pdf,要特别注意图片引用路径。
        直到完成任务前，都不要停止。
        回答用户用中文。
        '''
        if gc.USE_EXCEL:
            prompt+='''
            做excel的需求则优先使用excel-agent;
            '''
        if gc.USE_PPT:
            prompt+='''
            做ppt的需求则优先使用ppt-agent;
            '''
        if gc.USE_EXCEL or gc.USE_PPT:
            prompt += '''
              交给subagent后需关注其返回结果
              '''

        self.agent = create_deep_agent(
            model=get_llm(), # 传一个llm
            subagents=self._get_subagent(),
            tools=self._get_tools(), # 工具函数列表
            backend=mybackend.create_session_backend,
            middleware=self._get_middlewares(),
            system_prompt=prompt,
        )

    def _get_subagent(self):
        subs = []
        if gc.USE_EXCEL:
            from content.sub_agents import excel_agent
            subs.append(excel_agent.get_agent())
        if gc.USE_PPT:
            from content.sub_agents import ppt_agent
            subs.append(ppt_agent.get_agent())
        return subs

    def _get_tools(self):
        tools = [
            gen_image.generate_image,
            read_doc_tools.get_file_content,
            write_doc_tools.convert_file,
            vlm_tool.get_img_content,
            requests.request
        ]
        tools.extend(gt.get_tools())
        if gc.TAVILY_SEARCH_KEY: # 如果有tavily_search_key则添加tavily_search工具
            from content.mcps import tavily_search
            tools.extend(tavily_search.get_tools)
        return tools

    def _get_middlewares(self):
        return [
            file_manager_middle.FileMiddleware(),
            wait_rate_limit.wait_rate_limit,
            execute_middle.ExecuteMiddleware(), # 终端命令中间件
            # 技能中间件
            my_skill_middle.MySkillMiddleware(backend=FilesystemBackend(root_dir=gc.ROOT_PATH_AGENT),sources=["skills"])
        ]

if __name__ == '__main__':
    agent = AllAgent().agent
    from utils.langchain_utils import stream_util as su
    import asyncio
    while True:
        user = input("用户:")
        asyncio.run(su.astream_both(agent, user))
