import os
from utils.general_utils.loggers import logger

def get_files_update_time(dir_path,all_update_times=None,ignore_dir_names=None):
    """
    :param dir_path: 传入一个文件夹地址
    :param all_update_times: 存储所有文件的更新时间
    :param ignore_dirs: 忽略的目录列表
    :return: 该文件夹地址下所有文件的更新时间
    """
    if all_update_times is None:
        all_update_times = []
    for file_name in os.listdir(dir_path): # 获取当前目录下的所有文件和目录名称
        file_path = os.path.join(dir_path, file_name) # 拼接文件路径
        if os.path.isdir(file_path): # 判断是否是目录
            if not (ignore_dir_names and file_name in ignore_dir_names):
                get_files_update_time(file_path,all_update_times,ignore_dir_names) # 递归调用
        else:
            logger.info(os.path.getmtime(file_path))
            all_update_times.append(os.path.getmtime(file_path)) # 添加文件更新时间
    return all_update_times

def get_max_update_time(dir_path,ignore_dir_names=None):
    """
    :param dir_path: 传入一个文件夹地址
    :param ignore_dirs: 忽略的目录列表
    :return:  该文件夹地址下最大的更新时间
    """
    all_update_times = get_files_update_time(dir_path,ignore_dir_names=ignore_dir_names)
    return max(all_update_times) if all_update_times else 0


def get_all_files_path_in_dir(path,all_paths=None):
    if all_paths is None:
        all_paths = set()
    # 获得传入目录下所有文件的路径组成一个集合
    items = os.listdir( path) # 获取当前目录下的所有文件和目录名称
    for item in items: # 遍历所有文件和目录名称
        item_path = os.path.join(path, item) # 拼接文件路径
        if os.path.isdir(item_path): # 判断是否是目录
            get_all_files_path_in_dir(item_path,all_paths) # 递归调用
        else:
            all_paths.add(item_path) # 添加文件路径到集合中
    return all_paths # 返回所有文件路径的集合


def list_directory(path, indent=''):
    """
    递归列出目录结构，返回树形结构的字符串

    参数:
        path: 要列出的目录路径
        indent: 缩进字符串，用于控制树形结构的层级显示
                (递归调用时自动传递，首次调用不需要提供)

    返回:
        返回一个字符串，包含整个目录树的文本表示
    """

    # 初始化一个空字符串，用于累积当前层级及子目录的所有输出内容
    tree_str = ''

    try:
        # os.listdir(path) 获取指定路径下的所有文件和目录名称（不包括完整路径）
        # 返回一个包含名称的列表，例如: ['file1.txt', 'dir1', 'file2.jpg']
        items = os.listdir(path)

        # 对项目列表进行排序，确保输出顺序一致
        # 默认按字母顺序排序，便于阅读
        items.sort()  # 排序显示

        # 使用 enumerate 遍历列表，同时获取索引 i 和项目名称 item
        # i 从 0 开始，用于判断是否是最后一个元素
        for i, item in enumerate(items):
            # 使用 os.path.join 将目录路径和项目名称连接成完整路径
            # 这样可以正确处理不同操作系统的路径分隔符（Windows用\，Linux/Mac用/）
            item_path = os.path.join(path, item)

            # 判断当前项目是否是列表中的最后一个
            # len(items) - 1 是最后一个元素的索引
            # 例如: 如果有5个项目，最后一个索引是4
            is_last = (i == len(items) - 1)

            # 选择前缀符号（树形结构的连接线）
            # 如果是最后一个项目，使用 '└── '（结尾符号）
            # 否则使用 '├── '（中间符号）
            # 这些符号模拟了树形结构的视觉效果
            # 例如:
            # ├── 项目1
            # ├── 项目2
            # └── 项目3 (最后一个)
            prefix = '└── ' if is_last else '├── '

            # 将当前项目添加到结果字符串中
            # f-string 格式化字符串: {indent}缩进 + {prefix}连接符 + {item}项目名
            # \n 是换行符，确保每个项目单独占一行
            tree_str += f'\n{indent}{prefix}{item}'

            # 检查当前项目是否为目录
            # os.path.isdir() 判断路径是否是一个目录
            if os.path.isdir(item_path):
                # 如果是目录，需要递归进入该目录，继续列出其内容

                # 计算下一级的缩进字符串
                # 根据当前项目是否是最后一个，决定使用什么缩进符号
                # 如果是最后一个: 使用空格缩进（不再有竖线）
                # 如果不是最后一个: 使用竖线和空格（表示还有后续兄弟项目）
                #
                # 例如当前层级:
                # ├── dir1/       (不是最后一个，下一级缩进用 '│   ')
                # │   └── file    (竖线表示上面还有兄弟目录)
                # └── dir2/       (是最后一个，下一级缩进用 '    ')
                #     └── file    (空格缩进，表示上面没有兄弟了)
                new_indent = indent + ('    ' if is_last else '│   ')

                # 递归调用当前函数，传入子目录路径和新的缩进
                # 将递归返回的子目录树形结构字符串追加到当前结果中
                # 注意: 递归调用返回的字符串已经包含了换行和正确的缩进
                tree_str += list_directory(item_path, new_indent)

        # 返回当前层级及所有子目录累积的树形结构字符串
        return tree_str

    except PermissionError:
        # 当没有权限访问某个目录时会发生 PermissionError
        # 例如: 系统受保护的目录、其他用户的私有目录等

        # 返回权限不足的提示信息
        # 使用 f-string 格式化，包含当前的缩进
        # 这样错误提示会显示在正确的位置，保持树形结构的对齐
        return f'{indent}[权限不足]'






if __name__ == "__main__":
    pass