import os
from env import serect
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] =  serect.LANGSMITH_API_KEY
os.environ["LANGSMITH_ENDPOINT"]="https://api.smith.langchain.com"
# 平台地址 https://smith.langchain.com/