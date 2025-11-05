from langchain.messages import AIMessage,ToolMessage,HumanMessage


ROLE_MAP = {
    AIMessage: "ai",
    HumanMessage: "human",
    ToolMessage: "tool",
}