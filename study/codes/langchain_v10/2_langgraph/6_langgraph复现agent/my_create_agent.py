"""
辅助理解代码
使用 LangGraph 复现 LangChain 的 create_agent
"""
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode # 导入tool节点
from langchain.messages import AnyMessage # 导入一个任何message的类
from typing_extensions import TypedDict, Annotated # 导入类型定义工具
import operator # 导入操作符
from common_utils import save_graph_img # 导入自定义保存流程图函数


# 定义 Agent 状态
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


def create_agent(llm, tools, system_prompt: str = None):

    # 1. 模式系统ReAct形式的提示词
    default_system_prompt = """你是一个智能助手，使用ReAct（Reasoning and Acting）模式解决问题。请按照以下步骤思考：
        1. 思考(Thought)：分析问题，决定下一步行动
        2. 行动(Action)：调用工具或回答问题
        3. 观察(Observation)：获取工具执行结果
        以下是用户自定义的system_prompt
        """
    system_prompt = default_system_prompt + system_prompt

    # 2. 模型绑定工具
    llm = llm.bind_tools(tools)

    # 3. 定义模型节点
    def call_model(state: AgentState):
        messages = [{"role": "system", "content": system_prompt}] + state["messages"]
        return {"messages": [llm.invoke(messages)]}

    # 4. 定义条件函数
    def should_continue(state: AgentState):
        """判断是否继续执行工具或结束"""
        messages = state["messages"]
        last_message = messages[-1]
        # 如果没有工具调用，结束
        if last_message.tool_calls:
            return "continue"
        else:
            return "end"

    # 创建图
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # 设置入口点
    workflow.add_edge(START, "agent")

    # 添加条件边
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    # 工具执行后返回 agent
    workflow.add_edge("tools", "agent")
    # 编译图
    agent = workflow.compile()
    # 保存图（可选）
    save_graph_img(agent, "agent.png")

    return agent
