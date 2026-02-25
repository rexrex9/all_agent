from langchain.agents.middleware import AgentMiddleware,AgentState
from langchain.tools import tool
from langchain.messages import ToolMessage
from pydantic import BaseModel, Field
from typing import Literal,Annotated # 导入枚举类型
from langgraph.types import Command
from langchain.tools import InjectedToolCallId
class Todo(BaseModel):
    content: str  = Field(description="单个todo任务的描述")
    status: Literal["排队", "正在处理", "已完成"] =  Field(description="任务状态")

class PlanningState(AgentState):
    todos: list[Todo]
    """任务列表"""  #也可通过 docString来描述参数

class PlaningMiddleware(AgentMiddleware):

    state_schema = PlanningState
    def __init__(self):
        super().__init__()

        self.system_prompt = '''
        进行任务时，首先规划一下任务，然后使用 write_todos 工具来帮助管理和规划任务目标,并把todo list记录下来。
        确保跟踪每个步骤进度，更新状态，并向用户完整展示你的进度(包含已完成与正在排队的),一定要完整。
        关键要求：完成一个步骤后，必须立即将该待办事项标记为已完成。不要等到完成多个步骤后才批量标记。
        '''

        @tool
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
        self.tools = [write_todos]

    async def awrap_model_call(self,request,handler):
        request.system_prompt =  request.system_prompt + "\n\n" + self.system_prompt
        return await handler(request)

