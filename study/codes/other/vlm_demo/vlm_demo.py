from utils.doc_utils import base64_utils as bu
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from base import config as cfg

vlm = ChatOpenAI(model='Qwen/Qwen3-VL-30B-A3B-Instruct',
            base_url='https://api.siliconflow.cn/v1')

img_path = 'bot.png'

base64_url = bu.image_to_data_url(img_path)


messages = [HumanMessage(content=[{"type": "text", "text": "描述下图"},
                                  {"type": "image_url", "image_url": {"url": base64_url}}])]
result = vlm.invoke(messages)
print(result.content)

