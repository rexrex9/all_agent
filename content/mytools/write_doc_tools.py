import pypandoc
from utils.general_utils import globle_util as gu
from content.utils import runtime_util as ru
def convert_file(filepath, output_format):
    """
    转换文件格式,支持txt,md,pdf,html,docx等
    :param: file_path: 输入文件路径
    :param: output_format: 输出格式 (如: 'html', 'pdf', 'docx', 'md')
    :return 输出文件路径
    """
    file_strs = filepath.split('.')
    # 1. 得到输入文件的格式
    input_format = file_strs[-1]
    # 2. 根据输出文件的格式，拼出输出文件的路径
    output_file_path = file_strs[0] +'.' + output_format
    # 3. 再判断是否是pdf转换
    if output_format.lower() == 'pdf':

        # 如果输入格式是txt，将其视为md（Markdown）格式处理
        # 因为Pandoc对txt支持有限，而txt和md语法相似
        if input_format == 'txt':
            input_format = 'md'  # 把txt当作md

        # 根据操作系统平台选择不同的字体配置
        # get_platform()返回0表示Windows，非0表示其他系统（如Linux/Mac）
        if gu.get_platform() == 0:
            # Windows平台配置
            # pdf_engine = '--pdf-engine=wkhtmltopdf'  # 注释掉的备选引擎
            mainfont = 'mainfont=SimSun'  # 设置主字体为宋体（Windows）
            cjkmainfont = 'CJKmainfont=SimSun'  # 设置CJK（中日韩）字体为宋体
        else:
            # 非Windows平台配置（Linux/Mac）
            # pdf_engine = '--pdf-engine=weasyprint'  # 注释掉的备选引擎
            mainfont = 'mainfont=Noto Sans CJK SC'  # 设置主字体为思源黑体（Linux/Mac）
            cjkmainfont = 'CJKmainfont=Noto Sans CJK SC'  # 设置CJK字体为思源黑体

        pypandoc.convert_file(source_file=filepath,  # 源文件
                                  to=output_format,  # 目标格式
                                  outputfile=output_file_path,  # 输出文件的路径
                                  format=input_format,
                                  extra_args=[  # 额外参数列表，传递给Pandoc
                                      '--pdf-engine=xelatex',  # 指定使用xelatex引擎生成PDF（支持Unicode和字体嵌入）
                                      '-V', mainfont,  # 设置LaTeX变量：主字体
                                      '--variable', cjkmainfont,  # 设置LaTeX变量：CJK字体,
                                      '--resource-path', ru.get_thread_dir(),  # 设置资源查找路径（如图片、样式表等）
                                    ],
                                  )
    else:
        pypandoc.convert_file(source_file=filepath,to=output_format,outputfile=output_file_path,format=input_format)

    return output_file_path




if __name__ == '__main__':
    filepath = r'D:\agent_files\24f96bf4-4267-463d-b07e-f7a2c97bec62\张三打怪兽_绘本.md'
    convert_file(filepath,'pdf')





