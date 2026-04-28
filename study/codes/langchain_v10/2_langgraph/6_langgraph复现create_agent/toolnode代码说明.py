
from langchain.messages import ToolMessage
from mytools import *

tools = [search, calculator, current_time, unit_converter]
tools_by_name = {tool.name: tool for tool in tools} # 注册工具

def tool_node(state):
    """执行工具调用"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}
