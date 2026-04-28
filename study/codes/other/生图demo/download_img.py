image_url="https://bizyair-prod.oss-cn-shanghai.aliyuncs.com/outputs%2Ff3c28833-1c7f-41b4-a065-0091075d0203_a329afac985027bf083ebb3eb9572930_ComfyUI_242d8e33_00001_.png?OSSAccessKeyId=LTAI5tPza7RAEKed35dCML5U&Expires=1776761556&Signature=Tm4cVilYp1Pu8UerMqUOUZiOJ3k%3D"

import requests

def download_image(image_url, save_path):
    response = requests.get(image_url)
    image_data = response.content # 获取图片二进制数据

    with open(save_path, 'wb') as f:
        f.write(image_data)