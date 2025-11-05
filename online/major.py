from agents_manager.agents.reception_agent import ReceptionAgent
from online.content.history import ChatManager as cm


class Chat:
    def __init__(self):
        self.reception_agent = ReceptionAgent()

    def chat(self,user_input,conversation_id):
        return cm.chat(self.reception_agent,conversation_id,user_input)



if __name__ == '__main__':
    from utils.general_utils.steam_util import stream_print
    c = Chat()

    cid = '3c46d42655b94e0f97b211ee2a371bb2'
    while True:
        user_input = input("用户：")
        res = c.chat(user_input,cid)
        stream_print(res)

