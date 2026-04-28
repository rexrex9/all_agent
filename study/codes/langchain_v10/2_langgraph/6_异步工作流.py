import time
import asyncio
from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
'''
正常情况下，如果要做个异步工作流
则每个节点函数变成 async 异步函数
最后调用的用ainvoke或者astream

但是：新版本的langgraph似乎代码即便是同步的写法，它一样是异步的时间。

'''


class State(TypedDict):
    a:str
    b:int

# 如何声明一个工作节点
async def node1(state):
    await asyncio.sleep(2)

async def node2(state: State):
    await asyncio.sleep(1)

async def node3(state):
    print("node3")


sg = StateGraph(State) # 实例化一个StateGraph对象
sg.add_node('n1',node1) # 添加一个工作节点
sg.add_node('n2',node2)
sg.add_node('n3',node3)
# 如何将工作节点连接(边)
sg.add_edge(START,'n1')
sg.add_edge(START,'n2')
sg.add_edge(['n2','n1'],'n3')
sg.add_edge('n3',END)

# 如何运行工作流
# 1. 先编译
g = sg.compile()

# 画图(可选)
graph_image = g.get_graph().draw_mermaid_png()
image_path = "simple.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

start_time = time.time()
# 2. 再运行
res = asyncio.run(g.ainvoke({'a':'hello', 'b':1}))

print(res)

end_time = time.time()
print(end_time-start_time)