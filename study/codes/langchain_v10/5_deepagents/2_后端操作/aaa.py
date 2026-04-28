


root_dir = '/agent_files'

file_path = '/agent_files/../a.txt'

with open(file_path, 'w') as f:
    f.write('Hello, World!')

    '/../a.txt'
def wrap_model_call(request, handler):
    request.file_path = root_dir + request.file_path  # 调工具前把文件路径转换成绝对路径(加上root_dir)
    result = handler(request)
    result.file_path = result.file_path.replace(root_dir, '') # 调工具后把文件路径转换成相对路径(去掉root_dir)