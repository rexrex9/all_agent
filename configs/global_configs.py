from langchain.messages import AIMessage,ToolMessage,HumanMessage
from utils.general_utils.globle_util import get_platform

ROLE_MAP = {
    AIMessage: "ai",
    HumanMessage: "human",
    ToolMessage: "tool",
}

USER_UPLOAD_PATH = 'user_uploads'
ROOT_PATH_AGENT = '/agent_files'
ROOT_PATH_SYSTEM = f'D:/{ROOT_PATH_AGENT}' if get_platform()==0 else ROOT_PATH_AGENT


RATE_LIMIT = 400000000
WAIT_RATE_LIMIT_SEC = 60


#POSTGRE_STR="postgresql://myuser:mypassword@115.190.35.205:25432/all_agent"