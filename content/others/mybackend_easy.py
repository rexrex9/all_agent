import asyncio

from deepagents.backends import FilesystemBackend
import os
from base import config as cfg
from content.utils import runtime_util as ru

def backend_factory(runtime):
    root_dir = os.path.join(cfg.ROOT_PATH_AGENT, ru.get_thread_id())
    os.makedirs(root_dir, exist_ok=True) # 创建目录
    # -> /agent_files/fqzxvaqw132312saa
    return FilesystemBackend(root_dir=root_dir, virtual_mode=True)
