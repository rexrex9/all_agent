from agents_manager.agents.reception_agent import ReceptionAgent
from online.content.history import ChatManager as cm
from managers import mysql_manager as mm
from utils.general_utils import globle_util as gu
from utils.general_utils import os_util as ou
from configs import global_configs as gcfg
class Chat:
    def __init__(self):
        self.reception_agent = ReceptionAgent()

    def chat(self,user_input,conversation_id):
        return cm.chat(self.reception_agent,conversation_id,user_input)

    def new_session(self):
        return gu.get_uuid()

    def switch_session(self,conversation_id):
        return mm.MemeryManager.switch_session(conversation_id)

    def clear_session(self,conversation_id):
        mm.MemeryManager.clear_memery(conversation_id)
        p = 'D:'+gcfg.WORK_P if gu.get_platform()==0 else gcfg.WORK_P
        ou.delete_folder_contents(p)


if __name__ == '__main__':
    from utils.general_utils.steam_util import stream_print
    c = Chat()

    cid = '111'
    while True:
        user_input = input("用户：")
        res = c.chat(user_input,cid)
        stream_print(res)

