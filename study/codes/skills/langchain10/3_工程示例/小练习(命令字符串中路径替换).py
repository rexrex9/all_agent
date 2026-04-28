import re,os
s1 = 'python /aaa/a.py'
s2 = 'python /agent_files/aaa/a.py'
root_dir = '/agent_files'

# 1. 用正则识别到路径字符串
def find_path(text):
    pattern = r'(?:[a-zA-Z]:)?[\\/](?:[^\\/:*?"<>|\s，。；：！？、,;:!?()\[\]{}]+[\\/])*[^\\/:*?"<>|\s，。；：！？、,;:!?()\[\]{}]+(?=[\s，。；：！？、,;:!?()\[\]{}]|$)'
    paths = re.findall(pattern, text)
    return paths
# 2. 在正则路径字符串替换为加上root_dir的字符串
def change_command_path(command):
    command = os.path.normpath(command) # 规划化路径字符串
    paths = find_path(command) # 先找到路径字符串 /aaa/a.py
    for p in paths:
        rel_p = os.path.relpath(p,'/')
        changed_path = os.path.join(root_dir, rel_p) # 将路径字符串替换为加上root_dir的  /agent_files/aaa/a.py
        command = command.replace(p, changed_path) # 3. 最后把原来的命令字符串中的 路径字符串替换为 root_dir替换后的字符串
    return os.path.normpath(command)  # 规划化路径字符串

print(change_command_path(s1))



