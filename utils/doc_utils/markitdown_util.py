from markitdown import MarkItDown

md = MarkItDown()
#/agent_files/4cefbc33-1bd8-4b81-aa75-50b27d3ca1f8/user_uploads/agent.md

def get_file_content(file_path):
    """
    支持ppt,doc,xls,pdf
    :param file_path:
    :return: str
    """
    result = md.convert(file_path)
    return result.text_content

if __name__ == '__main__':
    print(get_file_content(r"D:\agent_files\6e1af0c1-aa6f-4101-af99-b01d8158f602\user_uploads\agent.pdf"))