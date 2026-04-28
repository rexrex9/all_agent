# 辅助理解
from conn.llm import get_llm
import json
import re
import math
import datetime

llm = get_llm()

# 系统提示词 - 描述ReAct模式和使用规则
SYSTEM_PROMPT = """
你是一个智能助手，使用ReAct（Reasoning and Acting）模式解决问题。请按照以下步骤思考：

1. 思考(Thought)：分析问题，决定下一步行动
2. 行动(Action)：调用工具或回答问题
3. 观察(Observation)：获取工具执行结果

规则：
- 当需要外部信息时调用工具
- 工具调用格式：{"action": "工具名", "action_input": {参数}}
- 最终答案格式：{"action": "final_answer", "action_input": "答案"}

可用工具：
1. 搜索(search): 获取最新信息
   - 参数: query (搜索关键词)
2. 计算器(calculator): 执行数学计算
   - 参数: expression (数学表达式，如"sqrt(16)+3*2")
3. 当前时间(current_time): 获取当前时间
   - 参数: 无
4. 单位转换(unit_converter): 转换单位
   - 参数: value (数值), from_unit (原单位), to_unit (目标单位)
   - 支持单位: km/m/cm, kg/g, °C/°F/K

示例：
问题：姚明的身高是多少英尺？
{
  "thought": "姚明是中国人，身高通常用米表示，需要转换为英尺",
  "action": "search",
  "action_input": {"query": "姚明身高"}
}

问题：10公里是多少米？
{
  "thought": "单位转换问题",
  "action": "unit_converter",
  "action_input": {"value": 10, "from_unit": "km", "to_unit": "m"}
}

问题：3的平方根加上5乘以2等于多少？
{
  "thought": "需要计算数学表达式",
  "action": "calculator",
  "action_input": {"expression": "sqrt(3)+5*2"}
}

现在开始，请严格按照格式输出JSON。
"""


# 工具函数
def search(query):
    # 模拟搜索API
    knowledge_base = {
        "姚明身高": "2.29米",
        "珠穆朗玛峰高度": "8848.86米",
        "地球到月球距离": "384400公里",
        "水的沸点": "100°C",
        "北京人口": "2189万"
    }
    return knowledge_base.get(query, f"未找到关于'{query}'的信息")


def calculator(expression):
    try:
        # 安全计算 - 只允许数学函数
        allowed_names = {
            k: v for k, v in math.__dict__.items()
            if not k.startswith("_")
        }
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"


def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def unit_converter(value, from_unit, to_unit):
    # 单位转换表
    conversions = {
        # 长度
        ("km", "m"): lambda x: x * 1000,
        ("m", "cm"): lambda x: x * 100,
        ("cm", "m"): lambda x: x / 100,
        ("m", "km"): lambda x: x / 1000,
        # 重量
        ("kg", "g"): lambda x: x * 1000,
        ("g", "kg"): lambda x: x / 1000,
        # 温度
        ("°C", "°F"): lambda x: (x * 9 / 5) + 32,
        ("°F", "°C"): lambda x: (x - 32) * 5 / 9,
        ("°C", "K"): lambda x: x + 273.15,
        ("K", "°C"): lambda x: x - 273.15
    }

    try:
        if (from_unit, to_unit) in conversions:
            result = conversions[(from_unit, to_unit)](float(value))
            return f"{result} {to_unit}"
        else:
            return f"不支持从 {from_unit} 到 {to_unit} 的转换"
    except Exception as e:
        return f"转换错误: {str(e)}"


# 工具注册表
TOOL_REGISTRY = {
    "search": search,
    "calculator": calculator,
    "current_time": current_time,
    "unit_converter": unit_converter
}


def parse_react_response(response):
    """解析ReAct格式的响应"""
    try:
        # 尝试提取JSON
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            data = json.loads(json_match.group())
            return data
    except (json.JSONDecodeError, TypeError):
        pass
    return None


def react_agent(question, max_steps=10):
    """ReAct代理主循环"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    print(f"问题: {question}")
    print("-" * 50)

    for step in range(max_steps):
        # 调用模型获取响应
        response = llm.invoke(messages)
        print(f"步骤 {step + 1} 响应:\n{response.content}\n")

        # 解析响应
        action_data = parse_react_response(response.content)

        if not action_data:
            print("无法解析响应，尝试直接输出")
            return response.content

        # 添加到消息历史
        messages.append({"role": "assistant", "content": response.content})

        # 检查最终答案
        if action_data.get("action") == "final_answer":
            answer = action_data.get("action_input", "未提供答案")
            print(f"最终答案: {answer}")
            return answer

        # 执行工具
        tool_name = action_data.get("action")
        tool_input = action_data.get("action_input", {})

        if tool_name in TOOL_REGISTRY:
            try:
                # 执行工具
                if tool_input:
                    result = TOOL_REGISTRY[tool_name](**tool_input)
                else:
                    result = TOOL_REGISTRY[tool_name]()

                # 格式化观察结果
                observation = f"工具 {tool_name} 结果: {result}"
                print(observation)


                # 反思
                # 添加到消息历史
                messages.append({
                    "role": "user",
                    "content": observation
                })
            except Exception as e:
                error_msg = f"工具执行错误: {str(e)}"
                print(error_msg)
                messages.append({
                    "role": "user",
                    "content": error_msg
                })
        else:
            error_msg = f"未知工具: {tool_name}"
            print(error_msg)
            messages.append({
                "role": "user",
                "content": error_msg
            })

    return "超过最大步数，未找到答案"


if __name__ == '__main__':
    # 测试不同问题
    questions = [
        "姚明的身高是多少英尺？",
        #"10公里是多少米？",
        #"2的平方加上3乘以4等于多少？",
        #"现在北京是什么时间？",
        #"水的沸点是多少开尔文？",
        #"珠穆朗玛峰的高度是多少千米？",
        #"请告诉我今天的日期"
    ]

    for q in questions:
        print("=" * 70)
        result = react_agent(q)
        print(f"最终结果: {result}\n")