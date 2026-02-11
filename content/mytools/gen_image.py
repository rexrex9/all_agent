from conn import gen_img  # 导入自建的图片生成连接模块，其中应包含gen_image函数
import requests  # 用于下载网络图片
from langchain.tools import tool  # 用于将此函数包装为LangChain可调用的工具
from content.utils import runtime_util as rt  # 导入运行时工具，用于处理文件路径
from base import configs as gc  # 导入项目全局配置
import os  # 用于操作系统文件路径和目录
from utils.general_utils.globle_util import get_uuid  # 导入工具函数，用于生成唯一ID

@tool
def generate_image(prompt: str,
                   reference_image_path: str,
                   image_size: str):
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
    # 第一步：判断任务类型并调用生成API
    if reference_image_path:
        # 情况A：Agent提供了参考图路径 -> 调用编辑模型进行“图生图”
        # 使用编辑模型 (gc.EDIT_IMAGE_MODEL，如Qwen/Qwen-Image-Edit-2509)
        img_url = gen_img.gen_image(
            prompt=prompt,
            model=gc.EDIT_IMAGE_MODEL,  # 从配置中读取编辑模型名
            image_size=image_size,
            reference_image_path=reference_image_path  # 传入原图路径供模型参考
        )
    else:
        # 情况B：Agent未提供参考图 -> 调用基础模型进行“文生图”
        # 使用默认的基础生成模型 (如Qwen/Qwen-Image)
        img_url = gen_img.gen_image(
            prompt=prompt,
            image_size=image_size
            # 未指定model参数，使用gen_image函数内部的默认模型
        )

    # 第二步：下载生成的图片（API返回的URL有效期为1小时）
    img_data = requests.get(img_url).content  # 向图片URL发起GET请求，获取二进制图片数据

    # 第三步：准备本地保存路径
    # 使用工具函数处理生成图片的存储根目录，确保路径格式正确
    dir = rt.change_file_path(gc.GENERATE_IMAGE_PATH)
    # 创建目录（如果目录不存在），exist_ok=True表示目录已存在时不报错
    os.makedirs(dir, exist_ok=True)

    # 生成一个唯一的文件名（使用UUID），避免文件覆盖，并添加.png后缀
    img_name = get_uuid() + ".png"
    # 拼接完整的本地文件路径
    local_path = os.path.join(dir, img_name)

    # 第四步：将图片数据写入本地文件
    with open(local_path, 'wb+') as handler:  # 以二进制写入模式('wb+')打开文件
        handler.write(img_data)  # 将下载的图片二进制数据写入文件

    # 第五步：返回本地文件路径，供Agent使用
    return local_path
