import time
from typing_extensions import TypedDict # 继承这个就代表是一个字典
from langgraph.graph import StateGraph, START, END

# 定义状态
class State(TypedDict):
    k1: str
    k2: str

# 1. 初始化图
workflow = StateGraph(State)

# 装饰器，自动将节点添加到工作流
def node(func):
    node_name = func.__name__
    workflow.add_node(node_name, func)

@node
def n1(state: State):
    print("n1 starts execution")
    print(state)
    time.sleep(1)
    state["k1"]= "n1"

@node
def n2(state: State):
    print("n2 starts execution")
    print( state)
    time.sleep(1)
    return {"k2": "n2"}


workflow.add_edge(START, "n1")
workflow.add_edge(START, "n2")
workflow.add_edge(["n1","n2"], END)

graph = workflow.compile()
state = graph.invoke({"k1": "k1","k2":"k2"})

print('finish')
print(state)
