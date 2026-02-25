from conn.llms import get_llm
from my_create_agent import create_agent # 导入自定义的create_agent函数
from my_tools import * # 导入自定义的工具

agent = create_agent(
    llm=get_llm(),
    tools=[search, calculator, current_time, unit_converter],
    system_prompt="你是一个有用的Agent"
)

print("开始执行")
for chunk in agent.stream({
    "messages": [{'role':'user','content':"姚明的身高是多少英尺？"}]
}):
    print(chunk)
    print("---")