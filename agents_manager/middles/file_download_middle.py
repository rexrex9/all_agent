import os,asyncio
from agents_manager.utils import runtime_util as rt
from configs.global_configs import ROOT_PATH_SYSTEM,USER_UPLOAD_PATH
from langchain.agents.middleware import AgentState, AgentMiddleware
from utils.doc_utils import base64_util as bu
from utils.general_utils.loggers import logger
from utils.general_utils.globle_util import get_uuid
from langchain.messages import ToolMessage

class CustomState(AgentState):
    start_work_time: float
    files: list

class FileDownloadMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState
    def __init__(self):
        super().__init__()

    async def abefore_agent(self, state, runtime):
        logger.info(state)
        files = state.get('files')
        dir_path = os.path.join(ROOT_PATH_SYSTEM, rt.get_thread_id(runtime), USER_UPLOAD_PATH)
        await asyncio.to_thread(os.makedirs, dir_path, exist_ok=True)
        if files:
            content = f'用户上传了如下文件,已下载至{dir_path}:'
            for file in files:
                await asyncio.to_thread(bu.save_base64_file_from_content_block,file,dir_path)
                content += f'\n{file["metadata"]["filename"]}'
            return {"messages": [*state['messages'], ToolMessage(content=content,tool_call_id=get_uuid(),name="file_upload")]}
        else:
            return None
