from datetime import datetime
from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.tools import tool
from pydantic import BaseModel, Field #字段
# pydantic 用来约束参数类型的一个基础库

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")


@ tool(name_or_callable="get_current_time", description="获取当前时间")
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@ tool(name_or_callable="get_weather", description="获取天气", args_schema=WeatherInput)
def get_weather(city: str) -> str:
    return f"它总是雨天在 {city}!"


llm = create_agent(
    model=get_llm(),
    tools=[get_current_time,get_weather],
    system_prompt="你是一个时间查询工具"
)

res = llm.invoke({"messages":[{'role':'user','content':'北京什么天气？'}]})
print( res["messages"][-1].content)