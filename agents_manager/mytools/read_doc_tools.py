from utils.doc_utils import markitdown_util

def get_file_content(file_path):
    """
    阅读文件的工具，支持ppt,doc,xls,pdf
    :param file_path: 文件地址
    :return: str 文件内容
    """
    result = markitdown_util.get_file_content(file_path)
    return result