from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from conn import llms

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/",virtual_mode= True),
    skills=["skills"],
    model=llms.get_small_llm(),
    system_prompt=""",
    注意:
    1. skill的name并非工具名字。
    2. 直到满足用户需求前都不要停止。
    3. 你在windows环境中
    """
)

result = agent.stream(
    {"messages": [{"role": "user", "content": "1234 * 5678 是多少？"}]},
    config={"configurable": {"thread_id": "1"}},
)

for i in result:
    print(i)