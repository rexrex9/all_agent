from deepagents.backends import FilesystemBackend
from configs.global_configs import ROOT_PATH_SYSTEM,ROOT_PATH_AGENT
from agents_manager.utils import runtime_util as rt
import os
def create_session_backend(runtime):
    thread_id = rt.get_thread_id(runtime)
    # 根据 thread_id 动态创建目录
    #root_dir = os.path.join(ROOT_PATH_SYSTEM, thread_id)
    #asyncio.to_thread(os.makedirs, root_dir, exist_ok=True)
    root_dir_agent = os.path.join(ROOT_PATH_AGENT, thread_id)
    return FilesystemBackend(
        root_dir=root_dir_agent,
        virtual_mode=True
    )
