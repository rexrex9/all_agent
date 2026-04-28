from langchain.agents import create_agent # 创建智能体的包
from langchain.messages import HumanMessage
from conn.llm import get_llm


def write_file(file_path,content):
    """写文件的函数"""
    with open(file_path,"w+",encoding="utf-8") as f:
        f.write(content)


agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[write_file], # 工具集
    system_prompt="你是一个助力", # 系统提示词
)

# Run the agent
res = agent.invoke({"messages":[HumanMessage(content="给我写个html贪吃蛇")]})






