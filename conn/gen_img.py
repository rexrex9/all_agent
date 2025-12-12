import requests
from base import configs as gc
from utils.general_utils import base64_utils as bu
from utils.general_utils.loggers import logger

def gen_image(prompt,model=gc.IMAGE_MODEL,image_size="1328x1328", reference_image_path=''):
    url = "https://api.siliconflow.cn/v1/images/generations"

    headers = {
        "Authorization": f"Bearer {gc.SILICON_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": image_size,
    }
    if reference_image_path:
        payload["image"] = bu.image_to_data_url(reference_image_path)
    response = requests.post(url, json=payload, headers=headers)
    logger.info(response.json())
    return response.json()["images"][0]["url"]

