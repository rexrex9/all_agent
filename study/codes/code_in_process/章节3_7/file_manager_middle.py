from langchain.agents.middleware import AgentMiddleware
from utils.doc_utils import os_util as ou
from content.utils import runtime_util as ru
from content.utils import base64_util as bu
from langchain.messages import ToolMessage,AIMessage
from utils.general_utils import globle_util as gu
from utils.doc_utils import zip_files as zf
from langchain.agents.middleware import AgentState
import time
import asyncio
from conn.minio_conn import MinioConn
import os
from base import configs as cfg
from utils.general_utils.loggers import logger

class CustomState(AgentState):
    start_work_time: float  # Agent工作开始的时间戳
    file_update_time: float  # 文件最后更新时间戳，用于检测文件变化
    upload_files: list # 用户上传的文件列表

# 基于类的中间件
class FileMiddleware(AgentMiddleware):
    state_schema = CustomState

    def __init__(self):
        super().__init__()
        self.mc = MinioConn() # 创建Minio连接


    async def abefore_agent(self, state, runtime):
        # 先创建user_upload文件夹
        upload_dir_path = os.path.join(ru.get_root_dir(runtime),cfg.USER_UPLOAD_PATH ) # 拼接user_upload文件夹的绝对路径

        await asyncio.to_thread(os.makedirs,upload_dir_path,exist_ok=True) # 异步创建文件夹
        result = {'file_update_time': time.time(), 'start_work_time': time.time()}

        files = []
        upload_files = state.get('upload_files')
        if upload_files:
            # 处理一下upload_files
            for file in upload_files: # 遍历用户上传的文件列表
                # 异步解码base64数据
                d = await asyncio.to_thread(bu.save_base64_file_from_content_block,file,upload_dir_path)
                files.append(ru.get_out_path(d['file_path'])) # 把绝对路径改为相对路
            # 把用户上传的文件列表给到Agent去看，放到Messages中
            s = '用户上传了文件,文件列表如下:\n'
            s += '\n'.join(files)
            result['messages'] = [ToolMessage(content=s, tool_call_id=gu.get_uuid(), name='file_upload')]
            result['upload_files'] = None # 清空upload_files
        return  result


    async def _check_if_new_file(self, folder_path, work_start_time):
        """
        检查文件夹中是否有比指定时间更新的文件

        参数:
        folder_path: str - 要检查的文件夹路径
        work_start_time: float - 参考时间戳

        返回:
        bool: 如果存在比work_start_time更新的文件返回True，否则False
        """

        if not os.path.exists(folder_path): # 文件夹不存在直接返回false
            return False
        # 异步执行文件时间检查，避免阻塞事件循环
        max_time = await asyncio.to_thread(ou.get_folder_file_update_time_max, folder_path)
        return max_time > work_start_time  # 比较最新文件时间与参考时间

    async def abefore_model(self, state, runtime):
        # 问题 3，通过检测文件更新时间判断是否要获取目录树
        # 仅当有新的文件出现后，或者文件被修改过时或者被删除时，才返回目录树
        root_dir = ru.get_root_dir(runtime) # 问题 1：获取root_dir的值
        if await self._check_if_new_file(root_dir,state['start_work_time']): # 判断是否有新的文件
            trees = ou.get_directory_tree(root_dir=root_dir) # 获取目录树
            toolmessage = ToolMessage(content = f'当前目录结构:{trees}', tool_call_id=gu.get_uuid(), name='file_tree')
            return {'messages':[toolmessage],'file_update_time':time.time()}
        # 问题 2：目录结构要怎么return给模型
        # 把树形结构被包裹在 toolmessage里返回给模型

    async def awrap_tool_call(self,request,handler):
        # 在调用工具之前去修改路径到绝对路径
        # 1. 检查request中是否存在路径
        #logger.info(request)
        filepath_fields = ['filepath', 'filename', 'image_path', 'reference_image_path']
        for file_path_field in filepath_fields:
            if file_path_field in request.tool_call['args']:
                file_path = request.tool_call['args'][file_path_field] # 获取文件路径
                # 2. 修改路径为绝对路径
                request.tool_call['args'][file_path_field] = ru.change_file_path(file_path) # 把相对路径改为绝对路径
        try:
            # 执行实际工具调用
            result = await handler(request)
        except Exception as e:
            # 捕获异常并返回错误信息
            return ToolMessage(
                content=f"Error: {e}",
                tool_call_id=request.tool_call['id'],
                name=request.tool_call['name']
            )

        if isinstance(result, ToolMessage): # 判断是否是ToolMessage,或者是ToolMessage的子类
            result.content = ru.get_out_path(result.content) # 把绝对路径改为相对路径
        return result

    async def aafter_agent(self, state, runtime):
        # 1. 检查文件变化
        root_dir = ru.get_root_dir(runtime)
        if await self._check_if_new_file(root_dir,state['start_work_time']):
            # 2. 压缩工作目录
            zip_file_path = await asyncio.to_thread(zf.compress_dir, root_dir)
            file_name = os.path.basename(zip_file_path) # 获取文件名
            # 3. 异步上传到MinIO对象存储
            await asyncio.to_thread(self.mc.upload_file,file_name, zip_file_path)
            # 4. 生成下载链接
            download_url = self.mc.gen_presigned_url(file_name)
            # 把download_url以AIMessage的形式追加更新messages

            # 之所以弄两个AIMessage是因为下载链接只有完整的出现在一个AIMessage中时，在前端的下载链接才是一个可点击的超链接
            return {'messages':
                        [AIMessage(content='可通过如下地址下载: '),
                         AIMessage(content=download_url)]
                    }