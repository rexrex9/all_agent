#from langchain.agents import create_agent
from my_agent import create_agent
from mytools import *

from conn.llm import get_llm


agent = create_agent(model=get_llm(),
             tools=[search,calculator,current_time,unit_converter],
             system_prompt="你是一个助手")

res = agent.stream({"messages":[{"role":"user","content":"姚明身高是多少英尺？优先尝试工具"}]})

figure = agent.get_graph().draw_mermaid_png()
with open("sss.png", "wb+") as f:
    f.write(figure)

for chunk in res:
    print(chunk)
