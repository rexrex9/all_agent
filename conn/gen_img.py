import requests
from base import configs as gc  # 导入项目配置文件，其中定义了API密钥、默认模型等常量
from content.utils import base64_util as bu  # 导入图片处理工具模块，用于将本地图片转换为Data URL格式


def gen_image(prompt, model=gc.IMAGE_MODEL, image_size="1328x1328", reference_image_path=''):
    """
    调用硅基流动(SiliconFlow) API 生成或编辑图像

    参数:
        prompt (str): 描述生成图像的文本提示词（必填）。例如："一只坐在咖啡馆里的橘猫"
        model (str): 指定使用的AI模型。默认从配置中读取(gc.IMAGE_MODEL)。
                    可以是 "Qwen/Qwen-Image"（纯生成）或 "Qwen/Qwen-Image-Edit-2509"（编辑图片）。
        image_size (str): 生成图像的尺寸，格式为"宽x高"。默认"1328x1328"是Qwen模型的推荐尺寸之一。
        reference_image_path (str): 参考图像的本地路径。当使用编辑模型时，此为需要被修改的原图路径。
                                    留空则表示从零开始生成新图。

    返回:
        str: 生成的图像的临时URL。注意：该URL有效期为1小时，请及时下载保存。

    示例:
        # 纯文本生成
        url = gen_image("一只坐在咖啡馆里的橘猫")

        # 基于原图编辑（换背景）
        url = gen_image("将背景换成雪山",
                        model="Qwen/Qwen-Image-Edit-2509",
                        reference_image_path="cat.jpg")
    """

    # SiliconFlow API 的固定端点
    url = "https://api.siliconflow.cn/v1/images/generations"

    # 构建请求头：包含认证信息和内容类型
    headers = {
        "Authorization": f"Bearer {gc.SILICON_API_KEY}",  # 使用配置中的API密钥进行认证
        "Content-Type": "application/json"  # 指定请求体为JSON格式
    }

    # 构建基础请求体（JSON格式）
    payload = {
        "model": model,  # 指定AI模型
        "prompt": prompt,  # 文本描述，驱动图像生成的核心
        "image_size": image_size,  # 输出图像尺寸
    }

    # 判断是否为图像编辑任务：如果提供了参考图像路径，则将其添加到请求体中
    if reference_image_path:
        # 通过工具函数将本地图片转换为Data URL格式（如：data:image/png;base64,XXX）
        # 这是API要求的格式之一，适用于Qwen/Qwen-Image-Edit-2509模型
        payload["image"] = bu.image_to_data_url(reference_image_path)

    # 发送POST请求到API
    response = requests.post(url, json=payload, headers=headers)

    # 解析API返回的JSON响应，提取第一张生成图片的临时访问URL
    return response.json()["images"][0]["url"]