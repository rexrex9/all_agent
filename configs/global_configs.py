from langchain.messages import AIMessage,ToolMessage,HumanMessage

ROLE_MAP = {
    AIMessage: "ai",
    HumanMessage: "human",
    ToolMessage: "tool",
}

WORK_P = '/agent_files'
RATE_LIMIT = 40000
WAIT_RATE_LIMIT_SEC = 60