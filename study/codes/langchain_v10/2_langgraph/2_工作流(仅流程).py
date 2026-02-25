import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str

# 1. 初始化图
workflow = StateGraph(State)

# 装饰器，自动将节点添加到工作流
def node(func):
    node_name = func.__name__
    workflow.add_node(node_name, func)

# 状态节点
def start(state: State):
    return {"joke": "msg.content"}

@node
def n1(state: State):
    print("n1 starts execution")
    time.sleep(1)  # 模拟耗时操作
    print("n1 finished")

@node
def n2(state: State):
    print("n2 starts execution")
    time.sleep(2)  # 模拟耗时操作
    print("n2 finished")

@node
def n3(state: State):
    print("n3 starts execution")
    time.sleep(1)  # 模拟耗时操作
    print("n3 finished")

@node
def n4(state: State):
    print("n4 starts execution")
    time.sleep(1)  # 模拟耗时操作
    print("n4 finished")

# 3. 添加连接边
workflow.add_edge(START, "n1")  # n1 从 start 开始
workflow.add_edge("n1", "n2")   # n2 依赖于 n1
workflow.add_edge("n1", "n3")   # n3 依赖于 n1
workflow.add_edge(["n2","n3"], "n4")   # n3 依赖于 n2（n3 将在 n2 执行完后被触发）
workflow.add_edge("n4", END)    # n3 到达结束节点

# 4. 编译图
graph = workflow.compile()

# 5. 保存（可选）
graph_image = graph.get_graph().draw_mermaid_png()
image_path = "flow.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 6. 执行
state = graph.invoke({"topic": "猫"}, print_mode='updates')
print(state)