from utils.doc_utils import markitdown_util
from utils.general_utils.loggers import logger
from langchain.tools import tool

@ tool
def get_file_content(filepath):
    """
    阅读文件的工具，支持ppt,doc,xls,pdf
    :param filepath: 文件地址
    :return: str 文件内容
    """
    result = markitdown_util.get_file_content(filepath)
    return result




if __name__ == '__main__':
    f = r"D:\agent_files\e527f8d9-e317-408e-ad46-e305c50ea623\examples\sample_sales_data.xlsx"
    print(get_file_content(f))