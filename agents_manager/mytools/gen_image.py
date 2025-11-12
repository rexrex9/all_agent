from conn import gen_img
import requests

def generate_image(prompt,local_path):
    """
    生图工具
    :param prompt: 生图所需的提示词
    :local_path: 本地保存路径
    :return: 图片的url
    """
    img_url= gen_img.gen_image(prompt)
    # 下载图片并保存
    img_data = requests.get(img_url).content
    with open(local_path, 'wb') as handler:
        handler.write(img_data)

if __name__ == '__main__':
    generate_image("hello world",'D:/1.png')