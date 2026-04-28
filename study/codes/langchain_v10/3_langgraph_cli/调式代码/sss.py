import flask
import uuid
app = flask.Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/hello2")
def hello2():
    return "Hello World2!"


# 新建会话窗口的接口
@app.route("/new_session")
def new_session():
    # 得到一个会话id
    session_id = uuid.uuid4().hex
    # 把这个会话id在mysql新建一条记录


    # 返回这个会话id到前端
    return session_id

@app.route("/chat")
def chat(request):
    session_id = request.args.get("session_id")
    query = request.args.get("query")
    #context = 加载上下文，用session_id从mysql中加载
    #prompt = context+query
    #res = agent.chat(prompt)
    #mysql.save(session_id,res) # 添加AI的回复到mysql里的上下文记录种
    #return res # 把回复返回给前端

@app.route("/switch_session")
def switch_session(request):
    session_id = request.args.get("session_id")
    #return mysql.load(session_id) # 加载上下文


# 如果要做一个完整的Agent后端
'''
新建会话窗口的接口
切换窗口的接口
删除会话窗口接口
与Agent对话的接口

'''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)