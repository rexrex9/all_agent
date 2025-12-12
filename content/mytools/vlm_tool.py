from utils.general_utils.loggers import logger
from langchain.tools import tool
from conn.llms import get_vlm
from utils.general_utils import base64_utils as bu
from langchain.messages import HumanMessage

vlm = get_vlm()
@ tool
async def get_img_content(filepath):
    """
    阅读图片的工具
    :param filepath: 文件地址
    :return: str 图片内容
    """
    base64_url = bu.image_to_data_url(filepath)
    messages = [HumanMessage(content=[{"type": "text", "text": "描述下图"},
                                     {"type": "image_url", "image_url": {"url": base64_url}}])]
    result = await vlm.ainvoke(messages)
    return result