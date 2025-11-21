import shutil
import os
def compress_dir(folder_path):
    """
    使用shutil压缩文件夹
    Args:
        folder_path: 要压缩的文件夹路径
    """
    output_path = shutil.make_archive(
        base_name=folder_path,
        format='zip',
        root_dir=os.path.dirname(folder_path),
        base_dir=os.path.basename(folder_path)
    )
    return output_path

if __name__ == "__main__":
    # 使用示例
    compress_dir("D://agent_files/801984c4-662e-42de-a7e6-b5f734238241")