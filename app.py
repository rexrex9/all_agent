# 尝试用fastapi去写服务接口, 学习用，其中大量伪代码


import fastapi
from pydantic import BaseModel
from all_agent import agent
from fastapi import WebSocket, WebSocketDisconnect
import json
from langchain_core.load import dumpd  # 或者 dumps
from langchain.messages import AIMessageChunk
import uuid
class Query(BaseModel):
    query: str
    session_id: str

app = fastapi.FastAPI()

@app.get('/')
def hello_world():
    return 'Hello, World!'

@app.post('/new_thread')
def new_thread_id():
    thread_id = uuid.uuid4()
    # 在数据库thread表里新建一行数据
    sql_manager.insert_thread(thread_id)
    return thread_id

@app.post('/swich_thread')
def swich_thread(thread_id: str):
    # 在数据库thread表里更新行数据
    messages = menery_manager.get_history(thread_id)
    return 序列化的(messages)

@app.post('/delete_thread')
    # 删除数据库thread表里的数据
def delete_thread(thread_id: str):
    sql_manager.delete_thread(thread_id)
    menery_manager.delete_history(thread_id)

@app.websocket('/chat')
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 接收前端发送的消息
            data = await websocket.receive_text()
            # 这里假设前端发送的是 JSON 字符串
            query_data = json.loads(data)
            query = query_data.get('query', '')
            # session_id获取
            # messages = 通过session_id获取history

            # 遍历异步生成器
            async for i in agent.astream({'messages': {'role':'user', 'content': query},
                                          },stream_mode=['updates','messages']):
                if i[0] == 'updates':  # 通过判断元组中的第一个是否是updates，来判断是否是打印日志
                    # 异步存储内容到记忆数据库
                    await websocket.send_text(json.dumps(dumpd(i[1])))
                else:
                    # 1. 过滤掉空token
                    token = i[1][0].content
                    if token.strip():
                        if type(i[1][0]) == AIMessageChunk:  # 2. 过滤掉toolmessage (通过判断它的数据类型是否是AIMessageChunk)
                            await websocket.send_text(token)
            # 发送结束标记（可选）
            await websocket.send_text("[END]")


    except WebSocketDisconnect:
        print("Client disconnected")



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=9115)