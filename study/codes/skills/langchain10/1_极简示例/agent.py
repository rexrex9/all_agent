from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from conn import llm
agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/",virtual_mode= True),
    skills=["skills"], # 技能目录
    model=llm.get_llm(),
    system_prompt=""",
    注意:
    1. skill的name并非工具名字。
    """
)

result = agent.stream(
    {"messages": [{"role": "user", "content": "1234 * 5678 是多少？"}]},
)

for i in result:
    print(i)