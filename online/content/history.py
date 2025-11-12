
from managers.mysql_manager import MemeryManager as mm
from langchain.messages import AIMessageChunk
from utils.general_utils import globle_util as gu
from configs.global_configs import ROLE_MAP
from utils.general_utils.loggers import logger
class ChatManager:

    @staticmethod
    def chat(agent,conversation_id,user_input):
        sender_id = gu.get_uuid()
        messages = mm.search_history(conversation_id)
        messages.append({
            "role": "user",
            "content": user_input
        })
        mm.insert_memery(conversation_id, sender_id, "human", user_input)

        gen = agent.chat(messages)
        for r in gen:
            if r[0] == "updates":
                logger.info(r)
                obj = r[1].get("model")
                if obj is None:
                    continue
                else:
                    obj = obj.get("messages")[0]
                role = ROLE_MAP[type(obj)]
                content = obj.content
                session_data = obj.response_metadata if obj.response_metadata else None
                mm.insert_memery(conversation_id, sender_id, role, content, session_data=session_data)
            if r[0] == "messages" and type(r[1][0]) == AIMessageChunk and r[1][1]["langgraph_node"]=='model':
                c = r[1][0].content
                if c:
                    yield c