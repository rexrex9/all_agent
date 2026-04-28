from utils.doc_utils import markitdown_utils
from langchain.tools import tool

@tool
def get_file_content(filepath): # filepath不与langchain本身的文件管理工具中的file_path同名
    """
    读取文档内容
    :param filepath: 文档路径
    :return: 文档内容
    """
    return markitdown_utils.get_file_content(filepath)