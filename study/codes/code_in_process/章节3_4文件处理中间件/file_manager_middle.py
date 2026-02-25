# 过程中代码,可运行位置在 content/middles

import asyncio
import time
from langchain.agents.middleware import AgentState, AgentMiddleware
from utils.doc_utils import os_util as ou
from utils.general_utils.globle_util import get_uuid
from langchain.messages import ToolMessage
from content.utils import runtime_util as rt

class CustomState(AgentState):
    """
    自定义Agent状态类，扩展LangChain的AgentState
    """
    start_work_time: float  # Agent工作开始的时间戳
    file_update_time: float  # 文件最后更新时间戳，用于检测文件变化


class FileMiddleware(AgentMiddleware[CustomState]):

    state_schema = CustomState  # 指定使用的状态类

    def __init__(self):
        super().__init__()

    async def _check_if_new_file(self, folder_path, work_start_time):
        """
        检查文件夹中是否有比指定时间更新的文件

        参数:
        folder_path: str - 要检查的文件夹路径
        work_start_time: float - 参考时间戳

        返回:
        bool: 如果存在比work_start_time更新的文件返回True，否则False
        """
        # 异步执行文件时间检查，避免阻塞事件循环
        max_time = await asyncio.to_thread(ou.get_folder_file_update_time_max, folder_path)
        return max_time > work_start_time  # 比较最新文件时间与参考时间

    async def abefore_model(self, state, runtime):
        """
        Agent调用模型前的钩子函数

        功能: 检查工作目录是否有新文件，如果有则生成目录结构信息
        触发条件: 文件更新时间晚于状态中记录的时间
        """
        DIR_PATH = rt.get_root_thread_dir()  # 获取当前线程的工作目录
        # 检查是否有新文件加入工作目录
        if await self._check_if_new_file(DIR_PATH, state['file_update_time']):
            # 生成美观的目录树结构描述
            content = f'当前目录结构:\n{ou.get_directory_tree(DIR_PATH)}'

            # 返回ToolMessage给模型，包含目录结构信息
            return {
                "messages": [ToolMessage(
                    content=content,
                    tool_call_id=get_uuid(),  # 生成唯一工具调用ID
                    name="summery_file_paths"  # 工具名称
                )],
                "file_update_time": time.time()  # 更新文件检测时间
            }

    async def abefore_agent(self, state, runtime):
        """
        Agent执行前的钩子函数
        """
        # 获取当前时间戳，用于状态管理
        file_update_time = time.time()
        # 没有上传文件时，只更新时间状态
        return {
            "start_work_time": file_update_time,
            "file_update_time": file_update_time
        }

    async def awrap_tool_call(self, request, handler):
        # 执行实际工具调用
        tool_result = await handler(request)

        # 在工具调用后：将绝对路径转换回相对路径
        if isinstance(tool_result, ToolMessage):
            # 只转换内容中的路径，其他信息保持不变
            tool_result.content = rt.get_out_path(tool_result.content)

        return tool_result