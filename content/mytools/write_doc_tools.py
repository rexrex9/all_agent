#from utils.general_utils.loggers import logger
from langchain.tools import tool
import pypandoc
from content.utils import runtime_util as rt
# tool
def convert_file(filepath, output_format):
    """
    转换文件格式,支持txt,md,pdf,html,docx等
    :param:
        file_path: 输入文件路径
        output_format: 输出格式 (如: 'html', 'pdf', 'docx', 'md')
    :return 输出文件路径
    """
    output_file = filepath.replace(filepath.split('.')[-1], output_format)
    input_format = filepath.split('.')[-1]
    #logger.info(f"开始转换文件:{filepath}")
    #logger.info(f"输出文件:{output_file}")
    if output_format.lower() == 'pdf':
        if input_format=='txt':
            input_format='md' # 把txt当作md
        pypandoc.convert_file(
            filepath,
            output_format,
            outputfile=output_file,
            format=input_format,
            extra_args=[
                '--pdf-engine=xelatex',
                '-V', 'mainfont=SimSun',  # 添加中文字体
                '--variable', 'CJKmainfont=SimSun',  # 添加 CJK 字体
                '--resource-path', rt.get_root_thread_dir(),  # 设置资源路径
            ]
        )
    else:
        pypandoc.convert_file(
            filepath,
            output_format,
            outputfile=output_file,
            format=input_format,
        )



    return output_file

if __name__ == '__main__':
    convert_file(r'D:\workspace\pythonworkspace\projects\all_agent\content\mytools\a.txt','pdf')