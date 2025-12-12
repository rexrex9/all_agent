import os
from utils.general_utils.globle_util import get_platform

LOG_DIR = os.path.dirname(__file__)

class MINIO:
    # 前端 9090 后台 9000
    ENDPOINT = os.getenv("MINIO_ENDPOINT") if os.getenv("MINIO_ENDPOINT") else "115.190.35.205:9000"
    ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY") if os.getenv("MINIO_ACCESS_KEY") else "rexrex92"
    SECRET_KEY = os.getenv("MINIO_SECRET_KEY") if os.getenv("MINIO_SECRET_KEY") else "rexrex92"

USER_UPLOAD_PATH = 'user_uploads'
GENERATE_IMAGE_PATH = 'generate_images'
ROOT_PATH_AGENT = '/agent_files'
ROOT_PATH_SYSTEM = f'D:/{ROOT_PATH_AGENT}' if get_platform()==0 else ROOT_PATH_AGENT
ROOT_SYSTEM = 'fD:/' if get_platform()==0 else '/'

WAIT_RATE_LIMIT_SEC = 90 # 等待wait_rate_limit的间隔
WAIT_RATE_LIMIT_RETRY = 3 # 重试次数

TAVILY_SEARCH_KEY = os.getenv("TAVILY_SEARCH_KEY")
SILICON_API_KEY = os.getenv("OPENAI_API_KEY")

USE_PPT = True if os.getenv("USE_PPT") and os.getenv("USE_PPT") == 'true' else False
if USE_PPT:
    PPT_MCP_URL = os.getenv("PPT_MCP_URL") if os.getenv("PPT_MCP_URL") else "http://localhost:4810/mcp"
USE_EXCEL =  True if os.getenv("USE_EXCEL") and os.getenv("USE_EXCEL") == 'true' else False

BASE_LLM = os.getenv("BASE_LLM")
BASE_VLM = os.getenv("BASE_VLM")
IMAGE_MODEL = os.getenv("IMAGE_MODEL")
EDIT_IMAGE_MODEL = os.getenv("EDIT_IMAGE_MODEL")
BASE_URL = os.getenv("MODEL_API_BASE_URL")
