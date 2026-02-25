import requests
from base import configs as gc

url = "https://api.siliconflow.cn/v1/images/generations"

headers = {
    "Authorization": f"Bearer {gc.SILICON_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": 'Qwen/Qwen-Image',
    "prompt": '随便生成一个小动物',
    "image_size": "1328x1328",
}

response = requests.post(url, json=payload, headers=headers)

print(response.json()["images"][0]["url"])