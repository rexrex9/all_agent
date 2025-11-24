from utils.doc_utils import markitdown_util
from utils.general_utils.loggers import logger
from utils.general_utils.globle_util import get_platform
from configs import global_configs as gc
def get_file_content(file_path):
    """
    阅读文件的工具，支持ppt,doc,xls,pdf
    :param file_path: 文件地址, 注意正确的文件路径应该是 ROOT_PATH_SYSTEM/agent_files/[thread_id]/[dir_path]/file_name这种形式
    :return: str 文件内容
    """
    if get_platform() == 0:
        file_path = file_path[1:]
    logger.info(f"开始读取文件:{file_path}")
    result = markitdown_util.get_file_content(file_path)
    return result

def fix_file_path(file_path):
    """
    修复文件路径
    :param file_path:
    :return:
    """

    if not file_path.startswith(gc.ROOT_PATH_SYSTEM):
        file_path.split('user_upload')
    return file_path



if __name__ == '__main__':
    f = '/D://agent_files/b37c33e3-1d00-4eae-989b-e05d1f123adf/user_uploads/agent历史与概念.pdf'
    print(get_file_content(f))