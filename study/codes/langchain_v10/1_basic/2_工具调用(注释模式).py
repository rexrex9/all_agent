from datetime import datetime
from langchain.agents import create_agent
from conn.llm import get_llm


def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city: str,datetime:str) -> str:
    """
    获取天气
    :param city: 城市
    :datetime: 日期
    :return:
    """
    return f"今天是{datetime}，{city}在下雨!"

# 工具函数必须要有描述

# 工具函数三要素_
# 名称(函数名）
# 描述(文档字符串）
# 参数

llm = create_agent(
    model=get_llm(),
    tools=[get_current_time,get_weather],
    system_prompt="你是一个时间查询工具"
)

res = llm.invoke({"messages":[{'role':'user','content':'今天北京的天气是什么。要明确告诉我今天的日期？'}]})
print( res["messages"][-1].content)