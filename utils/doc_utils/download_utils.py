
import requests

def download_image(image_url, save_path):
    # 下载图片
    response = requests.get(image_url)
    image_data = response.content # 获取图片二进制数据

    with open(save_path, 'wb') as f:
        f.write(image_data)