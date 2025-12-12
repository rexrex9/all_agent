
import os
import shutil


def delete_folder_contents(folder_path):
    """
    删除文件夹中的所有内容
    """
    if not os.path.exists(folder_path):
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)

# 获取文件夹下所有文件的更新时间
def get_folder_file_update_time(folder_path):
    """
    :param folder_path:
    :return:
    """
    file_update_time_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_update_time = os.path.getmtime(file_path)
            file_update_time_list.append(file_update_time)
    return file_update_time_list

# 获取文件更新时间最大值
def get_folder_file_update_time_max(folder_path):
    """
    :param folder_path:
    :return:
    """
    file_update_time_list = get_folder_file_update_time(folder_path)
    if len(file_update_time_list) == 0:
        return 0
    file_update_time_max = max(file_update_time_list)
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
    lines = []
    def add_tree(path, prefix=''):
        """递归添加树结构"""
        # 获取所有条目并排序
        try:
            items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        except PermissionError:
            lines.append(f"{prefix}[权限不足]")
            return

        for i, item in enumerate(items):
            full_path = os.path.join(path, item)
            is_last = (i == len(items) - 1)

            # 确定连接符号
            connector = '└── ' if is_last else '├── '

            if os.path.isdir(full_path):
                # 目录
                lines.append(f"{prefix}{connector}{item}/")
                # 递归处理子目录
                extension = '    ' if is_last else '│   '
                add_tree(full_path, prefix + extension)
            else:
                # 文件
                lines.append(f"{prefix}{connector}{item}")

    # 添加根目录
    #root_name = os.path.basename(os.path.abspath(root_dir))
    #lines.append(f"{root_name}/")
    add_tree(root_dir)

    return '\n'.join(lines)


if __name__ == "__main__":
    folder_path = r'D:\agent_files\46ae1177-34a0-45cf-bc4c-c2d1c56974e1'
    # #get_folder_file_update_time(folder_path)
    # file_path = r'D:\workspace\pythonworkspace\projects\all_agent\utils\general_utils\os_util.py'
    # a = get_folder_file_update_time_max(folder_path)
    # print(a)
    # print(type(a))
    a = get_directory_tree(folder_path)
    print(a)