import math
import datetime
from langchain.tools import tool

@tool
def search(query):
    """搜索知识"""
    knowledge_base = {
        "姚明身高": "2.29米",
        "珠穆朗玛峰高度": "8848.86米",
        "地球到月球距离": "384400公里",
        "水的沸点": "100°C",
        "北京人口": "2189万"
    }
    return knowledge_base.get(query, f"未找到关于'{query}'的信息")

@tool
def calculator(expression):
    """计算数学表达式"""
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

@tool
def current_time():
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def unit_converter(value, from_unit, to_unit):
    """
    单位转换工具
    :param value: 待转换的值
    :param from_unit: 转换前的单位
    :param to_unit: 转换后的单位
    :return:
    """
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