import requests
from env.serect import SILICON_API_KEY

def gen_image(prompt):
    url = "https://api.siliconflow.cn/v1/images/generations"
    payload = {
        "model": "Qwen/Qwen-Image",
        "prompt": prompt,
        "image_size": "256x256",
    }
    headers = {
        "Authorization": f"Bearer {SILICON_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)

    return response.json()["images"][0]["url"]

if __name__ == '__main__':
    res = gen_image("hello world")
    print(res)