from deepagents import create_deep_agent
from conn.llm import get_llm
from deepagents.backends.filesystem import FilesystemBackend
import excute_middle


agent = create_deep_agent(
    backend=FilesystemBackend(root_dir=excute_middle.root_dir,virtual_mode=True),
    skills=["skills"],
    model=get_llm(),
    tools= [],
    middleware=[excute_middle.ExcuteMiddleware()],
    system_prompt=""",
    注意:
    1. skill的name并非工具名字。
    """
)

for chunk in agent.stream({"messages": [{"role": "user", "content": "你手上有几个技能"}]}):
    print(chunk)


