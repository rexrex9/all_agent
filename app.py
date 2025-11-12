from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from online.major import Chat
from pydantic import BaseModel

class Query(BaseModel):
    query: str
    session_id: str

app = FastAPI()
c = Chat()
# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
    expose_headers=["*"]
)

@app.post("/chat")
def stream_text(query: Query):
    # 确保返回的是流式生成器
    return StreamingResponse(
        c.chat(query.query, query.session_id),
        media_type="text/plain"
    )



@app.get("/new_session")
def new_session():
    # 创建新的会话
    return {"session_id": c.new_session()}

@app.get("/switch_session")
def switch_session(session_id: str):
    # 切换会话
    return c.switch_session(session_id)
    # 返回示例[{'content': '你好！😊  \n是的，我可以**流式传输**响应内容 —— 也就是说，我会逐字、逐句地把答案“流式”发送给你，而不是等全部内容准备好后再一次性返回。这样你就能更快地看到开头部分，阅读体验也更自然流畅。\n\n无论是写文档、回答问题，还是生成代码，我都会以流式方式输出，就像和朋友聊天一样自然～\n\n现在，有什么我可以为你做的吗？✨', 'role': 'ai'}, {'content': '你能流式传输吗', 'role': 'human'}, {'content': '你好！👋 很高兴再次见到你～  \n有什么我可以为你做的吗？比如：  \n- 写一份文档？  \n- 整理文件？  \n- 查找信息？  \n- 上传文件到 MinIO？  \n- 或者只是想聊聊天？  \n\n我随时都在，等你吩咐 😊', 'role': 'ai'}, {'content': '你好', 'role': 'human'}, {'content': '你好！看起来你可能想问些什么？或者需要我帮你完成什么任务？无论是写文档、找信息、处理文件，还是其他任何事情，我都很乐意帮忙！🌟', 'role': 'ai'}, {'content': '你好', 'role': 'human'}, {'content': '你好！有什么我可以帮你的吗？😊', 'role': 'ai'}, {'content': '你好', 'role': 'human'}, {'content': '你好！有什么我可以帮你的吗？😊', 'role': 'ai'}, {'content': '你好', 'role': 'human'}]
@app.post("/clear_session")
def clear_session(session_id: str):
    # 清空会话
    return c.clear_session(session_id)




if __name__ == "__main__":
    import uvicorn
    # /docs打开前端
    uvicorn.run(app, host="0.0.0.0", port=8000)