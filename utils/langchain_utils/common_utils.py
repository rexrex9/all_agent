from langgraph.graph.state import CompiledStateGraph
# 做一个画图的工具

def save_graph_img(graph:CompiledStateGraph, image_path: str):
    graph_image = graph.get_graph().draw_mermaid_png()
    with open(image_path, "wb+") as f:
        f.write(graph_image)
