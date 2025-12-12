#from utils.general_utils.loggers import logger
from langchain.tools import tool
import pypandoc
from content.utils import runtime_util as rt
@ tool
def convert_file(filepath, output_format):
    """
    转换文件格式,支持pdf,html,docx
    :param:
        file_path: 输入文件路径
        output_format: 输出格式 (如: 'html', 'pdf', 'docx', 'md')
    :return 输出文件路径
    """
    output_file = filepath.replace(filepath.split('.')[-1], output_format)
    #logger.info(f"开始转换文件:{filepath}")
    #logger.info(f"输出文件:{output_file}")
    pypandoc.convert_file(
        filepath,
        output_format,
        outputfile=output_file,
        extra_args=[
            '--pdf-engine=xelatex',
            '-V', 'mainfont=SimSun',  # 设置中文字体
            '--variable', 'CJKmainfont=SimSun',  # 设置 CJK 字体
            '--resource-path', rt.get_root_thread_dir(),  # 设置资源路径
        ]
    )
    return output_file

if __name__ == '__main__':
    convert_file(r'D:\agent_files\6b55f2fa-9b75-4cfb-8449-086f75f1ae28\xiaomei_kite_story.md','pdf')