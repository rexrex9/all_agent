from langchain_core.runnables.config import var_child_runnable_config
from base import configs as gc
import os
def get_thread_id(runtime=None):
    # 从 runtime config 中获取 thread_id
    config = getattr(runtime, 'config', None)
    if config is None:
        configurable = getattr(runtime, 'context', None)
    else:
        configurable = config.get('configurable', None)

    # 从 var_child_runnable_config
    if configurable is None and var_child_runnable_config.get() is not None:
        configurable = var_child_runnable_config.get().get("configurable", {})
    if configurable is None:
        return 'default'
    thread_id = configurable.get('thread_id', 'default')
    return thread_id


def change_file_path(file_path):
    """
    转换文件路径为当前线程对应的文件路径

    主要功能：
    1. 如果路径已经包含线程根目录，直接返回
    2. 将绝对路径转换为相对于线程根目录的路径
    3. 处理系统根目录的特殊情况

    Args:
        file_path (str): 原始文件路径

    Returns:
        str: 转换后的文件路径
    """

    # 规范化文件路径，处理多余的分隔符、'.'和'..'等
    # 例如：/home//user/./docs/../file.txt -> /home/user/file.txt
    file_path = os.path.normpath(file_path)

    # 获取当前线程的根目录路径
    root_thread_dir = get_root_thread_dir()

    # 检查原始路径是否已经包含线程根目录
    # 如果已经包含，说明路径已经是正确格式，直接返回
    if root_thread_dir in file_path:
        return file_path

    # 检查是否为绝对路径（以根目录开始的路径）
    if os.path.isabs(file_path):
        # 如果路径中包含系统根目录标识（gc.ROOT_SYSTEM）
        if gc.ROOT_SYSTEM in file_path:
            # 则计算相对于系统根目录的相对路径
            file_path = os.path.relpath(file_path, gc.ROOT_SYSTEM)
        else:
            # 如果不包含系统根目录标识，则计算相对于系统根目录"/"的相对路径
            file_path = os.path.relpath(file_path, "/")

    # 将相对路径与线程根目录拼接，得到完整的线程相关路径
    p = os.path.join(root_thread_dir, file_path)

    # 返回转换后的完整路径
    return p

def get_root_thread_dir():
    """
    获取当前线程的专属根目录路径

    功能描述：
    1. 将系统根路径与当前线程ID组合，生成线程专用的目录路径
    2. 对路径进行规范化处理，确保路径格式统一

    返回:
    str: 当前线程的专属目录路径（标准化格式）

    示例:
    如果 ROOT_PATH_SYSTEM = "C:\\temp"
    get_thread_id() 返回 "thread_123"
    则返回 "C:\\temp\\thread_123"
    """
    # 将系统根目录路径与当前线程ID拼接，生成完整路径
    # os.path.join: 智能拼接路径，自动处理不同操作系统的路径分隔符
    # get_thread_id(): 原有方法，获取当前线程的唯一标识符
    raw_path = os.path.join(gc.ROOT_PATH_SYSTEM, get_thread_id())

    # 规范化路径，处理路径中的冗余部分（如 '..', '.', 多余的斜杠等）
    # 例如: "C:\\temp\\thread_123\\..\\thread_123" → "C:\\temp\\thread_123"
    normalized_path = os.path.normpath(raw_path)

    return normalized_path


def get_out_path(file_path):
    """
    从完整的文件路径中提取相对于线程目录的相对路径

    功能描述：
    1. 获取线程根目录路径并添加路径分隔符
    2. 从完整文件路径中移除线程根目录部分，得到相对路径
    3. 用于将绝对路径转换为相对于线程目录的相对路径

    参数:
    file_path (str): 文件路径

    返回:
    str: 相对于线程根目录的文件路径（移除了线程目录前缀）, 如果线程根目录不存在，则返回原始路径

    示例:
    假设线程目录为 "C:\\temp\\thread_123"
    输入: "C:\\temp\\thread_123\\data\\file.txt"
    返回: "data\\file.txt"
    输入: "dir\\data\\file.txt"
    返回: "dir\\data\\file.txt"
    """

    # 如果输入不是字符串，则返回原始路径
    if type(file_path) != str:
        return file_path

    # 获取线程根目录并添加路径分隔符
    # 注意：这里使用 '\\' 作为分隔符，在跨平台场景中建议使用 os.path.sep
    thread_dir = get_root_thread_dir() + '\\'

    # 规范化输入的文件路径，确保格式一致
    # 这有助于后续的字符串替换操作更可靠
    file_path = os.path.normpath(file_path)

    # 从完整路径中移除线程根目录前缀，得到相对路径
    # 例如: "C:\\temp\\thread_123\\data\\file.txt" → "data\\file.txt"
    # 如果线程根目录不存在，则返回原始路径
    # 例如: "data\\file.txt" → "data\\file.txt"
    relative_path = file_path.replace(thread_dir, '')

    return relative_path



if __name__ == '__main__':
    root_dir = r'D:\code\langchain-demo\datas\filepaths\\'
    file_path = r'\code\langchain-demo\datas/filepaths.py'
    print(get_out_path(file_path))
    root_dir = os.path.normpath(root_dir)
    file_path = os.path.normpath(file_path)
    print(root_dir)
    print(file_path)
    a = os.path.relpath(file_path, '/')
    print(a)
    a = 'aaaa'
    b = 'asddsaaaa'
    print(a in  b)