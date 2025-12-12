from conn import gen_img
import requests
from langchain.tools import tool
from content.utils import runtime_util as rt
from base import configs as gc
import os
from utils.general_utils.globle_util import get_uuid

@ tool
def generate_image(prompt: str,
                   reference_image_path:str,
                   image_size:str):
#
    """
    生图工具
    :param prompt: 生图所需的提示词
    :param reference_image_path: 参考图片的路径，非必要，若传入则生图会参考该图
    :param image_size: 图片大小, 枚举值
        "1328x1328"
        "1664x928"
        "928x1664"
        "1472x1140"
        "1140x1472"
        "1584x1056"
        "1056x1584"
    :
    :return: 图片的url
    """
    if reference_image_path:
        img_url = gen_img.gen_image(prompt,model=gc.EDIT_IMAGE_MODEL,image_size=image_size,reference_image_path=reference_image_path)
    else:
        img_url= gen_img.gen_image(prompt,image_size=image_size)
    # 下载图片并保存
    img_data = requests.get(img_url).content
    dir = rt.change_file_path(gc.GENERATE_IMAGE_PATH)
    os.makedirs(dir, exist_ok=True)
    img_name = get_uuid()+".png"
    local_path = os.path.join(dir, img_name)
    with open(local_path, 'wb+') as handler:
        handler.write(img_data)
    return local_path

if __name__ == '__main__':
    generate_image("hello world",'D:/1.png')