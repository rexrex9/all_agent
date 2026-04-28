from pydantic import BaseModel, Field
from typing import Literal # 导入枚举类型
from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.tools import InjectedToolCallId
from langchain.messages import ToolMessage,SystemMessage,HumanMessage
from typing import Annotated
from langgraph.types import Command
from langchain.agents.middleware import TodoListMiddleware


class Todo(BaseModel):
    content: str = Field(description="单个todo任务的描述")
    status: Literal["排队", "正在处理", "已完成"] =  Field(description="任务状态")

class PlanningState(AgentState):
    todos: list[Todo]
    """任务列表"""  #也可通过 docString来描述参数

# 用来更新State中todos的工具函数
def write_todos(todos: list[Todo],  tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """创建或更新任务列表
     : param todos: 待办事项列表
     : param tool_call_id: 工具调用ID
    """
    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(f"更新了 todo list: {todos}", tool_call_id=tool_call_id)
            ],
        }
    )

class PlanningMiddleware(AgentMiddleware):

    state_schema = PlanningState
    tools = [write_todos]

    def __init__(self):
        self.system_prompt = """
        先将用户的需求拆解为一个任务列表。
        每次工作时，查看任务列表。
        每做完1个任务，更新任务列表中当前任务的状态到 完成。
        """

    async def awrap_model_call(self,request,handler):
        # 把system_prompt加到request里面的state的messages里去
        request.system_prompt = request.system_prompt + "\n\n" + self.system_prompt
        return await handler(request)


'''
# 首先Agent工作之初产生一个任务列表
# 每次工作时，查看任务列表( 会被顺便完成掉，因为首先产生任务列表与更新任务列表的动作都会在上下文中展示最新的任务列表)
# 每做完1个任务，更新任务列表中当前任务的状态到 完成 (仅需提供给Agent更新任务列表的工具，它自己会去安排什么时候更新任务列表的)
'''


