# 辅助理解代码
from conn.llm import get_llm
import json
import datetime
import re

llm = get_llm()

# 系统提示词 - 描述可用函数和调用规则
SYSTEM_PROMPT = """
你是一个智能助手，可以调用以下函数工具：
1. 加法函数：
   - 名称：add
   - 功能：计算两个整数的和
   - 参数：
        a: 整数（第一个数字）
        b: 整数（第二个数字）
   - 调用格式：{"function": "add", "arguments": {"a": x, "b": y}}

2. 时间函数：
   - 名称：get_current_time
   - 功能：获取当前时间
   - 参数：无
   - 调用格式：{"function": "get_current_time", "arguments": {}}

调用规则：
1. 当用户问题需要数学计算时调用add
2. 当用户问题涉及当前时间时调用get_current_time
3. 其他情况直接回答问题
4. 调用函数时必须严格使用JSON格式
5. 不要解释函数调用过程，直接输出JSON或回答
"""



# 自定义函数
def add(a, b):
    return a + b


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 函数注册表
function_registry = {
    "add": add,
    "get_current_time": get_current_time
}


# 解析函数调用
def parse_function_call(response):
    try:
        # 尝试提取JSON字符串
        json_str = re.search(r'\{[\s\S]*\}', response).group()
        data = json.loads(json_str)
        return data["function"], data.get("arguments", {})
    except:
        pass
    return None, None


def do(question):
    # 构建消息
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    print(f"User>\t {question}")

    # 第一次调用模型
    response = llm.invoke(messages)
    print(f"最初回复>\t {response.content}")

    # 尝试解析函数调用
    func_name, func_args = parse_function_call(response.content)
    if func_name and func_name in function_registry:
        print(f"执行函数>{func_name} 参数 {func_args}")
        # 执行函数
        if func_args:
            result = function_registry[func_name](**func_args)
        else:
            result = function_registry[func_name]()

        print(f"函数返回>\t {result}")

        # 构建第二次查询
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": f"函数执行结果: {result}\n请基于此结果回答我的原始问题"})
        # 第二次调用模型
        final_response = llm.invoke(messages)
        return final_response.content
    else:
        return response.content


if __name__ == '__main__':
    # 测试不同场景
    questions = [
        "现在几点，并且告诉我123+222等于多少"
        # "123加456等于多少？",
        # "现在几点了？",
        # "你好，今天天气怎么样？"
    ]

    for q in questions:
        print("=" * 50)
        result = do(q)
        print(f"最终回复: {result}\n")