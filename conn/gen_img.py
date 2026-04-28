
import requests
import os
def gen_img(model, prompt,image_size,reference_image=None):
    """
    :param model: 模型
    :param prompt: 提示词
    :param image_size: 图片大小
    :param reference_image: 参考图的base64 uri
    :return:
    """
    url = "https://api.siliconflow.cn/v1/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": image_size,
        "batch_size": 1
    } # 请求体，用以发送数据，传递参数
    if reference_image:
        payload["image"] = reference_image

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    } # 请求头，用以指定鉴权

    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()["images"][0]["url"]