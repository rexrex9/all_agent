import requests
from dotenv import load_dotenv
load_dotenv()
import os
from utils.doc_utils import base64_utils as bu

url = "https://api.siliconflow.cn/v1/images/generations"

payload = {
    "model": "Qwen/Qwen-Image-Edit-2509",
    "prompt": "把这个老鼠变成粉红色的",
    "image": bu.image_to_data_url('a.png'),
}
headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)
import download_img
download_img.download_image(response.json()["images"][0]['url'],'s.png')



