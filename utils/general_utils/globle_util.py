import sys
# 判断当前的系统是windows，还是linux、mac

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