import requests
from base import configs as gc
from content.utils import base64_util as bu

url = "https://api.siliconflow.cn/v1/images/generations"

headers = {
    "Authorization": f"Bearer {gc.SILICON_API_KEY}",
    "Content-Type": "application/json"
}
reference_image_path = 'a.png'
payload = {
    "model": "Qwen/Qwen-Image-Edit-2509",
    "prompt": "把它变成一个战斗姿态",
    "image_size": "1328x1328",
    "image":bu.image_to_data_url(reference_image_path),
}

response = requests.post(url, json=payload, headers=headers)

print(response.json()["images"][0]["url"])

