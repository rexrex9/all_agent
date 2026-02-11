import uuid
import sys

# 生成uuid
def get_uuid():
    return uuid.uuid4().hex

def get_platform():
    platform = sys.platform
    if platform.startswith("win"):
        #print("这是 Windows 系统")
        return 0
    elif platform.startswith("linux"):
        #print("这是 Linux 系统")
        return 1
    elif platform == "darwin":
        #print("这是 macOS 系统")
        return 2

if __name__ == '__main__':
    print(get_platform())