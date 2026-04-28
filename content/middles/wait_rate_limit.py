import asyncio
from openai import RateLimitError
from langchain.agents.middleware import wrap_model_call
from base import config as cfg
from utils.general_utils.loggers import logger

@wrap_model_call
async def wait_rate_limit(request,handler):
    for i in range(cfg.WAIT_RATE_LIMIT_RETRY):
        try:
            result = await handler(request)
            return result # 仅需成功就立即返回
        except RateLimitError:
            logger.info(f'触发了速率限制,正在重试 {i+1}/{cfg.WAIT_RATE_LIMIT_RETRY}')
            # 如果触发速率限制则停顿90秒，再继续循环
            await asyncio.sleep(cfg.WAIT_RATE_LIMIT_SEC)
    else:
        raise RateLimitError


