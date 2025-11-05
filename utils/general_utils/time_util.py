
import time
from functools import wraps
from utils.general_utils.loggers import logger
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.info(f"方法：{func.__name__};耗时： {time.time() - start:.3f}s")
        return result
    return wrapper


if __name__ == '__main__':
    @timer
    def test_func():
        time.sleep(1)
        return "Hello, World!"
    print(test_func())