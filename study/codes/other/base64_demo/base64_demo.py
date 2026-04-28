import base64


def file_to_base64(file_path):
    """将文件转换为Base64字符串"""
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        base64_str = base64.b64encode(binary_data).decode('utf-8')
        return base64_str


def base64_to_file(base64_str, output_path):
    """将Base64字符串转换回文件"""
    binary_data = base64.b64decode(base64_str)

    with open(output_path, 'wb') as file:
        file.write(binary_data)

    print(f"文件已保存到: {output_path}")


if __name__ == '__main__':
    file_path = 'bot.png'
    base64_str = file_to_base64(file_path)
    print(base64_str)
    #output_path = 'bot2.png'
    #base64_to_file(base64_str, output_path)