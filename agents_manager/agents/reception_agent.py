#from env import anthropic_env
from deepagents import create_deep_agent
from conn.llms import get_silicon
from agents_manager.mytools import minio_tools,terminal_control
from deepagents.backends import FilesystemBackend

p = r'/agent_files'

class ReceptionAgent:
    def __init__(self):
        #tools = asyncio.run(minio_mcp.get_minio_tools())
        #tools.append(gt.get_current_time)

        self.agent = create_deep_agent(
            model=get_silicon(), # 传一个llm
            tools=self.get_tools(), # 工具函数列表
            backend=FilesystemBackend(root_dir=p),
            system_prompt="""你是一个通用智能体"""
        )

    def get_tools(self):
        tools = minio_tools.get_minio_tools()
        tools.append(terminal_control.run_command)
        return tools
    def chat(self,messages):
        res = self.agent.stream({"messages": messages},
            stream_mode = ["updates","messages"])
        return res

    def chat_try(self,user_input):
        messages = [{"role": "user", "content": user_input}]
        return self.chat( messages)

    def steam_try(self,user_input):
        messages = [{"role": "user", "content": user_input}]
        return self.agent.stream({"messages": messages})

if __name__ == '__main__':
    from utils.general_utils.steam_util import stream_print_log
    print(2)
    agent = ReceptionAgent()
    print(1)
    #p = r'D:\agent_file_system'
    stream_print_log(agent.steam_try(f"写一个完整的战棋类游戏"))
