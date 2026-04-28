
from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
# 需求：
# 做一个能够跳出循环的循环工作流
# 提示：可以通过计数循环次数判断要不要跳出
# 要点：
# 1. 构造一个条件函数
# 2. 添加一个条件边
# 3. 做一个loop_count的自增操作


class State(TypedDict):
    loop_count:int

# 每次循环增加loop_count+1
def node1(state):
    loop_count = state['loop_count']+1
    return {'loop_count':loop_count}
def node2(state: State):
    print(state)


# 弄个条件函数判断loop_count是不是大于3
def condiction_func(state):
    if state['loop_count']>3:
        return 'end'
    else:
        return 'continue'

sg = StateGraph(State) # 实例化一个StateGraph对象
sg.add_node('n1',node1) # 添加一个工作节点
sg.add_node('n2',node2)
# 如何将工作节点连接(边)
sg.add_edge(START,'n1')
# 添加一个条件边
sg.add_conditional_edges(
    # 起始节点
    'n1',
    # 条件函数
    condiction_func,
    # 路径字典
    {'continue': 'n2', 'end': END}
)

sg.add_edge('n2','n1')


# 如何运行工作流
# 1. 先编译
g = sg.compile()

# 画图(可选)
graph_image = g.get_graph().draw_mermaid_png()
image_path = "simple.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 2. 再运行
res = g.invoke({'loop_count':0})

print(res)