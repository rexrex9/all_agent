from langchain.agents.middleware import wrap_tool_call
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command
from typing import Callable
from utils.general_utils.loggers import logger
from content.utils import runtime_util as rt

@wrap_tool_call
async def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    filepath_fields = ['filepath', 'filename','image_path','reference_image_path']
    for field in filepath_fields: # 把文件路径转换成绝对路径
        if field in request.tool_call['args']:
            if request.tool_call['args'][field]:
                request.tool_call['args'][field] = rt.change_file_path(request.tool_call['args'][field])
    tool_result = await handler(request) # 执行工具得到结果

    if isinstance(tool_result, ToolMessage): # 把文件路径转换成相对路径
        tool_result.content = rt.get_out_path(tool_result.content)

    return  tool_result