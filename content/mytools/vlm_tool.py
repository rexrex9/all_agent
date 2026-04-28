
from conn.llm import get_vlm
from utils.doc_utils import base64_utils as bu
from langchain.messages import HumanMessage

vlm = get_vlm()
def read_image(image_path):
    """
    理解图片的工具
    :param image_path: 图片的路径
    :return:
    """
    base64_url = bu.image_to_data_url(image_path)

    messages = [HumanMessage(content=[{"type": "text", "text": "描述下图"},
                                      {"type": "image_url", "image_url": {"url": base64_url}}])]
    result = vlm.invoke(messages)
    return result.content

if __name__ == "__main__":
    image_path = 'bot.png'
    print(read_image(image_path))