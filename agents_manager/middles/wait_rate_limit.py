from langchain.agents.middleware import before_model
from utils.general_utils.loggers import logger
from configs import global_configs as gc
import asyncio

last_tokens = 0
# 节点式 (Node-style)：模型调用前的日志记录
@before_model()
async def wait_rate_limit(state, runtime):
    global last_tokens
    # 统计messages内全部的tokens
    total_tokens = 0
    for message in state['messages']:
        # 判断message是否有属性usage_metadata
        if hasattr(message, 'usage_metadata') and message.usage_metadata:
            total_tokens += message.usage_metadata.get('total_tokens', 0)
    logger.info(f"{total_tokens} tokens used")
    if total_tokens-last_tokens > gc.RATE_LIMIT:
        logger.info(f"new {total_tokens - last_tokens} tokens used")
        last_tokens = total_tokens
        logger.info(f"waiting for {gc.WAIT_RATE_LIMIT_SEC} seconds")
        await asyncio.sleep(gc.WAIT_RATE_LIMIT_SEC)
    return None