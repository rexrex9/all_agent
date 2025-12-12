from langchain_core.runnables.config import var_child_runnable_config
from utils.general_utils.loggers import logger
from base.configs import ROOT_PATH_SYSTEM,ROOT_SYSTEM
import os
def get_thread_id(runtime=None):
    """从 runtime config 中获取 thread_id"""
    config = getattr(runtime, 'config', None)
    if config is None:
        configurable = getattr(runtime, 'context', None)
    else:
        configurable = config.get('configurable', None)
    if configurable is None and var_child_runnable_config.get() is not None:
        configurable = var_child_runnable_config.get().get("configurable", {})
    if configurable is None:
        return 'default'
    thread_id = configurable.get('thread_id', 'default')
    return thread_id

def get_root_thread_dir():
    path = os.path.normpath(os.path.join(ROOT_PATH_SYSTEM, get_thread_id()))
    return path

def change_file_path(file_path):
    logger.info(f"file_path:{file_path}")
    file_path = os.path.normpath(file_path)
    root_thread_dir = get_root_thread_dir()
    if root_thread_dir in file_path:
        return file_path
    """将文件路径改为线程路径"""
    if os.path.isabs(file_path):
        if ROOT_SYSTEM in file_path:
            file_path = os.path.relpath(file_path, ROOT_SYSTEM)
        else:
            file_path = os.path.relpath(file_path, "/")
    p = os.path.join(root_thread_dir, file_path)
    logger.info(f"changed_file_path:{p}")
    return p

def get_out_path(file_path):
    dir= get_root_thread_dir() +'\\'
    file_path = os.path.normpath(file_path)
    file_path = file_path.replace(dir, '')
    return file_path

if __name__ == '__main__':
    root_dir = r'D:\code\langchain-demo\datas\filepaths\\'
    file_path = r'撒大s/苏打撒D:\code\langchain-demo\datas/filepaths.py'
    root_dir = os.path.normpath(root_dir)
    file_path = os.path.normpath(file_path)
    print(root_dir)
    print(file_path)
    a = os.path.relpath(file_path, root_dir)
    print(a)
    a = 'aaaa'
    b = 'asddsaaaa'
    print(a in  b)