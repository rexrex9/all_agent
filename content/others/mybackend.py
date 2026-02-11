from deepagents.backends import FilesystemBackend, BackendProtocol
from base.configs import ROOT_PATH_AGENT
from content.utils import runtime_util as rt
import os
from typing import Optional


class LazyFilesystemBackend(BackendProtocol):
    """
    延迟初始化的文件系统后端

    实现了 BackendProtocol 协议,提供懒加载机制:
    - 构造时不立即创建 FilesystemBackend 实例
    - 首次调用文件操作时才初始化真实后端
    - 避免初始化时因创建目录等os操作线程阻塞报错
    """

    def __init__(self, runtime):
        """
        初始化懒加载后端

        Args:
            runtime: 运行时上下文对象,用于获取线程ID等信息
        """
        self.runtime = runtime  # 保存运行时上下文
        self._backend: Optional[FilesystemBackend] = None  # 真实后端实例(初始为None)
        self._thread_id = rt.get_thread_id(runtime)  # 从运行时获取线程ID
        self._root_dir = os.path.join(ROOT_PATH_AGENT, self._thread_id)  # 构建根目录路径

    def _ensure_backend(self) -> FilesystemBackend:
        """
        确保后端已初始化(懒加载核心方法)

        采用单例模式,首次调用时:
        1. 创建根目录
        2. 初始化 FilesystemBackend 实例
        3. 记录日志

        Returns:
            FilesystemBackend: 已初始化的文件系统后端实例
        """
        if self._backend is None:
            os.makedirs(self._root_dir, exist_ok=True)  # 目录不存在则创建
            self._backend = FilesystemBackend(
                root_dir=self._root_dir,  # 设置根目录
                virtual_mode=True  # 启用虚拟模式
            )
        return self._backend

    def ls_info(self, path: str):
        """
        列出目录信息

        Args:
            path: 目标路径

        Returns:
            目录内容信息列表
        """
        return self._ensure_backend().ls_info(path)

    def read(self, file_path: str, offset: int = 0, limit: int = 2000):
        """
        读取文件内容

        Args:
            file_path: 文件路径
            offset: 读取起始位置(字节偏移)
            limit: 读取字节数限制

        Returns:
            文件内容字符串
        """
        return self._ensure_backend().read(file_path, offset, limit)

    def write(self, file_path: str, content: str):
        """
        写入文件内容

        Args:
            file_path: 文件路径
            content: 要写入的内容

        Returns:
            写入操作结果
        """
        return self._ensure_backend().write(file_path, content)

    def edit(self, file_path: str, old_string: str, new_string: str,
             replace_all: bool = False):
        """
        编辑文件(字符串替换)

        Args:
            file_path: 文件路径
            old_string: 要替换的旧字符串
            new_string: 替换后的新字符串
            replace_all: 是否替换所有匹配项(False则只替换第一个)

        Returns:
            编辑操作结果
        """
        return self._ensure_backend().edit(file_path, old_string, new_string, replace_all)

    def grep_raw(self, pattern: str, path: Optional[str] = None,
                 glob: Optional[str] = None):
        """
        在文件中搜索匹配模式(类似 grep 命令)

        Args:
            pattern: 搜索模式(正则表达式)
            path: 搜索路径(可选)
            glob: 文件匹配模式(可选,如 "*.py")

        Returns:
            匹配结果列表
        """
        return self._ensure_backend().grep_raw(pattern, path, glob)

    def glob_info(self, pattern: str, path: str = "/"):
        """
        根据模式匹配文件(类似 glob 命令)

        Args:
            pattern: 文件匹配模式(如 "**/*.txt")
            path: 起始搜索路径

        Returns:
            匹配的文件信息列表
        """
        return self._ensure_backend().glob_info(pattern, path)


def create_session_backend(runtime):
    """
    创建会话级别的文件系统后端

    为每个运行时会话创建独立的懒加载后端实例,实现:
    - 会话隔离(每个 thread_id 对应独立目录)
    - 资源节约(延迟初始化)

    Args:
        runtime: 运行时上下文

    Returns:
        LazyFilesystemBackend: 懒加载的文件系统后端实例
    """
    return LazyFilesystemBackend(runtime)