import os,asyncio
from content.utils import runtime_util as rt
from base.configs import USER_UPLOAD_PATH
from langchain.agents.middleware import AgentState, AgentMiddleware
from content.utils import base64_util as bu
from utils.general_utils.loggers import logger
from utils.doc_utils import os_util as ou
from utils.general_utils.globle_util import get_uuid
from langchain.messages import ToolMessage,AIMessage
from utils.doc_utils.zip_files import compress_dir
from conn.minio_conn import MinioConn

import time
class CustomState(AgentState):
    upload_files: list
    start_work_time: float
    file_update_time: float
    uploaded: bool
class FileMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState
    def __init__(self):
        super().__init__()
        self.mc = MinioConn()

    async def _check_if_new_file(self,folder_path, work_start_time):
        max_time = await asyncio.to_thread(ou.get_folder_file_update_time_max,folder_path)
        return max_time > work_start_time

    async def abefore_model(self, state, runtime):
        DIR_PATH = rt.get_root_thread_dir()
        if await self._check_if_new_file(DIR_PATH, state['file_update_time']):
            content = f'当前目录结构:\n{ou.get_directory_tree(DIR_PATH)}'
            return {"messages": [ToolMessage(content=content,tool_call_id=get_uuid(),name="summery_file_paths")],
                    "file_update_time":time.time()}

    async def abefore_agent(self, state, runtime):
        #logger.info(state)
        file_update_time = time.time()
        dir_path = rt.change_file_path(USER_UPLOAD_PATH)
        await asyncio.to_thread(os.makedirs,dir_path, exist_ok=True)
        files = state.get('upload_files')
        if files:
            content = f'用户上传了如下文件,已下载,文件路径如下:'
            for file in files:
                r = await asyncio.to_thread(bu.save_base64_file_from_content_block,file,dir_path)
                content += f"\n{rt.get_out_path(r['file_path'])}"
            return {"messages": [ToolMessage(content=content,tool_call_id=get_uuid(),name="file_upload")],
                    "upload_files":None,
                    "uploaded":True,
                    "start_work_time":time.time(),
                    "file_update_time":file_update_time}
        else:
            return {"start_work_time": file_update_time,"file_update_time":file_update_time}
    async def aafter_agent(self, state, runtime):
        logger.info( state)


        DIR_PATH = rt.get_root_thread_dir()
        if await self._check_if_new_file(DIR_PATH, state['start_work_time']):
            # 压缩目录
            local_p = await asyncio.to_thread(compress_dir,DIR_PATH)
            # 上传文件
            obj_path = os.path.basename(local_p)
            await asyncio.to_thread(self.mc.upload_obj,obj_path,local_p)

            url = self.mc.gen_presigned_url(obj_path)
            return {"messages": [AIMessage(content='可通过如下地址下载:'), AIMessage(content=url)]}
        else:
            return None


    # 调用工具前后改变路径
    async def awrap_tool_call(self,request, handler):
        filepath_fields = ['filepath', 'filename', 'image_path', 'reference_image_path']
        for field in filepath_fields:  # 把文件路径转换成绝对路径
            if field in request.tool_call['args']:
                if request.tool_call['args'][field]:
                    request.tool_call['args'][field] = rt.change_file_path(request.tool_call['args'][field])
        tool_result = await handler(request)  # 执行工具得到结果

        if isinstance(tool_result, ToolMessage):  # 把文件路径转换成相对路径
            tool_result.content = rt.get_out_path(tool_result.content)

        return tool_result