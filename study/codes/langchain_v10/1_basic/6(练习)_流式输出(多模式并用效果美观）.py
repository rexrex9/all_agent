
from langchain.messages import AIMessageChunk
from langchain.agents import create_agent # 创建智能体的包

def stream_both(agent, input):
    # 需求
    # 传入智能体和用户的输入，流式打印updates的日志与流式打印token,并且token要提出来打印
    res = agent.stream({"messages":[{'role':'user','content':input}]},stream_mode=['updates','messages'])
    for i in res:
        if i[0]=='updates': # 通过判断元组中的第一个是否是updates，来判断是否是打印日志
            print(i[1])
        else:
            # 1. 过滤掉空token
            token = i[1][0].content
            if token.strip():
                if type(i[1][0])==AIMessageChunk: # 2. 过滤掉toolmessage (通过判断它的数据类型是否是AIMessageChunk)
                    print(token, end="|")



from conn.llm import get_llm
def get_weather(city: str) -> str:
    """获得天气的工具"""
    return f"它总是雨天在 {city}!"

agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[get_weather], # 工具集
    system_prompt="你是一个助力", # 系统提示词
)

stream_both(agent, "南京什么天气？")
