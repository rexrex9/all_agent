import json

from conn import mysql_conn as MC
from utils.general_utils import globle_util as gu

mc = MC.MysqlConn()


class MemeryManager:

    TABLE_NAME = 'chat_conversations'

    # 插入会话记录
    @classmethod
    def insert_memery(cls,conversation_id,sender_id,role,content,session_data= None):
        d = {'conversation_id':conversation_id,
             'sender_id':sender_id,
             'role':role,
             'content':content,
             'session_data':json.dumps(session_data)}
        mc.insert(cls.TABLE_NAME,d)


    # 根据session_id得到前k个聊天历史并拼接一下返回
    @classmethod
    def search_history(cls,conversation_id,k=5):
        sql = f'select content,role from {cls.TABLE_NAME} where conversation_id=%s and status=1 order by created_at desc limit %s'
        params = (conversation_id,k)
        historys = mc.search_with_params(sql, params)
        return historys if historys else []

    # 根据session_id清空会话记录,将状态改为0
    @classmethod
    def clear_memery(cls,conversation_id):
        sql = f'update {cls.TABLE_NAME} set status=0 where conversation_id ="%s"' % conversation_id
        mc.execute(sql)


if __name__ == '__main__':
    #conversation_id = MemeryManager.new_session()

    sender_id = gu.get_uuid()
    sender_type = 'user'
    # user
    # assistant
    message_content = 'asdasdadaaassaa'
    #MemeryManager.insert_memery(conversation_id,sender_id,sender_type,message_content)

    a = MemeryManager.search_history('123')
    print(a)