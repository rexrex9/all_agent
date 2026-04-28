import shutil # 这是shutil模块，处理一些高级的文件操作，理解为一个更高级封装的os模块

# 打包文件夹成zip的方法：
def zip_folder(folder_path, zip_path=None):
    """
    打包文件夹成zip文件
    :param folder_path: 要打包的文件夹路径
    :param zip_path: 压缩文件保存路径
    """
    if not zip_path:
        zip_path = folder_path
    return shutil.make_archive(zip_path, 'zip', folder_path)

if __name__ == '__main__':
    folder_path = r'D:\agent_files\9f4ad8ab-0642-4bbd-8f76-2fae9c8bd658' # 要打包的文件夹路径
    print(zip_folder(folder_path))
