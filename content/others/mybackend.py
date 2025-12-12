from deepagents.backends import FilesystemBackend, BackendProtocol
from base.configs import ROOT_PATH_AGENT
from content.utils import runtime_util as rt
import os
import threading
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from utils.general_utils.loggers import logger

# 全局线程池
_executor = ThreadPoolExecutor(max_workers=4)


class LazyFilesystemBackend(BackendProtocol):
    """
    延迟初始化的 FilesystemBackend
    第一次调用时在单独线程中创建，避免阻塞事件循环
    """
    def __init__(self, runtime):
        self.runtime = runtime
        self._backend: Optional[FilesystemBackend] = None
        self._lock = threading.Lock()
        self._thread_id = rt.get_thread_id(runtime)
        self._root_dir = os.path.join(ROOT_PATH_AGENT, self._thread_id)
        #logger.info(f"LazyBackend 创建: {self._thread_id}")

    def _ensure_backend(self) -> FilesystemBackend:
        logger.info(self.runtime)

        """
        确保 backend 已初始化
        使用双重检查锁定，首次调用时在线程池中创建
        """
        if self._backend is not None:
            return self._backend

        with self._lock:
            if self._backend is not None:
                return self._backend

            #logger.info(f"在线程中初始化 FilesystemBackend: {self._thread_id}")

            # 在线程池中创建 backend
            future = _executor.submit(self._create_backend_in_thread)
            self._backend = future.result()  # 等待完成

            #logger.info(f"✓ FilesystemBackend 初始化完成: {self._thread_id}")
            return self._backend

    def _create_backend_in_thread(self) -> FilesystemBackend:
        """在工作线程中创建 backend（允许阻塞调用）"""
        os.makedirs(self._root_dir, exist_ok=True)
        return FilesystemBackend(
            root_dir=self._root_dir,
            virtual_mode=True
        )

    # 委托所有方法（每个方法第一次调用时会初始化）

    def ls_info(self, path: str):
        return self._ensure_backend().ls_info(path)

    def read(self, file_path: str, offset: int = 0, limit: int = 2000):
        return self._ensure_backend().read(file_path, offset, limit)

    def write(self, file_path: str, content: str):
        return self._ensure_backend().write(file_path, content)

    def edit(self, file_path: str, old_string: str, new_string: str,
             replace_all: bool = False):
        return self._ensure_backend().edit(file_path, old_string, new_string, replace_all)

    def grep_raw(self, pattern: str, path: Optional[str] = None,
                 glob: Optional[str] = None):
        return self._ensure_backend().grep_raw(pattern, path, glob)

    def glob_info(self, pattern: str, path: str = "/"):
        return self._ensure_backend().glob_info(pattern, path)


def create_session_backend(runtime):
    """创建延迟初始化的 session backend"""
    return LazyFilesystemBackend(runtime)