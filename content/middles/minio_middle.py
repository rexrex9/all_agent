from langchain.agents.middleware import AgentMiddleware
from utils.doc_utils import os_utils as ou
from content.utils import runtime_util as ru
from langchain.messages import AIMessage
import os
from langchain.agents import AgentState
from utils.doc_utils import zip_files
from conn.minio_conn import MinioConn
from base import config as cfg
import asyncio
import time
from utils.general_utils.loggers import logger

class MinioState(AgentState):
    work_start_time: float
class MinioMiddle(AgentMiddleware):
    state_schema = MinioState
    def __init__(self):
        super().__init__()
        self.mc = MinioConn()
        self.mc.create_bucket_if_not_exists(cfg.MINIO_BUCKET)  # 创建存储桶
    async def abefore_agent(self, state,runtime):
        return {'work_start_time':time.time()} # 每次Agent开始工作时，把当前时间记录到状态中

    async def aafter_agent(self, state, runtime):
        session_path = ru.get_thread_dir()
        if os.path.exists(session_path) and ou.get_max_update_time(session_path,[cfg.USER_UPLOAD_DIR,os.path.join(cfg.SKILL_DIR_PATH,'skill-creator')])>state['work_start_time']: # 如果这个目录存在
            # 对比工作目录的更新时间于状态中的工作开始时间即可。
            # 1. 把线程目录打包成zip
            local_zip_path = await asyncio.to_thread(zip_files.zip_folder,session_path)
            # 2. 上传minio
            object_name = f'{ru.get_thread_id()}.zip'
            await asyncio.to_thread(self.mc.upload_file, cfg.MINIO_BUCKET, object_name, local_zip_path)
            # 3. 得到下载链接
            download_url = self.mc.get_download_url(cfg.MINIO_BUCKET, object_name)
            # 4. 把下载链接封装一个AIMessage并到 messages里去
            download_markdown = f"[点击下载文件]({download_url})"
            return {'messages': [AIMessage(content=download_markdown)]}

