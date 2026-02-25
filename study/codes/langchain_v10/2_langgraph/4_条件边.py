from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# 定义状态
class State(TypedDict):
    k1: int

# 1. 初始化图
workflow = StateGraph(State)


def node(func):
    """装饰器，自动将节点添加到工作流"""
    node_name = func.__name__
    workflow.add_node(node_name, func)

@node
def n1(state: State):
    state["k1"]+= 1
    return {"k1": state["k1"]}

@node
def n2(state: State):
    print('in n2')

@node
def n3(state: State):
    print('in n3')

# 条件函数
def flag_funcation(state: State):
    if state["k1"]>3:
        return "1"
    else:
        return "0"

# 3. 添加连接边
workflow.add_edge(START, "n1")
# 条件边
workflow.add_conditional_edges('n1', flag_funcation,{"0": "n2", "1": "n3"})
workflow.add_edge("n2", END)
workflow.add_edge("n3", END)

# 4. 编译图
graph = workflow.compile()

# 5. 保存（可选）
graph_image = graph.get_graph().draw_mermaid_png()
image_path = "condition.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 6. 执行
state = graph.invoke({"k1": 3}, print_mode='updates')
print(state)

