from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from conn.llm import get_llm

llm = get_llm()
# 状态
class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
# 节点
def generate_joke(state: State):
    print(f"开始生成笑话: {state['topic']}")
    msg = llm.invoke(f"请写一个关于{state['topic']}的简短中文笑话")
    return {"joke": msg.content}

def improve_joke(state: State):
    print(f"开始提高笑话: {state['joke']}")
    msg = llm.invoke(f"为这个笑话添加一个意想不到的转折: {state['joke']}, 仅输出提高后的笑话")
    return {"improved_joke": msg.content}



# 1.初始化图
workflow = StateGraph(State)
# 2.添加节点
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)

# 3.添加连接边
workflow.add_edge(START, "generate_joke")
workflow.add_edge("generate_joke", "improve_joke")
workflow.add_edge("improve_joke", END)
# 4.编译图
graph = workflow.compile()

# 5.保存(可选)
graph_image = graph.get_graph().draw_mermaid_png()
image_path = "simple.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 执行
state = graph.invoke({"topic": "猫"},print_mode='updates')
print(state['improved_joke'])