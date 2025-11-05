
from deepagents import create_deep_agent
from conn.llms import get_deepseek
from agents_manager.mytools import globle_tools as gt


class ReceptionAgent:
    def __init__(self):
        self.agent = create_deep_agent(
            model=get_deepseek(), # 传一个llm
            tools=[gt.get_current_time], # 工具函数列表
            system_prompt="""你是一个通用智能体"""
        )

    def chat(self,messages):
        res = self.agent.stream({"messages": messages},
            stream_mode = ["updates","messages"])
        return res

    def chat_try(self,user_input):
        messages = [{"role": "user", "content": user_input}]
        return self.chat( messages)

if __name__ == '__main__':
    from utils.general_utils.steam_util import steam_print_all
    print(2)
    agent = ReceptionAgent()
    print(1)
    steam_print_all(agent.chat("现在几点"))
