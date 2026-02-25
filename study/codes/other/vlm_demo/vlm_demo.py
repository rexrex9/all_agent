from content.utils import base64_util as bu
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from base import configs as gc

vlm = ChatOpenAI(model='Qwen/Qwen3-VL-30B-A3B-Instruct',
            base_url=gc.BASE_URL)

img_path = 'bot.png'

base64_url = bu.image_to_data_url(img_path)

messages = [HumanMessage(content=[{"type": "text", "text": "描述下图"},
                                     {"type": "image_url", "image_url": {"url": base64_url}}])]
result = vlm.invoke(messages)
print(result.content)