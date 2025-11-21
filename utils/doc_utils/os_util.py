
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



if __name__ == "__main__":
    folder_path = r'D:\workspace\pythonworkspace\projects\all_agent'
    #get_folder_file_update_time(folder_path)
    file_path = r'D:\workspace\pythonworkspace\projects\all_agent\utils\general_utils\os_util.py'
    a = get_folder_file_update_time_max(folder_path)
    print(a)
    print(type(a))