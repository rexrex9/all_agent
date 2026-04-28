# 导入日志库
import logging
# 导入路径操作库
import os
from base import config as cfg
LOG_FILE = os.path.join(cfg.LOG_DIR, 'app.log')


def setup_logging(log_file=LOG_FILE):
    # 创建日志目录
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    # 获取日志器
    logger = logging.getLogger("AllAgent")
    # 设置日志级别
    logger.setLevel(logging.INFO)
    # 避免重复添加处理器
    if not logger.handlers:
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        # 设置文件处理器级别
        file_handler.setLevel(logging.INFO)
        # 为文件处理器设置格式
        file_handler.setFormatter(formatter)
        # 添加文件处理器
        logger.addHandler(file_handler)
        if cfg.NEED_CONSOLE_LOG:
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            # 设置控制台处理器级别
            console_handler.setLevel(logging.INFO)
            # 为控制台处理器设置格式
            console_handler.setFormatter(formatter)
            # 添加控制台处理器
            logger.addHandler(console_handler)
    # 返回日志器
    return logger


# 初始化日志器
logger = setup_logging()


if __name__ == '__main__':
    logger.info("Hello, World!")