import os


def get_folder_file_update_time(folder_path):
    """
    获取文件夹下所有文件的最后修改时间

    参数:
    folder_path: 要遍历的文件夹路径

    返回:
    list: 包含所有文件最后修改时间戳的列表
          时间戳是从纪元（1970年1月1日00:00:00 UTC）开始的秒数
    """
    file_update_time_list = []  # 初始化空列表，用于存储所有文件的修改时间

    # 使用os.walk递归遍历文件夹及其所有子文件夹
    # root: 当前遍历的目录路径
    # dirs: 当前目录下的子目录列表
    # files: 当前目录下的文件列表
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前目录下的所有文件
        for file in files:
            # 构建文件的完整路径（目录路径 + 文件名）
            file_path = os.path.join(root, file)

            # 获取文件的最后修改时间（返回浮点数时间戳）
            # 时间戳表示从纪元（1970年1月1日00:00:00 UTC）开始的秒数
            file_update_time = os.path.getmtime(file_path)

            # 将获取到的时间戳添加到列表中
            file_update_time_list.append(file_update_time)

    # 返回包含所有文件修改时间的列表
    return file_update_time_list


def get_folder_file_update_time_max(folder_path):
    """
    获取文件夹下所有文件中最后修改时间的最大值（最新的修改时间）

    参数:
    folder_path: 要遍历的文件夹路径

    返回:
    float: 文件夹中最新的文件修改时间戳
           如果文件夹为空或没有文件，返回0
    """
    # 调用get_folder_file_update_time函数获取所有文件的修改时间
    file_update_time_list = get_folder_file_update_time(folder_path)

    # 检查列表是否为空（文件夹为空或没有文件）
    if len(file_update_time_list) == 0:
        # 如果列表为空，返回0作为默认值
        return 0

    # 使用max函数找出列表中的最大值（最新的修改时间）
    file_update_time_max = max(file_update_time_list)

    # 返回最新的修改时间戳
    return file_update_time_max


def get_directory_tree(root_dir='.'):
    """
    生成美观的树形目录结构

    示例输出:
    project/
    ├── src/
    │   ├── main.py
    │   └── utils.py
    ├── data/
    └── README.md
    """
    lines = []  # 存储最终输出的每一行

    def add_tree(path, prefix=''):
        """
        递归添加树结构

        参数:
        path: 当前要遍历的目录路径
        prefix: 当前层级的前缀字符串，用于生成缩进和连接线
        """
        try:
            # 获取所有条目并排序：目录在前，文件在后；同类内按字母顺序（不区分大小写）
            # 排序逻辑：key=lambda x: (not os.path.isdir(...), x.lower())
            # - not os.path.isdir(...): 目录→False(0)在前，文件→True(1)在后
            # - x.lower(): 同类内按字母顺序排列
            items = sorted(os.listdir(path),
                           key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))

        except PermissionError:
            # 如果没有权限访问该目录，添加提示信息并停止递归
            lines.append(f"{prefix}[权限不足]")
            return

        # 遍历当前目录下的所有条目
        for i, item in enumerate(items):
            full_path = os.path.join(path, item)  # 完整的文件/目录路径
            is_last = (i == len(items) - 1)  # 是否是当前目录的最后一个条目

            # 确定连接符号：最后一个条目使用└──，其他使用├──
            connector = '└── ' if is_last else '├── '

            if os.path.isdir(full_path):
                # 如果是目录，添加目录名（带/后缀）到输出
                lines.append(f"{prefix}{connector}{item}/")

                # 准备下一层递归的前缀：
                # - 如果是最后一个条目：使用空格缩进
                # - 否则：保留竖线连接符│
                extension = '    ' if is_last else '│   '

                # 递归调用：遍历子目录，传递增加的前缀
                add_tree(full_path, prefix + extension)
            else:
                # 如果是文件，直接添加文件名到输出
                lines.append(f"{prefix}{connector}{item}")

    # 从根目录开始递归遍历
    add_tree(root_dir)

    # 将所有行连接成完整的字符串输出
    return '\n'.join(lines)


if __name__ == "__main__":
    folder_path = r'../'
    a = get_directory_tree(folder_path)
    print(a)