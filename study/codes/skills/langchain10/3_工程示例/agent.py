from deepagents import create_deep_agent
from conn.llms import get_llm
from deepagents.backends.filesystem import FilesystemBackend
from execute_middle import ExecuteMiddleware,ROOT_DIR


agent = create_deep_agent(
    backend=FilesystemBackend(root_dir=ROOT_DIR,virtual_mode= True),
    skills=["skills"],
    model=get_llm(),
    middleware=[ExecuteMiddleware()],
    system_prompt=""",
    注意:
    1. skill的name并非工具名字。
    2. 直到满足用户需求前都不要停止。
    3. 你在windows环境中
    """
)

from utils.langchain_utils import stream_util as su

while True:
    user = input("用户:")
    su.stream_both(agent,user)
