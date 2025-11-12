from langchain.agents.middleware import before_model
from utils.general_utils.loggers import logger
from configs import global_configs as gc
import time

last_tokens = 0
# 节点式 (Node-style)：模型调用前的日志记录
@before_model()
def wait_rate_limit(state, runtime):
    global last_tokens
    # 统计messages内全部的tokens
    total_tokens = 0

    for message in state['messages']:
        logger.info(message)
        # 判断message是否有属性usage_metadata
        if hasattr(message, 'usage_metadata'):
            logger.info('usage_metadata///')
            logger.info(message.usage_metadata)
            total_tokens += message.usage_metadata.get('total_tokens', 0)
    logger.info(f"{total_tokens} tokens used")
    if total_tokens-last_tokens > gc.RATE_LIMIT:
        logger.info(f"new {total_tokens - last_tokens} tokens used")
        last_tokens = total_tokens
        logger.info(f"waiting for {gc.WAIT_RATE_LIMIT_SEC} seconds")
        time.sleep(gc.WAIT_RATE_LIMIT_SEC)
    return None