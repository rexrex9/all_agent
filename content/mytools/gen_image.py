from conn import gen_img
from base import config as cfg
from utils.doc_utils import base64_utils as bu
from content.utils import runtime_util as ru
import os
import uuid
from utils.doc_utils import download_utils as du


def generate_image(prompt,image_size,reference_image_path=None):
    """
    生图工具，也可基于图生成图，如果是图生图，请传参考图的路径以reference_image_path这个参数
    :param prompt: 生图的提示词
    :param image_size: 生成图片的大小，枚举值：
                    "1328x1328" （1：1）
                    "1664x928" （16：9）
                    "928x1664" （9：16）
                    "1472x1140" （4：3）
                    "1140x1472" （3：4）
                    "1584x1056" （3：2）
                    "1056x1584" （2：3）
    :param reference_image_path: 参考图的路径
    :return: generated_image_path
    """
    # 根据是否存在reference_image来判断调用生图模型还是修图模型
    if reference_image_path:
        model = cfg.EDIT_IMAGE_MODEL
        # 把参考图变成base64 uri
        reference_image = bu.image_to_data_url(reference_image_path)
    else:
        model = cfg.IMAGE_MODEL
        reference_image = None

    # 调用生图方法
    image_url = gen_img.gen_img(model, prompt, image_size, reference_image=reference_image)
    # 把生图结果保存为图片
    # 1. 图片的路径的问题
    # 1.1 拼接保存图片文件夹的路径
    image_dir_path = os.path.join(ru.get_thread_dir(),cfg.GENERATE_IMAGE_PATH)
    # 创建文件夹
    os.makedirs(image_dir_path, exist_ok=True)
    # 1.2 拼接图片路径
    image_path = os.path.join(image_dir_path, f"{uuid.uuid4().hex}.png")
    # 2. 下载图片
    du.download_image(image_url, image_path)

    return image_path