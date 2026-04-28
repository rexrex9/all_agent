import requests
from dotenv import load_dotenv
load_dotenv()
import os


url = "https://api.siliconflow.cn/v1/images/generations"
payload = {
    "model": "Qwen/Qwen-Image",
    "prompt": "二次元猫咪",
    "image_size": "512x512",
    "batch_size": 1,
} # 请求体，用以发送数据，传递参数

headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
} # 请求头，用以指定鉴权

response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)