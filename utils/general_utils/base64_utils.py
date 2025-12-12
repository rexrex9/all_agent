import base64
import mimetypes

def image_to_data_url(file_path):
    """生成完整的data URL（包含MIME类型）"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'image/jpeg'  # 默认类型
    with open(file_path, 'rb') as image_file:
        base64_data = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"

def base64_to_image(base64_str, output_path):
    """
    将Base64字符串解码为图片文件
    Args:
        base64_str: Base64字符串（可包含或不包含data URL前缀）
        output_path: 输出图片文件路径
    """
    # 移除可能的data URL前缀
    if base64_str.startswith('data:'):
        base64_str = base64_str.split('base64,')[-1]
    # 解码Base64字符串
    image_data = base64.b64decode(base64_str)
    # 保存为图片文件
    with open(output_path, 'wb') as f:
        f.write(image_data)
    print(f"图片已保存到: {output_path}")


def str_to_base64(input_str):
    """
    将字符串转换为Base64字符串
    Args:
        input_str: 输入字符串
    Returns:
        Base64字符串
    """
    return base64.b64encode(input_str.encode('utf-8')).decode('utf-8')
def base64_to_str(base64_str):
    """
    将Base64字符串转换为字符串
    Args:
        base64_str: Base64字符串
    Returns:
        字符串
    """
    return base64.b64decode(base64_str).decode('utf-8')

if __name__ == '__main__':
    # 示例用法
    r = image_to_data_url(r'D:\workspace\pythonworkspace\chuanzhi\mouse_pad\datas\figures\figure_07.jpg')
    print(r)
    from conn.llms import get_vlm
    from langchain.messages import HumanMessage
    vlm = get_vlm()
    message = HumanMessage(
        content=[
            {"type": "text", "text": "分析下图"},
            {"type": "image_url", "image_url": {"url": r}}
        ]
    )

    r = vlm.invoke([message])
    print(r.content)