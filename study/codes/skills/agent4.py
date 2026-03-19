from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from conn import llms
from tool import execute
agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/agent_files"),
    skills=["skills"],
    model=llms.get_llm(),
    tools= [execute],
    system_prompt="""
    注意:
    1. skill的name并非工具名字。
    2. 直到满足用户需求前都不要停止。
    """
    #     2. 你在windows环境中
)

result = agent.stream(
    {"messages": [{"role": "user", "content": "现在几点？"}]},
    config={"configurable": {"thread_id": "1"}},
)

for i in result:
    print(i)