import time,os,asyncio
from conn.minio_conn import MinioConn
from agents_manager.utils import runtime_util as rt
from utils.doc_utils.zip_files import compress_dir
from utils.doc_utils import os_util as ou
from configs.global_configs import ROOT_PATH_SYSTEM
from langchain.agents.middleware import AgentState, AgentMiddleware
from langchain.messages import AIMessage
from utils.general_utils.loggers import logger
class CustomState(AgentState):
    start_work_time: float

class ObjectStorageMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState
    def __init__(self):
        super().__init__()
        self.mc = MinioConn()

    def before_agent(self, state, runtime):
        return {"start_work_time": time.time()}

    async def _check_if_new_file(self,folder_path, work_start_time):
        max_time = await asyncio.to_thread(ou.get_folder_file_update_time_max,folder_path)
        return max_time > work_start_time

    async def aafter_agent(self, state, runtime):
        thread_id = rt.get_thread_id(runtime)
        DIR_PATH = os.path.join(ROOT_PATH_SYSTEM, thread_id)

        if await self._check_if_new_file(DIR_PATH, state['start_work_time']):
            # 压缩目录
            local_p = await asyncio.to_thread(compress_dir,DIR_PATH)
            # 上传文件
            obj_path = os.path.basename(local_p)
            await asyncio.to_thread(self.mc.upload_obj,obj_path,local_p)

            url = self.mc.gen_presigned_url(obj_path)
            return {"messages": [*state['messages'], AIMessage(content='可通过如下地址下载:'), AIMessage(content=url)]}
        else:
            return None

