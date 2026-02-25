from langchain.tools import tool

@ tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    with open(file_path, "w") as f:
        f.write(content)
    return f"已写入文件: {file_path}"

@ tool
def read_file(file_path: str) -> str:
    """Read content from a file"""
    with open(file_path, "r") as f:
        content = f.read()
    return f"已读取文件: {file_path}\n内容:\n{content}"

@ tool
def list_files(directory: str) -> str:
    """List all files in a directory"""
    import os
    files = os.listdir(directory)
    return f"已列出目录: {directory}\n文件列表:\n{files}"