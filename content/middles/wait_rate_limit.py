from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from base import configs as gc
import asyncio
from openai import RateLimitError
from utils.general_utils.loggers import logger

@wrap_model_call
async def wait_rate_limit(request: ModelRequest, handler) -> ModelResponse:
    #return await handler(request)
    for i in range(gc.WAIT_RATE_LIMIT_RETRY):
        try:
            return await handler(request)
        except RateLimitError as e:
            logger.info(f"Rate limit error, retrying ({i+1}/{gc.WAIT_RATE_LIMIT_RETRY})")
            if i == gc.WAIT_RATE_LIMIT_RETRY - 1:  # 最后一次重试
                raise
            await asyncio.sleep(gc.WAIT_RATE_LIMIT_SEC)


