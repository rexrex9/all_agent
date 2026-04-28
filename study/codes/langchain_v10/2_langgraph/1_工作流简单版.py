
from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
# 状态
# 在整个工作流中传递数据的一个字典模板
class State(TypedDict):
    a:str
    b:int

# 如何声明一个工作节点
def node1(state):
    print(state)

def node2(state: State):
    print("node2")

def node3(state):
    print("node3")

def node4(state):
    print("node4")

sg = StateGraph(State) # 实例化一个StateGraph对象
sg.add_node('n1',node1) # 添加一个工作节点
sg.add_node('n2',node2)
sg.add_node('n3',node3)
sg.add_node('n4',node4)
# 如何将工作节点连接(边)
sg.add_edge(START,'n1')
sg.add_edge('n1','n2')
sg.add_edge('n1','n3')
sg.add_edge(['n2','n3'],'n4')
sg.add_edge('n4',END)

# 如何运行工作流
# 1. 先编译
g = sg.compile()

# 画图(可选)
graph_image = g.get_graph().draw_mermaid_png()
image_path = "simple.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)


# 2. 再运行
res = g.invoke({'a':'hello', 'b':1})

print(res)