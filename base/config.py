# 配置文件
import os
from dotenv import load_dotenv
load_dotenv()

BASE_LLM=os.getenv("BASE_LLM")
BASE_VLM=os.getenv("BASE_VLM")
IMAGE_MODEL=os.getenv("IMAGE_MODEL")
EDIT_IMAGE_MODEL=os.getenv("EDIT_IMAGE_MODEL")

MODEL_API_BASE_URL=os.getenv("MODEL_API_BASE_URL")

ROOT_PATH_AGENT  = '/agent_files' # 默认的agent文件存储路径
LOG_DIR = os.path.dirname(__file__) # 当前脚本所在路径作为日志文件存储路径
NEED_CONSOLE_LOG = False # 是否需要控制台打印日志

HOST_IP = os.getenv("HOST_IP")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_ENDPOINT = f"{HOST_IP}:{MINIO_PORT}"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

MINIO_BUCKET = 'agent'
USER_UPLOAD_DIR = 'user_upload'
GENERATE_IMAGE_PATH = 'generate_images'

WAIT_RATE_LIMIT_SEC = 90 # 等待wait_rate_limit的间隔
WAIT_RATE_LIMIT_RETRY = 3 # 重试次数

TAVILY_SEARCH_KEY = os.getenv('TAVILY_SEARCH_KEY')
USE_EXCEL =  True if os.getenv("USE_EXCEL") and os.getenv("USE_EXCEL") == 'true' else False
USE_PPT = True if os.getenv("USE_PPT") and os.getenv("USE_PPT") == 'true' else False
if USE_PPT:
    PPT_MCP_URL = os.getenv("PPT_MCP_URL") if os.getenv("PPT_MCP_URL") else "http://localhost:4810/mcp"

SKILL_DIR_PATH = 'skills'