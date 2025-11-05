
import json
import re

def parse(content):
    try:
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # 如果没有代码块标记，尝试直接解析
            json_str = content
        return json.loads(json_str)
    except Exception as e:
        print(content)
        return None

if __name__ == '__main__':
    content = '''
    ```json
    {
      "reason": "用户询问当前时间，使用current_time工具获取当前时间信息",
      "result": "2025-09-22 18:30:26.392027"
    }
    ```
    '''
    print(parse(content))