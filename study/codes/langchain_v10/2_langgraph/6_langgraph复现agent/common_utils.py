
def save_graph_img(workflow, image_path):
    """保存图"""
    graph_image = workflow.get_graph().draw_mermaid_png()
    with open(image_path, "wb+") as f:
        f.write(graph_image)
