
import os
def read_file(file_path):
    """
    读文件内容的工具
    :param file_path: 文件路径
    :return:
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return content


def write_file(file_path, content):
    """
    写入内容到文件工具
    :param file_path: 文件路径
    :param content: 写入的内容
    :return:
    """
    with open(file_path, "w+", encoding="utf-8") as f:
        f.write(content)

def ls(dir_path):
    """
    展示文件夹目录的工具
    :param dir_path: 文件夹路径
    :return:
    """
    return os.listdir(dir_path)

if __name__ == '__main__':
    r = os.listdir('.')
    print(r)



