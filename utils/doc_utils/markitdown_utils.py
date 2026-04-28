
from markitdown import MarkItDown

md = MarkItDown()

def get_file_content(file_path):
    """
    支持ppt,doc,xls,pdf
    :param file_path:
    :return: str
    """
    result = md.convert(file_path)
    return result.text_content


if __name__ == '__main__':
    file_path = r'D:\downloads\ss.docx'
    print(get_file_content(file_path))